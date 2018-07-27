LifeSOS MQTT Client
===================

.. image:: https://badge.fury.io/py/lifesospy-mqtt.svg
    :target: https://badge.fury.io/py/lifesospy-mqtt
.. image:: https://readthedocs.org/projects/lifesospy-mqtt/badge/?version=latest
    :target: http://lifesospy-mqtt.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

This application provides an MQTT client that interfaces with
`LifeSOS <http://lifesos.com.tw>`__ alarm systems, sensors and switches.
It will publish the state of all devices to an MQTT broker, which can
then be consumed by any application that provides MQTT support, such as
Home Assistant or OpenHAB. It will also subscribe to topics on the
broker that allow the control of the alarm system (eg. arm, disarm) and
turn on/off any attached switches.

It was written for & tested with the LS-30 model, though it should also
work on the LS-10/LS-20 models. Note that in some markets, they may also
be labelled under the name of the distributor; eg. SecurePro in
Australia, WeBeHome in northern Europe.

For a quickstart and configuration help, please refer to the `ReadTheDocs <http://lifesospy-mqtt.readthedocs.io>`__ site.
