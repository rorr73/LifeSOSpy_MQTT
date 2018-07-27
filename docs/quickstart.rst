Quickstart
-------------

Step 1 - Installing the application
^^^^^^^^^^^^^^^^

To install, run the following command:

.. code-block:: console

   pip install lifesospy_mqtt

Step 2 - Generate a configuration file
^^^^^^^^^^^^^^^^

After installation of the application (and dependencies) has completed,
you will be able to start the application using the ``lifesospy_mqtt``
command.

When you run the application for the first time, it will create a new
configuration file and exit.

.. code-block:: text

   lifesospy_mqtt v0.10.5 - MQTT client to report state of LifeSOS security system and devices.

   A default configuration file has been created:
   ~\.lifesospy_mqtt\config.yaml

   Please edit any settings as needed then restart.

.. note::
    By default, the application will create a working directory ``.lifesospy_mqtt`` under
    your home directory. This will be used to hold the configuration file, along with any
    log files and a daemon locking file when needed. This behaviour can be overridden
    using command line arguments if desired.

Step 3 - Configure connection to your LifeSOS system
^^^^^^^^^^^^^^^^

Open up the new config file. For now, just fill out the settings in the
:ref:`LifeSOS <configuration_lifesos>` and :ref:`MQTT <configuration_mqtt>` sections.

Step 4 - Test connection and get list of devices
^^^^^^^^^^^^^^^^

Run ``lifesospy_mqtt -e`` to list all devices enrolled on your base unit. This will
also verify the application is able to connect to your LifeSOS system successfully.

.. code-block:: text

   lifesospy_mqtt v0.10.5 - MQTT client to report state of LifeSOS security system and devices.

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

Step 5 - Set up devices and topics
^^^^^^^^^^^^^^^^

Now that we know your LifeSOS settings are correct, go ahead and fill in
:ref:`Translator Settings <configuration_translator>` section of your config file.

For each device that you want to publish via MQTT, add an entry under ``devices``
with a ``device_id`` as listed during the above step, and specify a meaningful
``topic`` name. Also if you intend to use this MQTT client with Home Assistant,
specify a ``ha_name``, which is how the device will be labelled in the UI.

For each switch that you want to manage via MQTT, add an entry under ``switches``
with a ``switch number`` (value between 1 and 16) and specify a meaningful
``topic`` name. Again, if you intend to use this MQTT client with Home Assistant,
specify a ``ha_name``, which is how the switch will be labelled in the UI.

Step 6 - Run the application
^^^^^^^^^^^^^^^^

Go ahead and start the application by running ``lifesospy_mqtt``.

To verify data is being published to your MQTT broker, run the subscribe tool
that ships with it. For example, with Mosquitto:

.. code-block:: console

   mosquitto_sub -v -t 'home/alarm/#'

If this application is working correctly, you should see the data that was
published, similar to below:

.. code-block:: console

   home/alarm Disarm
   home/alarm/ha_state disarmed
   home/alarm/is_connected True
   home/alarm/operation_mode Disarm
   home/alarm/rom_version 02.4201/13/06
   home/alarm/exit_delay 15
   home/alarm/entry_delay 15

Step 7 - Run as a daemon (Optional)
^^^^^^^^^^^^^^^^

When you're happy that everything is working correctly, this application
can be set up to run as a daemon, to be run continuously in the background.

To do so, you will need to specify the ``-d`` command line argument. I'd
also recommend using the ``-l`` and ``-p`` arguments when running as a
daemon, to generate a log file and ensure only a single instance is running.
