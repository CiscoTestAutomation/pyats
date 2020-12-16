.. _connection_integration:

Integration
===========


The integration of connection module's :ref:`connection_manager` and topology
:ref:`Device object<topology_device_object>` is based off a relatively
simple & straight-forward concept: 

    *When given a Device object, users should be able to directly interface
    (eg, connect, send/receive commands) with the actual device, without having 
    to consciously involve anything else.*

.. code-block:: python

    # Example
    # -------
    #
    #   device & connection integration

    # when given a device object
    device = testbed.devices['some-uut-device']

    # users should be able to directly interface with it, eg:
    # connect to it
    device.connect()

    # send commands
    output = device.execute('show version')
    device.configure('''
        interface Ethernet1/1
            ip address 192.5.10.1 255.255.255.0
            no shutdown
    ''')

    # and more ...
    assert device.connected
    device.ping('192.5.10.2')
    device.reload()
    device.disconnect()

.. tip::

    For the sake of verbal simplicity, each connection (eg, telnet to console), 
    shall be referred to as a *connection instance* here forward.


.. _connection_single_instance:

Single Instance
---------------

The most simplistic usage scenarios of connections is to just open a *single*
connection instance to a testbed device. To do so, simply invoke the
``Device.connect()`` method directly. From there on, all services associated 
with that device should just show up directly as methods of that object 
instance:

.. code-block:: text

    Syntax
    ------

        # [] denotes optional arguments
        # *args, **kwargs denotes all other possible arguments

        # connect & disconnect
        device.connect([via = "path"], [**kwargs])
        device.disconnect()

        # calling services
        device.<services>([*args], [**kwargs])


.. code-block:: python

    # Example
    # -------
    #
    #   simplistic connection example 

    # using the topology module
    from pyats import topology

    # let's write an inline testbed file for simplicity
    # (edit this to whatever your testbed looks like)
    testbed = topology.loader.load('''
    testbed:
        name: my-inline-testbed

    devices:
        tplana-hath:
            type: iosxe
            os: iosxe
            connections:
                a:
                    protocol: telnet
                    ip: 10.1.1.1
                    port: 10000
    ''')

    # pick the device to work with
    device = testbed.devices['tplana-hath']

    # we should be able to directly connect to it
    device.connect()
    assert device.connected

    # run the various services associated with this connection
    device.execute('show version')
    device.configure('clock set 18:00:00 April 4 2063')

    # disconnect from it
    device.disconnect()

.. tip::

    keep in mind that connection library is oblivious to what type of connection
    is being opened up or where it is connecting to. Eg, in single connection
    instances, the opened session could be either console or mgmt/vty.


Multiple Instance
-----------------

When opening multiple connection instances, each connection must be provided 
with its own unique alias for identification purposes:

.. code-block:: text

    Syntax
    ------

        # [] denotes optional arguments
        # *args, **kwargs denotes all other possible arguments

        # connect to alias and disconnect from alias
        device.connect(alias = "alias", [via = "path"], [**kwargs])
        device.<alias>.disconnect()

        # calling services of an alias
        device.<alias>.<services>([*args], [**kwargs])


.. code-block:: python

    # Example
    # -------
    #
    #   multiple connection instance example 

    # following the example above, let's make the testbed
    # connection description slightly more complicated
    # (edit this to whatever your testbed looks like)
    testbed = topology.loader.load('''
    testbed:
        name: my-inline-testbed

    devices:
        tplana-hath:
            type: iosxe
            os: iosxe
            connections:
                a:
                    protocol: telnet
                    ip: 10.1.1.1
                    port: 10000
                mgmt:
                    protocol: telnet
                    ip: 10.1.1.1
                    port: 20000
    ''')

    # pick the device
    device = testbed.devices['tplana-hath']

    # make multiple connections to mgmt port (which accepts multi sessions)
    # each should be provided a unique alias and the exact path eg:
    device.connect(alias = 'vty_1', via = 'mgmt')
    device.connect(alias = 'vty_2', via = 'mgmt')
    device.connect(alias = 'vty_3', via = 'mgmt')

    # now we can use each instance independent of the others
    assert device.vty_1.connected
    assert device.vty_2.connected
    assert device.vty_3.connected

    # each instance has its own services
    # eg, configure different terminal width for each session
    device.vty_1.configure('terminal width 100')
    device.vty_2.configure('terminal width 200')
    device.vty_2.configure('terminal width 300')

    # disconnect each independently 
    device.vty_1.disconnect()
    device.vty_2.disconnect()
    device.vty_3.disconnect()

    # or disconnect everything altogether
    device.disconnect_all()

.. warning::

    alias names may not contain characters such as ``-``, ``.``, ``\`` etc. It 
    may only contain valid python attribute identifiers: ``[a-z], [A-Z], [0-9], 
    _``.

When ``device.connect()`` is called without the ``alias`` argument (eg, 
:ref:`connection_single_instance`), a default alias is used:

.. code-block:: python

    # Example
    # -------
    #
    #   default alias is "default"

    # in the case of single connections above
    device.connect()

    # you only get ONE connection, and
    # this connection bears the alias "default", eg:
    device.execute('show clock')

    # is the exact same as:
    device.default.execute('show clock')


When creating and handling multiple connections, always keep in mind that 
whilst you may establish multiple connections to the same device, the underlying
router/device resources are still shared, and thus changes (eg, configs) may be
applied *globally* (depending on what it was), and affect all your connection
instances.

.. tip::

    multiple connection instances start to make sense when you want to perform
    many ``show`` commands at the same time through asychronous means (eg, 
    multiprocessing, threading, etc).

