Changelog
=========

0.11.3
------

- Perform graceful shutdown when SIGTERM signal received (@bratanon)
- Fix issue where application doesn't shutdown immediately when signalled to exit.

.. @bratanon: https://github.com/bratanon

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
