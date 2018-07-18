"""
Provides a MQTT client to report state of LifeSOS security system and devices.
"""

import argparse
import asyncio
import logging
import logging.handlers
import os
import sys
from lifesospy.protocol import Protocol
from lifesospy_mqtt.config import Config
from lifesospy_mqtt.const import EX_OK, EX_NOHOST, EX_CONFIG
from lifesospy_mqtt.const import PROJECT_VERSION, PROJECT_DESCRIPTION
from lifesospy_mqtt.translator import Translator

_LOGGER = logging.getLogger(__name__)


def main(argv):
    """
    Runs MQTT loop to publish LifeSOS states.
    """

    # Display application header
    print("LifeSOSpy_MQTT v{} - {}\n".format(
        PROJECT_VERSION, PROJECT_DESCRIPTION))

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-d', '--daemon',
        help="Put the application into the background after starting.",
        action='store_true')
    group.add_argument(
        '-e', '--devices',
        help="List devices enrolled on base unit and exit.",
        action='store_true')
    parser.add_argument(
        '-c', '--config',
        help="Path to configuration file.",
        default=Config.get_default_path())
    parser.add_argument(
        '-l', '--logfile',
        help="When specified, path to daily rolling log file to be used.",
        default=None)
    parser.add_argument(
        '-p', '--pidfile',
        help="When specified, path to file that will record the process ID"
             " and is used for locking.",
        default=None)
    parser.add_argument(
        '-v', '--verbose',
        help="Display all logging output.",
        action='store_true')
    args = parser.parse_args()

    # Create log handlers; attach daily rolling log file handler if needed
    handlers = [logging.StreamHandler()]
    logfile_handler = None
    if args.logfile:
        logfile = os.path.expanduser(os.path.expandvars(args.logfile))
        logfile_handler = logging.handlers.TimedRotatingFileHandler(
            logfile, when='midnight', backupCount=5)
        handlers.append(logfile_handler)

    # Configure logger format, and set Debug level if verbose arg specified
    logging.basicConfig(
        format="%(asctime)s %(levelname)-5s (%(threadName)s) [%(name)s] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        level=None if not args.verbose else logging.DEBUG,
        handlers=handlers)

    # The python-daemin library isn't compatible with Windows
    if args.daemon and os.name == 'nt':
        _LOGGER.error("Daemon is not supported on Windows")
        sys.exit(EX_CONFIG)

    # Load the configuration file, or create default if none exists
    config = Config.load(args.config)
    if not config:
        sys.exit(EX_CONFIG)
    elif config.is_default:
        print("\nA default configuration file has been created:\n{}\n\n"
              "Please edit any settings as needed then restart."
              .format(config.config_path))
        sys.exit(EX_CONFIG)

    # Apply the config settings to logger system
    _apply_logger_config(config, args)

    # List devices only and exit
    if args.devices:
        _list_devices(config)
        sys.exit(EX_OK)

    # Run the translator
    if args.daemon:
        import daemon
        from daemon.pidfile import TimeoutPIDLockFile
        print("Starting daemon.")
        with daemon.DaemonContext(
            pidfile=None if not args.pidfile else \
                    TimeoutPIDLockFile(args.pidfile, acquire_timeout=-1),
            files_preserve=[None if not logfile_handler else \
                                    logfile_handler.stream.fileno()],
        ):
            _run_translator(config)
    else:
        _run_translator(config)


def _apply_logger_config(config: Config, args: argparse.Namespace):
    # Apply the config settings to logger system

    class Filter(logging.Filter):
        """Performs our custom filtering."""

        def __init__(self, config: Config, verbose: bool):
            super().__init__()
            self._config = config
            self._verbose = verbose

        def filter(self, record: logging.LogRecord) -> bool:
            """Determine if record meets minimum severity level."""
            if self._verbose:
                return record.levelno >= logging.DEBUG
            for namespace in self._config.logger.namespaces.items():
                if record.name.startswith(namespace[0]):
                    return record.levelno >= namespace[1].value
            return record.levelno >= self._config.logger.default.value

    # Reset level on root logger
    logger = logging.getLogger('')
    logger.setLevel(logging.NOTSET)

    # Add filter to all handlers
    for handler in logging.root.handlers:
        handler.setLevel(logging.NOTSET)
        handler.addFilter(Filter(config, args.verbose))


def _run_translator(config: Config) -> None:
    # Call function to run translator, wrapped in an event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            _async_run_translator(config))
    except KeyboardInterrupt:
        pass
    except Exception: # pylint: disable=broad-except
        _LOGGER.exception("Exiting due to unhandled exception")
    finally:
        loop.close()


async def _async_run_translator(config: Config) -> None:
    # Translate messages between the LifeSOS and MQTT interfaces;
    # runs indefinitely until user cancels or kill signal received
    translator = Translator(config)
    await translator.async_start()
    try:
        await translator.async_loop()
    finally:
        await translator.async_stop()


def _list_devices(config: Config) -> None:
    # Call function to list all devices, wrapped in an event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            _async_list_devices(config))
    except KeyboardInterrupt:
        pass
    except Exception: # pylint: disable=broad-except
        _LOGGER.exception("Exiting due to unhandled exception")
    finally:
        loop.close()


async def _async_list_devices(config: Config) -> None:
    # List all devices enrolled on the base unit
    from lifesospy.command import GetDeviceByIndexCommand
    from lifesospy.devicecategory import DC_ALL
    from lifesospy.response import DeviceInfoResponse

    protocol = await _async_new_protocol(config)
    try:
        print("Listing devices...")
        count = 0
        for category in DC_ALL:
            if category.max_devices:
                for index in range(0, category.max_devices):
                    response = await protocol.async_execute(
                        GetDeviceByIndexCommand(category, index))
                    if not isinstance(response, DeviceInfoResponse):
                        break
                    print("DeviceID '{:06x}' for {} zone {}, a {}.".
                          format(response.device_id,
                                 response.device_category.description,
                                 response.zone, str(response.device_type)))
                    count += 1
        print("{} devices were found.".format(count))
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
