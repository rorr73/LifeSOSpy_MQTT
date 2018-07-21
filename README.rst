LifeSOS MQTT Client
===================

This application provides an MQTT client that interfaces with `LifeSOS`_
alarm systems, sensors and switches. It will publish the state of all
devices to an MQTT broker, which can then be consumed by any application
that provides MQTT support, such as Home Assistant or OpenHAB. It will
also subscribe to topics on the broker that allow the control of the
alarm system (eg. arm, disarm) and turn on/off any attached switches.

It was written for & tested with the LS-30 model, though it should also
work on the LS-10/LS-20 models. Note that in some markets, they may also
be labelled under the name of the distributor; eg. SecurePro in
Australia, WeBeHome in northern Europe.

Requirements
------------

-  A network-connected LifeSOS LS-30, LS-20 or LS-10 alarm system.
-  Something to run this application on. Assuming you want to leave it
   running 24/7, a low-powered device like a Raspberry Pi or a NAS are
   ideal.
-  `Python 3.5.3 or higher`_ must be installed.
-  An MQTT broker to connect to; eg. `Mosquitto`_

Setting Up
----------

To install this application, run the following command:

::

   $ pip install lifesospy_mqtt

TODO…

.. _LifeSOS: http://lifesos.com.tw
.. _Python 3.5.3 or higher: https://www.python.org/downloads/
.. _Mosquitto: https://mosquitto.org/