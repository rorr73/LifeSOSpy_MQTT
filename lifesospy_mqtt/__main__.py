"""
Provides a MQTT client to report state of LifeSOS security system and devices.
"""

import argparse
import asyncio
import logging
import sys
from lifesospy.protocol import Protocol
from lifesospy_mqtt.config import Config
from lifesospy_mqtt.const import EX_OK, EX_NOHOST, EX_CONFIG
from lifesospy_mqtt.const import PROJECT_VERSION, PROJECT_DESCRIPTION
from lifesospy_mqtt.logger import configure as logger_configure
from lifesospy_mqtt.translator import Translator

_LOGGER = logging.getLogger(__name__)


def main(argv):
    """
    Runs MQTT loop to publish LifeSOS states.
    """

    # Configure logger format
    logging.basicConfig(
        format="%(asctime)s %(levelname)-5s (%(threadName)s) [%(name)s] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S')

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="LifeSOSpy_MQTT v{} - {}".format(
            PROJECT_VERSION, PROJECT_DESCRIPTION))
    parser.add_argument(
        '-c', '--config',
        help="Path to configuration file.",
        default=Config.get_default_path())
    parser.add_argument(
        '-d', '--devices',
        help="List devices enrolled on base unit and exit.",
        action='store_true')
    args = parser.parse_args()

    # Display application header
    print("LifeSOSpy_MQTT v{} - {}\n".format(PROJECT_VERSION, PROJECT_DESCRIPTION))

    # Load the configuration file, or create default if none exists
    config = Config.load(args.config)
    if not config:
        sys.exit(EX_CONFIG)
    elif config.is_default:
        print("\nA default configuration file has been created:\n{}\n\n"
              "Please edit any settings as needed then restart."
              .format(config.config_path))
        sys.exit(EX_CONFIG)

    # Configure logging using our settings
    logger_configure(config)

    # Provide an event loop for the rest of this
    loop = asyncio.get_event_loop()
    try:

        # If user just wants to list devices, do so and exit afterwards
        if args.devices:
            loop.run_until_complete(
                _async_list_devices(config))
            sys.exit(EX_OK)

        # Run the translator
        loop.run_until_complete(
            _async_run_translator(config))

    except KeyboardInterrupt:
        pass
    except Exception: # pylint: disable=broad-except
        _LOGGER.exception("Exiting due to unhandled exception")
    finally:
        loop.close()


async def _async_run_translator(config: Config) -> None:
    translator = Translator(config)
    await translator.async_start()
    try:
        await translator.async_loop()
    finally:
        await translator.async_stop()


async def _async_list_devices(config: Config) -> None:
    """List all devices enrolled on the base unit."""
    from lifesospy.command import GetDeviceByIndexCommand
    from lifesospy.devicecategory import DC_ALL
    from lifesospy.response import DeviceNotFoundResponse

    protocol = await _async_new_protocol(config)
    try:
        print("Listing devices...")
        count = 0
        for category in DC_ALL:
            if category.max_devices:
                for index in range(0, category.max_devices):
                    response = await protocol.async_execute(
                        GetDeviceByIndexCommand(category, index))
                    if response is None or \
                            isinstance(response, DeviceNotFoundResponse):
                        break
                    print(response)
                    count += 1
        print("{} devices found.".format(count))
    finally:
        protocol.close()


async def _async_new_protocol(config: Config) -> Protocol:
    if config.lifesos.host:
        # Create a Client instance and connect to server
        from lifesospy.client import Client

        client = Client(config.lifesos.host, config.lifesos.port)
        if config.lifesos.password:
            client.password = config.lifesos.password
        try:
            await client.async_open()
        except Exception: # pylint: disable=broad-except
            _LOGGER.error("Failed to connect to LifeSOS network interface.", exc_info=True)
            sys.exit(EX_NOHOST)
        return client

    else:
        # Create a Server instance and wait for connection
        from lifesospy.server import Server

        connected = asyncio.Event(loop=asyncio.get_event_loop())

        def _on_connection_made(protocol: Protocol):
            connected.set()

        server = Server(config.lifesos.port)
        if config.lifesos.password:
            server.password = config.lifesos.password
        server.on_connection_made = _on_connection_made
        await server.async_listen()
        print("Waiting for client connection...")
        await connected.wait()
        return server


if __name__ == "__main__":
    main(sys.argv)
