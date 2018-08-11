Configuration
=============

All settings for this application's configuration file, ``config.yaml``, are listed below.

.. _configuration_lifesos:

LifeSOS settings
----------------

This section contains settings needed to interface with the LifeSOS base
unit / ethernet adapter.

.. code:: yaml

   # Settings for the LifeSOS interface
   lifesos:

     # Host and Port for the LifeSOS TCP Server to connect as a client,
     # or Port only to listen as a server for the LifeSOS TCP Client
     host: 192.168.1.100
     port: 1680

     # Master password, if needed by network interface
     password: ''

You will first need to determine whether your LifeSOS alarm system is
running in TCP SERVER or TCP CLIENT mode. Please refer to your manual if
unsure. This application is capable of supporting either mode, though
having LifeSOS in TCP SERVER MODE (ie. application will run as a client
and initiate connection) can make it easier to diagnose issues, as
connection failures will be logged.

If your LifeSOS ethernet adapter is configured in TCP SERVER mode:

-  **host**: The host name / IP address of your LifeSOS ethernet adapter
   to connect to.
-  **port**: The port number on your LifeSOS ethernet adapter.

If your LifeSOS ethernet adapter is configured in TCP CLIENT mode:

-  **host**: *Unused*; this line must be deleted or prefixed with a hash
   (ie. ``#host:``)
-  **port**: The port number to listen for incoming connections from
   LifeSOS.

Remaining settings are for either mode:

-  **password**: Master password, but **only if required by your LifeSOS
   system**. My old LS-30 doesn’t support it, but apparently it is a
   configurable setting on newer models to require a password to issue
   commands over the network interface.

.. _configuration_mqtt:

MQTT settings
-------------

This section contains settings needed to connect to your MQTT broker.

.. code:: yaml

   # Settings for the MQTT client
   mqtt:

     # URI providing the details needed to connect to the MQTT broker
     # Refer https://github.com/mqtt/mqtt.github.io/wiki/URI-Scheme
     uri: mqtt://username:password@127.0.0.1:1883

     # Server certificate authority file/path/data; only for secured connection (mqtts/wss)
     #cafile: /some/certfile
     #capath: /some/folder
     #cadata:

     # Unique client identifier; no need to change unless running multiple instances
     client_id: lifesos

-  **uri**: Provides the protocol, host name / IP address and port for
   the MQTT broker, and a username/password for login (if required).
-  **cafile**, **capath**, **cadata**: Optional settings used by HBMQTT
   on secure connections;
   `reference <http://hbmqtt.readthedocs.io/en/latest/references/mqttclient.html#hbmqtt.client.MQTTClient.connect>`__.
-  **client_id**: Name to identify this application to the MQTT broker.

.. _configuration_translator:

Translator settings
-------------------

This section contains settings used by the component responsible for
translating between the MQTT client and the LifeSOS ethernet adapter.

.. code:: yaml

   # Settings for the translator between LifeSOS and MQTT
   translator:

     # To automatically configure devices in Home Assistant, ensure this line
     # matches the setting in Home Assistant's config file. Note any devices and
     # switches will need to be assigned a 'ha_name"' to be exported.
     # Refer https://www.home-assistant.io/docs/mqtt/discovery/
     ha_discovery_prefix: homeassistant

     # Topic and Payload to announce Home Assistant has come online. When received,
     # our MQTT client will send out the device configurations for discovery.
     ha_birth_topic: homeassistant/status
     ha_birth_payload: online

     # Provide a topic for the Base Unit here
     baseunit:
       topic: home/alarm
       ha_name: "LifeSOS"

     # List your enrolled devices here and provide a topic
     # Hint: Run with '-e' option to get a list of device ids
     devices:
       #- device_id: '012cba'
       #  topic: home/remote
       #- device_id: '123abc'
       #  topic: home/lounge/motion
       #  auto_reset_interval: 180
       #  ha_name: "Lounge Motion"
       #  ha_name_rssi: "Lounge Motion RSSI"

     # Uncomment any switches you own and provide a topic
     switches:
       #- switch_number: 1
       #  topic: home/lounge/heater
       #  ha_name: "Lounge Heater"

Base Unit settings
^^^^^^^^^^^^^^^^^^

-  **topic**: The topic name for the base unit (alarm panel). Refer to
   the Topic section for more detail.

Device settings
^^^^^^^^^^^^^^^

Each enrolled device must have an entry here to link the unique device
identifier with a topic name. To determine the device identifier for
each device on your LifeSOS system, run ``lifesospy_mqtt -e``.

.. code-block:: text

   lifesospy_mqtt v0.10.1 - MQTT client to report state of LifeSOS security system and devices.

   Listing devices...
   DeviceID '123456' for Controller zone 01-01, a RemoteController.
   DeviceID '789abc' for Controller zone 01-02, a RemoteController.
   DeviceID 'def123' for Burglar zone 01-01, a PIRSensor.
   DeviceID '456789' for Burglar zone 01-02, a DoorMagnet.
   DeviceID 'abcdef' for Burglar zone 03-01, a PIRSensor.
   DeviceID 'fedcba' for Burglar zone 02-01, a PIRSensor.
   DeviceID '987654' for Burglar zone 04-01, a PIRSensor.
   DeviceID '321fed' for Burglar zone 04-02, a DoorMagnet.
   DeviceID 'cba987' for Special zone 04-03, a TempSensor.
   9 devices were found.

-  **device_id**: Unique identifier for the device you want to publish
   to the MQTT broker.
-  **topic**: The topic name for the device. Refer to the Topic section
   for more detail.
-  **auto_reset_interval**: all trigger-based sensors (like the PIR
   motion detector) only raise a single ``Trigger`` event when
   activated, not an ``On``/``Off`` binary state often needed by home
   automation software. This application will attempt to simulate a
   binary state by setting state to ``On`` when triggered, then reset to
   ``Off`` after this duration (in seconds) has elapsed. The default is
   30 seconds when no value specified.

Switch settings
^^^^^^^^^^^^^^^

Each switch you own must have an entry here to link the switch number
with a topic name.

-  **switch_number**: Number that identifies the switch on the base
   unit. Should be a value between 1 and 16.
-  **topic**: The topic name for the switch. Refer to the Topic section
   for more detail.

Home Assistant settings
^^^^^^^^^^^^^^^^^^^^^^^

Settings prefixed with ``ha_`` are for `Home
Assistant <https://www.home-assistant.io/>`__ support; specifically,
it’s `MQTT
Discovery <https://www.home-assistant.io/docs/mqtt/discovery/>`__
feature. If you are not intending to use this application with Home
Assistant, these settings can either be ignored or removed.

-  **ha_discovery_prefix**: the Home Assistant discovery prefix, as it
   is listed in the Home Assistant configuration.yaml file.
-  **ha_birth_topic**, **ha_birth_payload**: the topic and payload used
   by Home Assistant to notify when it has come online (`refer
   here <https://www.home-assistant.io/docs/mqtt/birth_will/>`__). This
   application will automatically send your LifeSOS configuration to
   Home Assistant when it receives this message.
-  **ha_name**: When this setting is listed under the device, it’s
   configuration will be exported to Home Assistant and the value will
   be used as the display name for the device.
-  **ha_name_rssi**: When this setting is listed under the device, the
   configuration needed to monitor the signal strength will be exported
   to Home Assistant, and the value will be used as the display name
   for the sensor.

Logger settings
---------------

This section contains settings to configure application logging.

.. code:: yaml

   # Settings to configure logging
   # Valid severity levels are:
   # critical, error, warning, info, debug
   logger:

     default: info

     #namespaces:
     #  lifesos: debug
     #  hbmqtt: debug

-  **default**: The default minimum severity level to log.
-  **lifesos**: Minimum severity level for any log entries generated
   directly from this application or the associated
   `LifeSOSpy <https://github.com/rorr73/LifeSOSpy>`__ library.
-  **hbmqtt**: Minimum severity level for any log entries generated from
   the `HBMQTT <https://github.com/beerfactory/hbmqtt>`__ library.
