Changelog
=========

0.11.6
------

- Updated python-daemon dependency to 2.2.4 to resolve issue with starting in daemon mode under Python 3.8 - `#15 <https://github.com/rorr73/LifeSOSpy_MQTT/issues/15>`__ 

0.11.5
------

- Fix PIR sensor not automatically resetting motion state when auto_reset_interval defined in configuration file - `#13 <https://github.com/rorr73/LifeSOSpy_MQTT/issues/13>`__

0.11.4
------

- Added low battery binary sensor for devices - `#9 <https://github.com/rorr73/LifeSOSpy_MQTT/issues/9>`__ (@bratanon)
- Fixed a deprecation warning that may be shown when loading the configuration file with PyYAML 5.1 or higher - `#11 <https://github.com/rorr73/LifeSOSpy_MQTT/issues/11>`__ (@bratanon)

0.11.3
------

- Perform graceful shutdown when SIGTERM signal received - `#7 <https://github.com/rorr73/LifeSOSpy_MQTT/issues/7>`__ (@bratanon)
- Fix issue where application doesn't shutdown immediately when signalled to exit - `#8 <https://github.com/rorr73/LifeSOSpy_MQTT/issues/8>`__

0.11.2
------

- Fix issue where Home Assistant will not reset from Triggered state when the alarm was triggered in Disarm mode (eg. due to tampering, panic button, environmental).

0.11.1
------

- Fix issue where devices shown as Unavailable in Home Assistant when MQTT connection is lost and subsequently reconnected.

0.11.0
------

- Changed the underlying MQTT client library from HBMQTT to Eclipse Paho, to reduce failures when reconnecting.
- Updated other dependent libraries.
- When a device is discovered that was not listed in the configuration file, log as warning and include device details.
- Support alternative Away/Disarm event pattern used by more recent LifeSOS units.

0.10.6
------

- Added auto config for Home Assistant to show device signal strength.

0.10.5
------

- Documentation moved out of README into `ReadTheDocs <http://lifesospy-mqtt.readthedocs.io>`__.

0.10.4
------

- Fix published HA auto config entry for alarm_control_panel, ahead of adding support to HA.
