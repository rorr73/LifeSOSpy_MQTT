Changelog
=========

0.11.0
------

- Changed the underlying MQTT client library from HBMQTT to Eclipse Paho, to reduce failures when reconnecting.
- Updated other dependent libraries.
- When a device is discovered that was not listed in the configuration file, log as warning and include device details.

0.10.6
------

- Added auto config for Home Assistant to show device signal strength.

0.10.5
------

- Documentation moved out of README into `ReadTheDocs <http://lifesospy-mqtt.readthedocs.io>`__.

0.10.4
------

- Fix published HA auto config entry for alarm_control_panel, ahead of adding support to HA.
