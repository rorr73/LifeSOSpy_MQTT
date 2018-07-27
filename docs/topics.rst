Topics
------

The topics published and subscribed to by this MQTT client are listed
below. In all cases, the parent topic name can be configured; the
sub-topic names and payloads are fixed to what is shown.

For maximum compatibility with other MQTT clients, all payloads are
plain text.

Base Unit Topics
^^^^^^^^^^^^^^^^

**home/alarm** *Published*

Current state for the base unit. This is a superset of
``operation_mode``; it also takes into account the exit and entry delay.
One of:

+--------------------+--------------------------------------------------+
| Value              | Description                                      |
+====================+==================================================+
| ``Disarm``         | No burglar alarm will be triggered.              |
+--------------------+--------------------------------------------------+
| ``Home``           | Only perimeter sensors are armed; eg. outer      |
|                    | doors, windows.                                  |
+--------------------+--------------------------------------------------+
| ``Away``           | All burglar sensors are armed.                   |
+--------------------+--------------------------------------------------+
| ``Monitor``        | Disarmed, but triggered sensors will be logged;  |
|                    | ie. for testing.                                 |
+--------------------+--------------------------------------------------+
| ``AwayExitDelay``  | Disarmed, but transitioning to Away mode after   |
|                    | delay.                                           |
+--------------------+--------------------------------------------------+
| ``AwayEntryDelay`` | Burglar sensor triggered, delayed alarm pending  |
+--------------------+--------------------------------------------------+

**home/alarm/entry_delay** *Published*

When a burglar sensor is triggered, the base unit will wait this many
seconds before triggering the alarm (providing a brief window to disarm
the system).

*Payload Example*: ``15``

**home/alarm/exit_delay** *Published*

When the system is set to Away mode via a remote controller or keypad,
it will wait this many seconds before actually changing state (giving
the owner time to exit the premises).

*Payload Example*: ``15``

**home/alarm/ha_state** *Published*

Provides the state of the base unit in a format recognised by Home
Assistant’s ``alarm_control_panel`` platform. One of:

+--------------------+--------------------------------------------------+
| Value              | Description                                      |
+====================+==================================================+
| ``disarmed``       | No burglar alarm will be triggered.              |
+--------------------+--------------------------------------------------+
| ``armed_home``     | Only perimeter sensors are armed; eg. outer      |
|                    | doors, windows.                                  |
+--------------------+--------------------------------------------------+
| ``armed_away``     | All burglar sensors are armed.                   |
+--------------------+--------------------------------------------------+
| ``pending``        | Pending mode change; ie. due to exit or entry    |
|                    | delay.                                           |
+--------------------+--------------------------------------------------+
| ``triggered``      | Alarm has been triggered.                        |
+--------------------+--------------------------------------------------+

**home/alarm/is_connected** *Published*

Indicates if this LifeSOS MQTT client is operational and connected to
the base unit. One of: ``True`` or ``False``.

| **home/alarm/operation_mode** *Published*
| **home/alarm/operation_mode/set** *Subscribed*

Gets or Sets the current operation mode. One of:

+--------------------+--------------------------------------------------+
| Value              | Description                                      |
+====================+==================================================+
| ``Disarm``         | No burglar alarm will be triggered.              |
+--------------------+--------------------------------------------------+
| ``Home``           | Only perimeter sensors are armed; eg. outer      |
|                    | doors, windows.                                  |
+--------------------+--------------------------------------------------+
| ``Away``           | All burglar sensors are armed.                   |
+--------------------+--------------------------------------------------+
| ``Monitor``        | Disarmed, but triggered sensors will be logged;  |
|                    | ie. for testing.                                 |
+--------------------+--------------------------------------------------+

**home/alarm/rom_version** *Published*

Current ROM version reported by the Base Unit. May help in determining
the features available, and in diagnosing issues.

*Payload Example*: ``02.4201/13/06``

**home/alarm/clear_status** *Subscribed*

When received, this application will clear the alarm/warning LEDs on
base unit and stop siren. No payload is required; it will be ignored.

**home/alarm/datetime/set** *Subscribed*

When received, the remote date/time will be set to the date/time
specified in the payload, or current local date/time if there is no
payload.

This topic is useful when called periodically to fix drift and
automatically correct for Daylight Savings changes.

*Payload Example*: ``2018-07-24-T13:57``

**home/alarm/event** *Published*

Details for an event when it occurs on the base unit. These are provided
in JSON format (if JSON is not available, refer ``event_code`` and
``restore_code`` for an alternative).

+--------------------+--------------------------------------------------+
| Name               | Description                                      |
+====================+==================================================+
| ``event_qualifier``| Context for the type of event. One of: ``Event``,|
|                    | ``Restore``, ``Repeat``.                         |
+--------------------+--------------------------------------------------+
| ``event_category`` | Category of event. One of: ``Alarm``,            |
|                    | ``Supervisory``, ``Trouble``,                    |
|                    | ``OpenClose_Access``, ``Bypass_Disable``,        |
|                    | ``Test_Misc``, ``Automation``                    |
+--------------------+--------------------------------------------------+
| ``event_code``     | Type of event. For a full list refer             |
|                    | `here <https://github.com/rorr73/LifeSOSpy/blob/ |
|                    | cae11d0d83190f873f2cdade9f8332797c558e9d/lifesos |
|                    | py/enums.py#L213>`__.                            |
+--------------------+--------------------------------------------------+
| ``device_category``| Device category ``code`` and ``description``,    |
|                    | JSON encoded.                                    |
+--------------------+--------------------------------------------------+
| ``zone``           | Zone where the event occurred, if it originated  |
|                    | from a device.                                   |
+--------------------+--------------------------------------------------+
| ``user_id``        | Unique identifier for user that generated the    |
|                    | event, if any.                                   |
+--------------------+--------------------------------------------------+

| **home/alarm/event_code** *Published*
| **home/alarm/restore_code** *Published*

Details for an event when it occurs on the base unit. Provided as an
alternative to the JSON version above, where JSON cannot be parsed by
the MQTT client.

*Payload Example*: ``ACPowerLoss``

Device Topics
^^^^^^^^^^^^^

**home/room/temp** *Published*

Current state for the device. The payload will depend on the type of
device.

+--------------------+--------------------------------------------------+
| Type               | Description                                      |
+====================+==================================================+
| Temperature        | Temperature, in celcius.                         |
+--------------------+--------------------------------------------------+
| Humidity           | Humidity, as a percentage.                       |
+--------------------+--------------------------------------------------+
| Light              | Illuminance, as Lux.                             |
+--------------------+--------------------------------------------------+
| AC Meter           | Current, in amps.                                |
+--------------------+--------------------------------------------------+
| Remote Control     | Does not provide a state. Button press available |
|                    | through ``event`` topic only.                    |
+--------------------+--------------------------------------------------+
| Keypad             | Does not provide a state. Button press available |
|                    | through ``event`` topic only.                    |
+--------------------+--------------------------------------------------+
| Magnet             | One of: ``Open``, ``Closed``.                    |
+--------------------+--------------------------------------------------+
| *Other*            | Simulated only; *see note below*. One of: ``On``,|
|                    | ``Off``.                                         |
+--------------------+--------------------------------------------------+

.. note::
    Most sensors are trigger-based; eg. motion, window break, flood, gas,
    smoke, etc. These do not normally provide a state; just a ``Trigger``
    event when activated. Since most home automation software requires a
    state, this application will attempt to simulate one by providing ``On``
    when triggered, and automatically reset to ``Off`` after a set duration.
    By default, this is 30 seconds, although it can be customised via the
    configuration setting ``auto_reset_interval``.

    Also note that motion sensors are designed to trigger as infrequently as
    possible, in order to preserve battery life. After being triggered, they
    will not trigger again until there has been no movement within the
    monitored area for at least 3 minutes. This can make them unsuitable for
    home automation tasks, such as lighting an area when movement is
    detected.

| **home/room/temp/category/code** *Published*
| **home/room/temp/category/description** *Published*

Code and Description for the category the device belongs to.

+-------+---------------------------------------------------------------+
| Code  | Description                                                   |
+=======+===============================================================+
| ``c`` | ``Controller`` - eg. remote control, keypad.                  |
+-------+---------------------------------------------------------------+
| ``b`` | ``Burglar``- eg. magnet, motion, breakage sensors.            |
+-------+---------------------------------------------------------------+
| ``f`` | ``Fire`` - eg. smoke, gas, flood.                             |
+-------+---------------------------------------------------------------+
| ``m`` | ``Medical`` - eg. medical wriststrap, emergency button.       |
+-------+---------------------------------------------------------------+
| ``e`` | ``Special`` - eg. temperature, humidity, light, power sensors.|
+-------+---------------------------------------------------------------+

**home/room/temp/device_id** *Published*

Unique identifier assigned to the device by the manufacturer.

*Payload Example*: ``123abc``

**home/room/temp/rssi_db** *Published*

Wireless signal strength, in dB. Value in range between ``0`` to
``100``.

**home/room/temp/rssi_bars** *Published*

Wireless signal strength, for visual representation as bars. Value in
range between ``0`` and ``4``.

**home/room/temp/type** *Published*

Type of device. A full list is available
`here <https://github.com/rorr73/LifeSOSpy/blob/cae11d0d83190f873f2cdade9f8332797c558e9d/lifesospy/enums.py#L64>`__.

*Payload Example*: ``TempSensor``

**home/room/temp/zone** *Published*

Zone assigned to the device by the owner.

*Payload Example*: ``04-03``

| **home/room/temp/high_limit** *Published*
| **home/room/temp/low_limit** *Published*

*-Only for devices in the* ``Special`` *category-*

Upper / Lower limit of allowable range; readings taken outside these
limits will trigger an alarm. When topic omitted or value is null, there
is no limit.

*Example*: A temperature sensor with a ``high_limit`` of ``40`` will
trigger a ``HighTemp`` alarm when the reading hits ``41``.

| **home/lounge/temperature/characteristics/Repeater** *Published*
| **home/lounge/temperature/characteristics/BaseUnit** *Published*
| **home/lounge/temperature/characteristics/TwoWay** *Published*
| **home/lounge/temperature/characteristics/Supervisory** *Published*
| **home/lounge/temperature/characteristics/RFVoice** *Published*

Device characteristics. Each property is ``True`` or ``False`` depending
on whether the characteristic is applies or not.

+--------------------+--------------------------------------------------+
| Name               | Description                                      |
+====================+==================================================+
| ``Repeater``       | *TODO*                                           |
+--------------------+--------------------------------------------------+
| ``BaseUnit``       | *TODO*                                           |
+--------------------+--------------------------------------------------+
| ``TwoWay``         | Most devices are one-way transmitters. If        |
|                    | ``True``, this device is also capable of         |
|                    | receiving messages from the base unit.           |
+--------------------+--------------------------------------------------+
| ``Supervisory``    | Device issues a ``Heartbeat`` event periodically,|
|                    | which can be used by the base unit to determine  |
|                    | if the device is still functional.               |
+--------------------+--------------------------------------------------+
| ``RFVoice``        | *TODO*                                           |
+--------------------+--------------------------------------------------+

**home/room/temp/switches/SW01** .. **SW16** *Published*

Switches that will be turned on when the device is triggered. One of:
``True``, ``False``.

| **home/room/temp/enable_status/Bypass** *Published*
| **home/room/temp/enable_status/Delay** *Published*
| **home/room/temp/enable_status/Hour24** *Published*
| **home/room/temp/enable_status/HomeGuard** *Published*
| **home/room/temp/enable_status/WarningBeepDelay** *Published*
| **home/room/temp/enable_status/AlarmSiren** *Published*
| **home/room/temp/enable_status/Bell** *Published*
| **home/room/temp/enable_status/Latchkey** *Published*
| **home/room/temp/enable_status/Inactivity** *Published*
| **home/room/temp/enable_status/TwoWay** *Published*
| **home/room/temp/enable_status/Supervised** *Published*
| **home/room/temp/enable_status/RFVoice** *Published*
| **home/room/temp/enable_status/HomeAuto** *Published*

Behaviour setting on the base unit for the device. Each property is
``True`` or ``False`` depending on whether the setting is enabled or
not.

+--------------------+--------------------------------------------------+
| Name               | Description                                      |
+====================+==================================================+
| ``Bypass``         | Ignore the alarm signal for device.              |
+--------------------+--------------------------------------------------+
| ``Delay``          | For controller devices, the ``exit_delay`` will  |
|                    | be imposed on the Away button. For burglar       |
|                    | devices, the ``entry_delay`` will be imposed on  |
|                    | the burglar alarm signal.                        |
+--------------------+--------------------------------------------------+
| ``Hour24``         | 24-Hour zone; the alarm signal will be processed |
|                    | regardless of operating mode.                    |
+--------------------+--------------------------------------------------+
| ``HomeGuard``      | Alarm signal will be raised when in ``Home``     |
|                    | operating mode.                                  |
+--------------------+--------------------------------------------------+
|``WarningBeepDelay``| Issue warning beeps during ``entry_delay``       |
|                    | before alarm signalled.                          |
+--------------------+--------------------------------------------------+
| ``AlarmSiren``     | Enable the siren when alarm triggered by device. |
+--------------------+--------------------------------------------------+
| ``Bell``           | When in ``Disarm`` mode, triggering this burglar |
|                    | device will sound a door bell chime.             |
+--------------------+--------------------------------------------------+
| ``Latchkey``       | Pressing Disarm or Away on controller will phone |
|                    | the Latchkey number.                             |
+--------------------+--------------------------------------------------+
| ``Inactivity``     | Burglar device is reassigned to be an inactivity |
|                    | sensor (eg. for monitoring the elderly). Instead |
|                    | of signalling a burglar alarm, it will signal a  |
|                    | medical inactivity alarm.                        |
+--------------------+--------------------------------------------------+
| ``TwoWay``         | *TODO*                                           |
+--------------------+--------------------------------------------------+
| ``Supervised``     | The base unit will listen for the periodic       |
|                    | ``Heartbeat`` event sent from the device, and    |
|                    | issue a warning when the device is no longer     |
|                    | responding.                                      |
+--------------------+--------------------------------------------------+
| ``RFVoice``        | *TODO*                                           |
+--------------------+--------------------------------------------------+
| ``HomeAuto``       | *TODO*                                           |
+--------------------+--------------------------------------------------+

| **home/room/temp/special_status/ControlAlarm** *Published*
| **home/room/temp/special_status/HighLowOperation** *Published*
| **home/room/temp/special_status/HighTriggered** *Published*
| **home/room/temp/special_status/LowTriggered** *Published*
| **home/room/temp/special_status/HighState** *Published*
| **home/room/temp/special_status/LowState** *Published*

*-Only for devices in the* ``Special`` *category-*

Behaviour setting on the base unit for a ``Special`` device. Each
property is ``True`` or ``False`` depending on whether the setting is
enabled or not.

+--------------------+--------------------------------------------------+
| Name               | Description                                      |
+====================+==================================================+
| ``ControlAlarm``   | When ``True``, the high/low limit is used only to|
|                    | control switches. When ``False``, the limits are |
|                    | used to trigger an alarm.                        |
+--------------------+--------------------------------------------------+
|``HighLowOperation``| When ``True``, the high limit is enabled. When   |
|                    | ``False``, the low limit is enabled.             |
+--------------------+--------------------------------------------------+
| ``HighTriggered``  | *TODO*                                           |
+--------------------+--------------------------------------------------+
| ``LowTriggered``   | *TODO*                                           |
+--------------------+--------------------------------------------------+
| ``HighState``      | *TODO*                                           |
+--------------------+--------------------------------------------------+
| ``LowState``       | *TODO*                                           |
+--------------------+--------------------------------------------------+

**home/room/temp/event_code** *Published*

Details for an event when it occurs on the device.

+--------------------+--------------------------------------------------+
| Name               | Description                                      |
+====================+==================================================+
| ``Button``         | When button on the device is pressed.            |
+--------------------+--------------------------------------------------+
| ``Away``           | Away button on remote control / keypad.          |
+--------------------+--------------------------------------------------+
| ``Disarm``         | Disarm button on remote control / keypad.        |
+--------------------+--------------------------------------------------+
| ``Home``           | Home button on remote control / keypad.          |
+--------------------+--------------------------------------------------+
| ``Heartbeat``      | Sent periodically by device to the base unit, so |
|                    | it knows the device is still functional.         |
+--------------------+--------------------------------------------------+
| ``Reading``        | When a new reading has been taken by the         |
|                    | ``Special`` devices.                             |
+--------------------+--------------------------------------------------+
| ``PowerOnReset``   | Device powered on; eg. inserted new batteries.   |
+--------------------+--------------------------------------------------+
| ``BatteryLow``     | Device indicating the batteries are low and need |
|                    | to be replaced.                                  |
+--------------------+--------------------------------------------------+
| ``Open``           | When a magnet sensor is opened.                  |
+--------------------+--------------------------------------------------+
| ``Close``          | When a magnet sensor is closed.                  |
+--------------------+--------------------------------------------------+
| ``Tamper``         | When the device enclosure is tampered with.      |
+--------------------+--------------------------------------------------+
| ``Trigger``        | When a trigger-based device is activated.        |
+--------------------+--------------------------------------------------+
| ``Panic``          | Panic button on remote control / keypad.         |
+--------------------+--------------------------------------------------+

Switch Topics
^^^^^^^^^^^^^

| **home/room/switch** *Published*
| **home/room/switch/set** *Subscribed*

Gets or Sets the current state of the switch. One of: ``On``, ``Off``.
