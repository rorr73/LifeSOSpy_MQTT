# LifeSOS MQTT Client

[![PyPI version](https://badge.fury.io/py/lifesospy-mqtt.svg)](https://badge.fury.io/py/lifesospy-mqtt)

This application provides an MQTT client that interfaces with
[LifeSOS](http://lifesos.com.tw) alarm systems, sensors and switches.
It will publish the state of all devices to an MQTT broker, which can
then be consumed by any application that provides MQTT support, such
as Home Assistant or OpenHAB. It will also subscribe to topics on the
broker that allow the control of the alarm system (eg. arm, disarm)
and turn on/off any attached switches.

It was written for & tested with the LS-30 model, though it should also
work on the LS-10/LS-20 models. Note that in some markets, they may also
be labelled under the name of the distributor; eg. SecurePro in
Australia, WeBeHome in northern Europe.

## Requirements

- A network-connected LifeSOS LS-30, LS-20 or LS-10 alarm system.
- Something to run this application on. Assuming you want to leave it
running 24/7, a low-powered device like a Raspberry Pi or a NAS are ideal.
- [Python 3.5.3 or higher](https://www.python.org/downloads/) must be
installed.
- An MQTT broker to connect to; eg. [Mosquitto](https://mosquitto.org/)

## Installation

To install this application, run the following command:

    $ pip install lifesospy_mqtt

After installation of the application (and dependencies) has completed,
you should be able to start the application using the `lifesospy_mqtt`
command. For now, just try displaying the help using the `-h` switch
to check it is installed correctly. It should look something like this:

```
lifesospy_mqtt v0.10.1 - MQTT client to report state of LifeSOS security system and devices.

usage: lifesospy_mqtt [-h] [-e] [-v] [-d] [-w WORKDIR] [-c CONFIGFILE]
                      [-l [LOGFILE]] [-p [PIDFILE]]

optional arguments:
  -h, --help            show this help message and exit
  -e, --devices         list devices enrolled on base unit and exit
  -v, --verbose         display all logging output.
  -d, --daemon          put the application into the background after starting
  -w WORKDIR, --workdir WORKDIR
                        work directory used to store config, log and pid files
                        (default: ~/.lifesospy_mqtt)
  -c CONFIGFILE, --configfile CONFIGFILE
                        configuration file name (default: config.yaml)
  -l [LOGFILE], --logfile [LOGFILE]
                        if specified, will write to a daily rolling log file
                        (default: None)
  -p [PIDFILE], --pidfile [PIDFILE]
                        if specified, file will be create to record the
                        process ID and is used for locking (default: None)
```

## Configuration

When you run the application for the first time, it will create a new
configuration file and exit.

```
lifesospy_mqtt v0.10.1 - MQTT client to report state of LifeSOS security system and devices.

A default configuration file has been created:
~\.lifesospy_mqtt\config.yaml

Please edit any settings as needed then restart.
```

Open up the new config file. The following sections will step you
through filling in the settings.

#### LifeSOS settings

This section contains settings needed to interface with the LifeSOS
base unit / ethernet adapter.

```yaml
# Settings for the LifeSOS interface
lifesos:

  # Host and Port for the LifeSOS TCP Server to connect as a client,
  # or Port only to listen as a server for the LifeSOS TCP Client
  host: 192.168.1.100
  port: 1680

  # Master password, if needed by network interface
  password: ''
```

You will first need to determine whether your LifeSOS alarm system is
running in TCP SERVER or TCP CLIENT mode. Please refer to your manual
if unsure. This application is capable of supporting either mode,
though having LifeSOS in TCP SERVER MODE (ie. application will
run as a client and initiate connection) can make it easier to
diagnose issues, as connection failures will be logged.

If your LifeSOS ethernet adapter is configured in TCP SERVER mode:

- **host**: The host name / IP address of your LifeSOS ethernet adapter to connect to.
- **port**: The port number on your LifeSOS ethernet adapter.


If your LifeSOS ethernet adapter is configured in TCP CLIENT mode:

- **host**: *Unused*; this line must be deleted or prefixed with a hash (ie. `#host:`)
- **port**: The port number to listen for incoming connections from LifeSOS.

Remaining settings are for either mode:

- **password**: Master password, but **only if required by your LifeSOS
system**. My old LS-30 doesn't support it, but apparently it is a
configurable setting on newer models to require a password to issue
commands over the network interface.

#### MQTT settings

This section contains settings needed to connect to your MQTT broker.

```yaml
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
```

- **uri**: Provides the protocol, host name / IP address and port for
the MQTT broker, and a username/password for login (if required).
- **cafile**, **capath**, **cadata**: Optional settings used by HBMQTT
on secure connections; [reference](http://hbmqtt.readthedocs.io/en/latest/references/mqttclient.html#hbmqtt.client.MQTTClient.connect).
- **client_id**: Name to identify this application to the MQTT broker.

#### Translator settings

This section contains settings used by the component responsible for
translating between the MQTT client and the LifeSOS ethernet adapter.

```yaml
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

  # Uncomment any switches you own and provide a topic
  switches:
    #- switch_number: 1
    #  topic: home/lounge/heater
    #  ha_name: "Lounge Heater"
```

##### Base Unit settings

- **topic**: The topic name for the base unit (alarm panel).
Refer to the Topic section for more detail.

##### Device settings

Each enrolled device must have an entry here to link the unique
device identifier with a topic name. To determine the device identifier
for each device on your LifeSOS system, run `lifesospy_mqtt -e`.

```
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
```

- **device_id**: Unique identifier for the device you want to publish
to the MQTT broker.
- **topic**: The topic name for the device. Refer to the
Topic section for more detail.
- **auto_reset_interval**: all trigger-based sensors (like the PIR
motion detector) only raise a single `Trigger` event when activated,
not an `On`/`Off` binary state often needed by home automation software.
This application will attempt to simulate a binary state by setting state
to `On` when triggered, then reset to `Off` after this duration (in seconds)
has elapsed. The default is 30 seconds when no value specified.

##### Switch settings

Each switch you own must have an entry here to link the switch number
with a topic name.

- **switch_number**: Number that identifies the switch on the base unit.
Should be a value between 1 and 16.
- **topic**: The topic name for the switch. Refer to the
Topic section for more detail.

##### Home Assistant settings

Settings prefixed with `ha_` are for [Home Assistant](https://www.home-assistant.io/)
support; specifically, it's [MQTT Discovery](https://www.home-assistant.io/docs/mqtt/discovery/)
feature. If you are not intending to use this application with Home
Assistant, these settings can either be ignored or removed.

- **ha_discovery_prefix**: the Home Assistant discovery prefix, as it is
listed in the Home Assistant configuration.yaml file.
- **ha_birth_topic**, **ha_birth_payload**: the topic and payload used
by Home Assistant to notify when it has come online
([refer here](https://www.home-assistant.io/docs/mqtt/birth_will/)). This
application will automatically send your LifeSOS configuration to Home
Assistant when it receives this message.
- **ha_name**: When this setting is listed under the device, it's
configuration will be exported to Home Assistant and the value will be
used as the display name for the device.

#### Logger settings

This section contains settings to configure application logging.

```yaml
# Settings to configure logging
# Valid severity levels are:
# critical, error, warning, info, debug
logger:

  default: info

  #namespaces:
  #  lifesos: debug
  #  hbmqtt: debug
```

- **default**: The default minimum severity level to log.
- **lifesos**: Minimum severity level for any log entries generated
directly from this application or the associated
[LifeSOSpy](https://github.com/rorr73/LifeSOSpy) library.
- **hbmqtt**: Minimum severity level for any log entries generated
from the [HBMQTT](https://github.com/beerfactory/hbmqtt) library.

## Topics

The topics published and subscribed to by this MQTT client are listed below.
In all cases, the parent topic name can be configured; the sub-topic names
and payloads are fixed to what is shown.

For maximum compatibility with other MQTT clients, all payloads are plain
text (UTF-8).

#### Base Unit Topics

**home/alarm** *Published*

Current state for the base unit. This is a superset of `operation_mode`; it
also takes into account the exit and entry delay. One of:

Value | Description
----- | -----------
`Disarm` | No burglar alarm will be triggered.
`Home` | Only perimeter sensors are armed; eg. outer doors, windows.
`Away` | All burglar sensors are armed.
`Monitor` | Disarmed, but triggered sensors will be logged; ie. for testing.
`AwayExitDelay` | Disarmed, but transitioning to Away mode after delay.
`AwayEntryDelay` | Burglar sensor triggered, delayed alarm pending.

**home/alarm/entry_delay** *Published*

When a burglar sensor is triggered, the base unit will wait this many seconds
before triggering the alarm (providing a brief window to disarm the system).

*Payload Example*: `15`

**home/alarm/exit_delay** *Published*

When the system is set to Away mode via a remote controller or keypad, it
will wait this many seconds before actually changing state (giving the owner
time to exit the premises).

*Payload Example*: `15`

**home/alarm/ha_state** *Published*

Provides the state of the base unit in a format recognised by Home Assistant's
`alarm_control_panel` platform. One of:

Value | Description
----- | -----------
`disarmed` | No burglar alarm will be triggered.
`armed_home` | Only perimeter sensors are armed; eg. outer doors, windows.
`armed_away` | All burglar sensors are armed.
`pending` | Pending mode change; ie. due to exit or entry delay.
`triggered` | Alarm has been triggered.

**home/alarm/is_connected** *Published*

Indicates if this LifeSOS MQTT client is operational and connected to the
base unit. One of: `True` or `False`.

**home/alarm/operation_mode** *Published*<br />**home/alarm/operation_mode/set** *Subscribed*

Gets or Sets the current operation mode. One of:

Value | Description
----- | -----------
`Disarm` | No burglar alarm will be triggered.
`Home` | Only perimeter sensors are armed; eg. outer doors, windows.
`Away` | All burglar sensors are armed.
`Monitor` | Disarmed, but triggered sensors will be logged; ie. for testing.

**home/alarm/rom_version** *Published*

Current ROM version reported by the Base Unit. May help in determining the
features available, and in diagnosing issues.

*Payload Example*: `02.4201/13/06`

**home/alarm/clear_status** *Subscribed*

When received, this application will clear the alarm/warning LEDs on base unit
and stop siren. No payload is required; it will be ignored.

**home/alarm/datetime/set** *Subscribed*

When received, the remote date/time will be set to the date/time specified in
the payload, or current local date/time if there is no payload.

This topic is useful when called periodically to fix drift and automatically
correct for Daylight Savings changes.

*Payload Example*: `2018-07-24-T13:57`

**home/alarm/event** *Published*

Details for an event when it occurs on the base unit. These are provided in
JSON format (if JSON is not available, refer `event_code` and `restore_code`
for an alternative).

Name | Description
---- | -----
`event_qualifier` | Context for the type of event. One of: `Event`, `Restore`, `Repeat`.
`event_category` | Category of event. One of: `Alarm`, `Supervisory`, `Trouble`, `OpenClose_Access`, `Bypass_Disable`, `Test_Misc`, `Automation`
`event_code` | Type of event. For a full list refer [here](https://github.com/rorr73/LifeSOSpy/blob/cae11d0d83190f873f2cdade9f8332797c558e9d/lifesospy/enums.py#L213).
`device_category` | Device category `code` and `description`, JSON encoded.
`zone` | Zone where the event occurred, if it originated from a device.
`user_id` | Unique identifier for user that generated the event, if any.

**home/alarm/event_code** *Published*<br />**home/alarm/restore_code** *Published*

Details for an event when it occurs on the base unit. Provided as an alternative
to the JSON version above, where JSON cannot be parsed by the MQTT client.

*Payload Example*: `ACPowerLoss`

#### Device Topics

**home/room/temp** *Published*

Current state for the device. The payload will depend on the type of device.

Type | Description
---- | -----------
Temperature | Temperature, in celcius.
Humidity | Humidity, as a percentage.
Light | Illuminance, as Lux.
AC Meter | Current, in amps.
Remote Control | Does not provide a state. Button press available through `event` topic only.
Keypad | Does not provide a state. Button press available through `event` topic only.
Magnet | One of: `Open`, `Closed`.
*Other* | Simulated only; *see below*. One of: `On`, `Off`.

Most sensors are trigger-based; eg. motion, window break, flood, gas, smoke, etc. These
do not normally provide a state; just a `Trigger` event when activated. Since most home
automation software requires a state, this application will attempt to simulate one by
providing `On` when triggered, and automatically reset to `Off` after a set duration.
By default, this is 30 seconds, although it can be customised via the configuration
setting `auto_reset_interval`.

Also note that motion sensors are designed to trigger as infrequently as possible, in
order to preserve battery life. After being triggered, they will not trigger again until
there has been no movement within the monitored area for at least 3 minutes. This can
make them unsuitable for home automation tasks, such as lighting an area when movement
is detected.

**home/room/temp/category/code** *Published*<br />**home/room/temp/category/description** *Published*

Code and Description for the category the device belongs to.

Code | Description
---- | -----------
`c` | `Controller` - eg. remote control, keypad.
`b` | `Burglar`- eg. magnet, motion, breakage sensors.
`f` | `Fire` - eg. smoke, gas, flood.
`m` | `Medical` - eg. medical wriststrap, emergency button.
`e` | `Special` - eg. temperature, humidity, light, power sensors.

**home/room/temp/device_id** *Published*

Unique identifier assigned to the device by the manufacturer.

*Payload Example*: `123abc`

**home/room/temp/rssi_db** *Published*

Wireless signal strength, in dB. Value in range between `0` to `100`.

**home/room/temp/rssi_bars** *Published*

Wireless signal strength, for visual representation as bars. Value in range between `0` and `4`.

**home/room/temp/type** *Published*

Type of device. A full list is available [here](https://github.com/rorr73/LifeSOSpy/blob/cae11d0d83190f873f2cdade9f8332797c558e9d/lifesospy/enums.py#L64).

*Payload Example*: `TempSensor`

**home/room/temp/zone** *Published*

Zone assigned to the device by the owner.

*Payload Example*: `04-03`

**home/room/temp/high_limit** *Published*<br />**home/room/temp/low_limit** *Published*

*-Only for devices in the `Special` category-*

Upper / Lower limit of allowable range; readings taken outside these limits will
trigger an alarm. When topic omitted or value is null, there is no limit.

*Example*: A temperature sensor with a `high_limit` of `40` will trigger a `HighTemp` alarm when the reading hits `41`.

**home/lounge/temperature/characteristics/Repeater** *Published*<br />
**home/lounge/temperature/characteristics/BaseUnit** *Published*<br />
**home/lounge/temperature/characteristics/TwoWay** *Published*<br />
**home/lounge/temperature/characteristics/Supervisory** *Published*<br />
**home/lounge/temperature/characteristics/RFVoice** *Published*

Device characteristics. Each property is `True` or `False` depending on whether the
characteristic is applies or not.

Name | Description
---- | -----------
`Repeater` | *TODO*
`BaseUnit` | *TODO*
`TwoWay` | Most devices are one-way transmitters. If `True`, this device is also capable of receiving messages from the base unit.
`Supervisory` | Device issues a `Heartbeat` event periodically, which can be used by the base unit to determine if the device is still functional.
`RFVoice` | *TODO*

**home/room/temp/switches/SW01** .. **SW16** *Published*

Switches that will be turned on when the device is triggered. One of: `True`, `False`.

**home/room/temp/enable_status/Bypass** *Published*<br />
**home/room/temp/enable_status/Delay** *Published*<br />
**home/room/temp/enable_status/Hour24** *Published*<br />
**home/room/temp/enable_status/HomeGuard** *Published*<br />
**home/room/temp/enable_status/WarningBeepDelay** *Published*<br />
**home/room/temp/enable_status/AlarmSiren** *Published*<br />
**home/room/temp/enable_status/Bell** *Published*<br />
**home/room/temp/enable_status/Latchkey** *Published*<br />
**home/room/temp/enable_status/Inactivity** *Published*<br />
**home/room/temp/enable_status/TwoWay** *Published*<br />
**home/room/temp/enable_status/Supervised** *Published*<br />
**home/room/temp/enable_status/RFVoice** *Published*<br />
**home/room/temp/enable_status/HomeAuto** *Published*

Behaviour setting on the base unit for the device. Each property is `True` or `False`
depending on whether the setting is enabled or not.

Name | Description
---- | -----------
`Bypass` | Ignore the alarm signal for device.
`Delay` | For controller devices, the `exit_delay` will be imposed on the Away button. For burglar devices, the `entry_delay` will be imposed on the burglar alarm signal.
`Hour24` | 24-Hour zone; the alarm signal will be processed regardless of operating mode.
`HomeGuard` | Alarm signal will be raised when in `Home` operating mode.
`WarningBeepDelay` | Issue warning beeps during `entry_delay` before alarm signalled.
`AlarmSiren` | Enable the siren when alarm triggered by device.
`Bell` | When in `Disarm` mode, triggering this burglar device will sound a door bell chime.
`Latchkey` | Pressing Disarm or Away on controller will phone the Latchkey number.
`Inactivity` | Burglar device is reassigned to be an inactivity sensor (eg. for monitoring the elderly). Instead of signalling a burglar alarm, it will signal a medical inactivity alarm.
`TwoWay` | *TODO*
`Supervised` | The base unit will listen for the periodic `Heartbeat` event sent from the device, and issue a warning when the device is no longer responding.
`RFVoice` | *TODO*
`HomeAuto` | *TODO*

**home/room/temp/special_status/ControlAlarm** *Published*<br />
**home/room/temp/special_status/HighLowOperation** *Published*<br />
**home/room/temp/special_status/HighTriggered** *Published*<br />
**home/room/temp/special_status/LowTriggered** *Published*<br />
**home/room/temp/special_status/HighState** *Published*<br />
**home/room/temp/special_status/LowState** *Published*

*-Only for devices in the `Special` category-*

Behaviour setting on the base unit for a `Special` device. Each property is `True` or `False`
depending on whether the setting is enabled or not.

Name | Description
---- | -----------
`ControlAlarm` | When `True`, the high/low limit is used only to control switches. When `False`, the limits are used to trigger an alarm.
`HighLowOperation` | When `True`, the high limit is enabled. When `False`, the low limit is enabled.
`HighTriggered` | *TODO*
`LowTriggered` | *TODO*
`HighState` | *TODO*
`LowState` | *TODO*

**home/room/temp/event_code** *Published*

Details for an event when it occurs on the device.

Name | Description
---- | -----------
Button | When button on the device is pressed.
Away | Away button on remote control / keypad.
Disarm | Disarm button on remote control / keypad.
Home | Home button on remote control / keypad.
Heartbeat | Sent periodically by device to the base unit, so it knows the device is still functional.
Reading | When a new reading has been taken by the `Special` devices.
PowerOnReset | Device powered on; eg. inserted new batteries.
BatteryLow | Device indicating the batteries are low and need to be replaced.
Open | When a magnet sensor is opened.
Close | When a magnet sensor is closed.
Tamper | When the device enclosure is tampered with.
Trigger | When a trigger-based device is activated.
Panic | Panic button on remote control / keypad.

#### Switch Topics

**home/room/switch** *Published*<br />**home/room/switch/set** *Subscribed*

Gets or Sets the current state of the switch. One of: `On`, `Off`.
