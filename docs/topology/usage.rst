.. _topology_usage:

Using Topology Objects
======================

As previously indicated, topology objects are interconnected together via object
attributes & property references (pointers), representing the physical testbed
topology. This section provides more details on how this can be done.


Device Connection Manager
-------------------------

``Device`` class natively only contains the meta-data and the interconnect
information related to testbed device. For example, device ``connections``
attribute is simply a dictionary describing the many ways to connect to the
actual device it represent. With the help of ``ConnectionManager`` class,
``Device`` objects are effectively transformed into a compound object that both
handles the above, as well as the actual connections (Eg. telnet/ssh).

Each ``Device`` object is instantiated with a ``connectionmgr`` attribute that
contains an instance of ``ConnectionManager``, and contains all of the current
active connections to the managed device.

.. code-block:: python

    # Example
    # -------
    #
    #   connecting to device

    # using the sample topology file from
    import os
    from pyats import topology

    testbedfile = os.path.join(os.path.dirname(topology.__file__),
                               'sampleTestbed.yaml')
    testbed = topology.loader.load(testbedfile)

    # pick a device
    n7k5 = testbed.devices['ott-tb1-n7k5']

    # connect to it by calling connect()
    #   this is actually a ConnectionManager method. the compound object
    #   redirects the call to Device.connectionmgr.connect(), and:
    #       - defaults to using connection alias "default"
    #       - and creates the connection
    #
    #   in effect, this is the same as calling
    #       n7k5.connectionmgr.connect()
    n7k5.connect == n7k5.connectionmgr.connect
    # True
    n7k5.connect()
    n7k5.is_connected()
    # True

    # since the connection above is aliased with default
    # we can make calls to it directly.
    n7k5.default
    # ott-tb1-n7k5(default)
    n7k5.default.execute('show clock')
    # 00:56:54.569 EST Sat Mar 07 2015

    # default connections are also shortcut to the device level, so users
    # don't always have to type the default alias
    n7k5.execute == n7k5.default.execute == n7k5.connectionmgr.default.execute
    # True
    n7k5.execute('show clock')
    # 00:58:27.069 EST Sat Mar 07 2015

    # the connection manager is capable of handling multiple connections
    # each connection is referred to via its alias, and the connection object
    # is again compounded to be callable directly under the device object.
    # if supported, you can always create extra connections to
    # the same connection type, as long as this is supported by the device

    # creating a new connection to the alt (mgmt) connection definition
    # and calling it 'mgmt'. After connecting, you can make calls to it.
    n7k5.connect(alias = 'mgmt', via = 'alt')
    n7k5.mgmt.execute('show version')
    # ... etc

To summarize this behavior:

  - device connections are handled by a ``ConnectionManager`` instance, under
    ``device.connectionmgr`` attribute

  - device attributes are compounded with attributes of this connection manager.
    Eg. calling ``device.connect()`` is the same as calling
    ``device.connectionmgr.connect()``, and calling each connection using
    ``device.<alias>.execute()`` is the same as
    ``device.connectionmgr.<alias>.execute()``


For more details of the functionality of ``ConnectionManager`` instances, refer
to Connections Library documentation.

Connect To All Devices
----------------------

``Testbed`` object also provides a convenience function, ``Testbed.connect()``,
allowing you to establish asynchronous connection to multiple testbed devices 
at the same time.

.. code-block:: python

    # Example
    # -------
    #
    # connecting to devices in parallel

    # using the sample topology file from
    from pyats import topology

    testbedfile = os.path.join('sampleTestbed.yaml')
    testbed = topology.loader.load(testbedfile)

    # connect to all devices in this testbed
    testbed.connect()

    # connect to some devices in this testbed
    testbed.connect(testbed.devices['uut'], 
                    testbed.devices['helper'])

    # connect to some devices in this testbed
    # and provide unique vias
    testbed.connect(testbed.devices['uut'], 
                    testbed.devices['helper'],
                    vias = {'uut': 'cli',
                            'helper': 'console'})

    # connect to some devices in this testbed
    # using unique vias per device, and shared kwargs (eg, log_stdout = False)
    # shared keyword-arguments will be passed to every single connection
    testbed.connect(testbed.devices['uut'], 
                    testbed.devices['helper'],
                    vias = {'uut': 'cli',
                            'helper': 'console'},
                    log_stdout = False)

This is a convenience function, as under the hood it uses threads perform
per device ``.connect()`` asynchronously. All other behavior follows that of
the above connection manager concept. 

Disconnect From All Devices
----------------------

``Testbed`` object provides a convenience function, ``Testbed.disconnect()``,
allowing you to make asynchronous disconnection from multiple testbed devices
at the same time.

.. code-block:: python

    # Example
    # -------
    #
    # disconnecting from devices in parallel
    # using the sample topology file from
    from pyats import topology
    testbed = topology.loader.load('your-testbed-file.yaml')
    # connect to all devices in this testbed
    testbed.connect()
    # disconnect from all devices in this testbed
    testbed.disconnect()
    # disconnect from some devices in this testbed
    testbed.disconnect(testbed.devices['uut'],
                    testbed.devices['helper'])
    # disconnect from some devices in this testbed
    # and provide unique vias
    testbed.disconnect(testbed.devices['uut'],
                    testbed.devices['helper'],
                    vias = {'uut': 'cli',
                            'helper': 'console'})
    # disconnect from some devices in this testbed
    # using unique vias per device, and shared kwargs
    # shared keyword-arguments will be passed to every single connection
    testbed.disconnect(testbed.devices['uut'],
                    testbed.devices['helper'],
                    vias = {'uut': 'cli',
                            'helper': 'console'},
                            log_stdout = False)

This is a convenience function using threads under the hood to perform per
device ``.disconnect()`` asynchronously.

* After disconnecting from devices, the connection objects will remain,
and can be checked by command ``.conectionmgr.connections``, the same objects
will be used to connect to device again.

Destroy connections to all device
----------------------

``Testbed`` object provides ``Testbed.destroy()`` function, allowing you
to destroy connections asynchronously to multiple testbed devices. Unlike
``.disconnect()``, if ``.destroy()`` is used, then all connection objects
will be completely removed.

.. code-block:: python

    # Example
    # -------
    #
    # destroy devices in parallel
    # using the sample topology file from
    from pyats import topology
    testbed = topology.loader.load('your-testbed-file.yaml')

    # connect to all devices in this testbed
    testbed.connect()
    # destroy all devices in this testbed
    testbed.destroy()
    # destroy some devices in this testbed
    testbed.destroy(testbed.devices['uut'],
                    testbed.devices['helper'])
    # destroy some devices in this testbed
    # and provide unique vias
    testbed.destroy(testbed.devices['uut'],
                    testbed.devices['helper'],
                    vias = {'uut': 'cli',
                            'helper': 'console'})
    # destroy some devices in this testbed
    # using unique vias per device, and shared kwargs
    # shared keyword-arguments will be passed to every single connection
    testbed.destroy(testbed.devices['uut'],
                    testbed.devices['helper'],
                    vias = {'uut': 'cli',
                            'helper': 'console'},
                            log_stdout = False)

This is a convenience function using threads under the hood to perform
per device ``.destroy()`` asynchronously.

Querying Topology
-----------------

The basic concept is simple:

    - ``Testbed`` contains one or more ``Device``

    - ``Device`` contains zero or more ``Interface``

    - ``Interface`` may be connected to a ``Link``

    - ``Link`` connects one or more ``Interface`` together.

It may be useful to refer to :ref:`topology_concept` page for detailed object 
attributes and how everything is tailored together.

.. code-block:: python

    # Example
    # -------
    #
    #   topology querying

    import os

    # import the topology module
    from pyats import topology

    # load the sample testbed supplied as part of topology module
    # (example testbed file page for reference)
    testbedfile = os.path.join(os.path.dirname(topology.__file__),
                               'sampleTestbed.yaml')
    testbed = topology.loader.load(testbedfile)

    # confirming that this is indeed a testbed object
    type(testbed) is topology.Testbed
    # True

    # check that our expected devices are part of the testbed
    'ott-tb1-n7k4' in testbed and 'ott-tb1-n7k5' in testbed
    # True

    # access the actual device object from Testbed.devices attribute
    testbed.devices
    # AttrDict({'ott-tb1-n7k4': <Device ott-tb1-n7k4 at 0xf77190cc>,
    #           'ott-tb1-n7k5': <Device ott-tb1-n7k5 at 0xf744e16c>})

    # see how many links this testbed contains:
    for link in testbed.links:
        print(repr(link))
    # <Link rtr1-rtr2-1 at 0xf744d16c>
    # <Link rtr1-rtr2-2 at 0xf744ef8c>
    # <Link ethernet-1 at 0xf744ee8c>
    # <Link ethernet-2 at 0xf744efac>

    # grab both device
    n7k4 = testbed.devices['ott-tb1-n7k4']
    n7k5 = testbed.devices['ott-tb1-n7k5']

    # confirm that this is a Device object
    type(n7k4) is Device and type(n7k5) is Device
    # True

    # note that you can check whether devices exists in a testbed
    # by using either the device object or its name
    n7k4 in testbed and n7k5 in testbed
    # True

    # find the links connecting n7k5 from n7k4
    # using Device.find_links()
    for link in n7k4.find_links(n7k5):
        print(repr(link))
    # <Link rtr1-rtr2-2 at 0xf744ef8c>
    # <Link rtr1-rtr2-1 at 0xf744d16c>

    # loop through interfaces and find a interface that connects
    # to a particular link
    for intf in n7k4:
        if n7k5 in intf.remote_devices and intf.link.name == 'rtr1-rtr2-2':
            break
    else:
        intf = None

    # the entire topology is chained by attributes
    intf.link.interfaces
    # WeakList([<Interface Ethernet4/2 at 0xf744eeac>,
    #           <Interface Ethernet5/2 at 0xf744d74c>])
    intf.link.interfaces[1].device
    # <Device ott-tb1-n7k5 at 0xf744e16c>
    intf.link.interfaces[1].device.testbed
    # <pyats.topology.testbed.Testbed object at 0xf76b5f0c>
    intf.link.interfaces[1].device is n7k5
    # True

    # and all properties are computed on the fly
    n7k4.find_links(n7k4) & set(testbed.links)
    # <Link ethernet-1 at 0xf744ee8c>
    # <Link ethernet-2 at 0xf744efac>


Device & Interface Aliases
--------------------------

Every topology object is a subclass of ``TopologyObject`` base class: each one
comes with its own ``name`` (mandatory) and ``alias`` (optional, defaults to
``name``).

.. code-block:: python

    # Example
    # -------
    #
    #   Topology objects have names and aliases

    from pyats import topology

    # testbed object example
    testbed = Testbed('myTestbed')
    testbed.name
    # myTestbed
    testbed.alias
    # myTestbed

    # Link object example
    link = Link('myLink', alias = 'newLink')
    link.name
    # myLink
    link.alias
    # newLink

In an effort to abstract out hostnames/interfaces and allow users to reference
to testbed objects using their aliases (indirect access), ``Testbed.devices``
and ``Device.interfaces`` object attributes have been rigged to allow accesses
using aliases as an added feature.

.. code-block:: python

    # Example
    # -------
    #
    #   topology alias access

    # continuing to use the same sample topology file from
    # the previous example
    import os
    from pyats import topology

    testbedfile = os.path.join(os.path.dirname(topology.__file__),
                               'sampleTestbed.yaml')
    testbed = topology.loader.load(testbedfile)

    # testbed has alias
    testbed.alias
    # topologySampleTestbed

    # testbed devices have aliases
    testbed.devices['ott-tb1-n7k4'].alias
    # device-1
    testbed.devices['ott-tb1-n7k5'].alias
    # device-2

    # you can refer to devices within a testbed using its alias name instead
    # of the actual device name. this yields the same device object
    testbed.devices['device-1'] is testbed.devices['ott-tb1-n7k4']
    testbed.devices['device-2'] is testbed.devices['ott-tb1-n7k5']
    device_1 = testbed.devices['device-1']
    device_2 = testbed.devices['device-2']

    # device in testbed check also works using alias
    'device-1' in testbed.devices
    # True

    # testbed device interfaces also have aliases
    device_1.interfaces['Ethernet4/1'].alias
    # device1-intf1
    device_1.interfaces['Ethernet4/2'].alias
    # device1-intf2

    # same as devices in testbed, interface access in device can be
    # done using their aliases, including in operator
    device_1.interfaces['device1-intf1'] is device_1.interfaces['Ethernet4/1']
    True
    device_1.interfaces['device1-intf2'] is device_1.interfaces['Ethernet4/2']
    True
    'device1-intf1' in device_1.interfaces
    True

    # in addition, to test if something is an alias or not, use is_alias()
    device_1.interfaces.is_alias('device1-intf1')
    # True
    testbed.devices.is_alias('ott-tb1-n7k4')
    # False

Thus, as long as the testscript does not hard-code device and interface names,
and instead refers to them using aliases, the script would remain agnostic,
and run on any similarly configured testbeds with the same topology.

.. note::

    ``Link`` and ``Testbed`` also have aliases, but since they are not stored as
    ``MutableMappings`` like ``Testbed.devices`` and ``Device.interfaces``, they
    need to be accessed directly and tested for their alias instead. Example,
    ``if intf.link.alias == 'linkAlias'``.


Add, Modify & Delete
--------------------

Testbed objects are mutable and non-singletons. This means that at anytime, you
can modify their attributes & connection properties as needed. Keep in mind that
the following rules still apply:

    - Testbed device names must be unique (within the testbed)

    - Testbed link names must be unique (within the testbed)

    - Device interface names must be unique (within the device)

As well, because the topology is represented by physical relationships, their
contained objects move with them. Eg, if you move an interface object from one
device to another, the link that is connected to that interface moves with it.
Ditto for devices and their interfaces, etc.

.. code-block:: python

    # Example
    # -------
    #
    #   topology adding/deleting and modifying

    # continuing to use the same sample topology file from
    # the first example
    import os
    from pyats import topology

    testbedfile = os.path.join(os.path.dirname(topology.__file__),
                               'sampleTestbed.yaml')
    testbed = topology.loader.load(testbedfile)

    # add a new device
    # note - could also do this with
    #   topology.Device('myNewDevice', testbed = testbed)
    new_device = topology.Device('myNewDevice')
    testbed.add_device(new_device)
    testbed.devices
    # AttrDict({'ott-tb1-n7k5': <Device ott-tb1-n7k5 at 0xf76990cc>,
    #           'ott-tb1-n7k4': <Device ott-tb1-n7k4 at 0xf73ce2ac>,
    #           'myNewDevice': <Device myNewDevice at 0xf74aa78c>})

    # modify a testbed alias
    testbed.alias = 'newAlias'

    # add new interfaces (to existing device)
    n7k4 = testbed.devices['ott-tb1-n7k4']
    interface = topology.Interface('Ethernet9/40', 'ethernet')
    interface.link = topology.Link('newLink')
    n7k4.add_interface(interface)
    n7k4.interfaces
    # AttrDict({'Ethernet9/40': <Interface Ethernet9/40 at 0xf73ce98c>,
    #           'Ethernet4/45': <Interface Ethernet4/45 at 0xf73ce28c>,
    #           'Ethernet4/46': <Interface Ethernet4/46 at 0xf73ce36c>,
    #           'Ethernet4/2': <Interface Ethernet4/2 at 0xf73ce24c>,
    #           'Ethernet4/6': <Interface Ethernet4/6 at 0xf73ce18c>,
    #           'Ethernet4/7': <Interface Ethernet4/7 at 0xf73ce2ec>,
    #           'Ethernet4/1': <Interface Ethernet4/1 at 0xf73ce34c>})

    # modify device information
    n7k4.custom['newCustomInfo'] = 'new information that did not exist before'

    # removing interfaces
    n7k5 = testbed.devices['ott-tb1-n7k5']
    n7k5.remove_interface('Ethernet5/1')

    # now the number of connections changed:
    for link in n7k4.find_links(n7k5):
        print(repr(link))
    # <Link rtr1-rtr2-2 at 0xf73ce0ec>

    # let's create a new testbed and move n7k5 over to it.
    new_testbed = topology.Testbed('newTestbed')
    n7k5.testbed = new_testbed

    # notice how everything changed over
    n7k4.interfaces['Ethernet4/2'].link.interfaces[0].device
    # <Device ott-tb1-n7k5 at 0xf76990cc>
    n7k4.interfaces['Ethernet4/2'].link.interfaces[0].device.testbed.name
    # 'newTestbed'

    # since now link rtr1-rtr2-2 connects 2 testbeds, it is contained in
    # both sides
    link = n7k4.interfaces['Ethernet4/2'].link
    link in testbed.links and link in new_testbed.links
    # True

    # let's squeeze a topology
    # (reduce a topology to a wanted list of devices and/or links,
    # aliases are respected, interfaces not connected to wanted links
    # are removed):
    testbed = topology.loader.load(testbedfile)
    testbed.squeeze('device-1', 'rtr1-rtr2-1', extend_devices_from_links=True)
    [device.name for device in testbed]
    # ['ott-tb1-n7k4', 'ott-tb1-n7k5']
    [link.name for link in testbed.links]
    # ['rtr1-rtr2-1']
    [interface.name for interface in testbed.devices['device-1']]
    # ['Ethernet4/1']
    [interface.name for interface in testbed.devices['device-2']]
    # ['Ethernet5/1']



The above example may be elaborate (involving new testbeds), but is only used
as an example to show how everything works together. Attribute collection (such
as ``links``) is a combined iterative computation of parent/child relationships,
as shown above.

The simplest way to think about this relationship is to visualize it: if you
move a linecard from one device to another without disconnecting the cables
first, then the cables would follow through and be connected to interfaces of
that linecard on the new parent device. The same applies with topology objects.

References and Weak References
------------------------------

``topology`` module is designed to avoid circular object references (eg, devices
referring to parent testbed and testbed containing devices).

    - ``Testbed`` contains ``Device``

    - ``Device`` refer to parent testbed as a weak reference.

    - ``Device`` contain ``Interface``

    - ``Interface`` refer to parent device as a weak reference

    - ``Interface`` contains ``Link``

    - ``Link`` refer to their connected ``Interface`` as weak references

.. code-block:: python

    # Example
    # -------
    #
    #   demonstration of where weak references apply

    # import objects
    from pyats.topology import Testbed, Device, Interface, Link

    # create the objects
    testbed = Testbed('exampleTestbed')
    device = Device('exampleDevice')
    interface = Interface('exampleInterface', 'ethernet')
    link = Link('exampleLink')

    # hook up the relationship
    testbed.add_device(device)
    device.add_interface(interface)
    link.connect_interface(interface)

    # testbed contains devices as actual references
    testbed.devices
    # AttrDict({'exampleDevice': <Device exampleDevice at 0xf763c70c>})

    # device.testbed is internally stored as a weak reference to testbed,
    # even though it returns the actual testbed object
    testbed.device
    # <pyats.topology.testbed.Testbed object at 0xf763c6ac>

    # device.interfaces contains interfaces as actual references
    device.interfaces
    # AttrDict({'exampleInterface': <Interface exampleInterface at 0xf763c74c>})

    # interface.device is internally stored as a weak reference
    # even though it returns the actual device object
    interface.device
    # <Device exampleDevice at 0xf763c70c>

    # interface connects to links as an actual reference
    interface.link
    # <Link exampleLink at 0xf763ca8c>

    # links contain only weak references to interfaces
    # even though when you access it, it returns actual objects
    link.interfaces
    WeakList([<Interface exampleInterface at 0xf763c74c>])
    link.interfaces[0]
    # <Interface exampleInterface at 0xf763c74c>

Therefore, all rules of python garbage collection apply. For example, if you
dereference a device object entirely, all of its interface objects will be gone.
However, the only exception is ``Link`` objects: if more than one interface
connects to the same link, then unless all of those interfaces are removed, the
link will continue to exist.

.. code-block:: python

    # Example
    # -------
    #
    #   weak ref deletions

    # using the sample topology file from
    import os
    from pyats import topology

    testbedfile = os.path.join(os.path.dirname(topology.__file__),
                               'sampleTestbed.yaml')
    testbed = topology.loader.load(testbedfile)

    # let's see how many devices and links we started with
    testbed.devices
    # AttrDict({'ott-tb1-n7k4': <Device ott-tb1-n7k4 at 0xf73f712c>,
    #           'ott-tb1-n7k5': <Device ott-tb1-n7k5 at 0xf765ef0c>})
    testbed.links
    # {<Link rtr1-rtr2-2 at 0xf73fa58c>,
    #  <Link ethernet-2 at 0xf73f8fac>,
    #  <Link ethernet-1 at 0xf73f8b6c>,
    #  <Link rtr1-rtr2-1 at 0xf73fa4ec>}

    # now remove a device
    testbed.devices.pop('ott-tb1-n7k4')

    # look at devices and lists again in the testbed. it's all gone
    testbed.devices
    # AttrDict({'ott-tb1-n7k5': <Device ott-tb1-n7k5 at 0xf765ef0c>})
    testbed.links
    # {<Link rtr1-rtr2-2 at 0xf73fa58c>,
    #  <Link rtr1-rtr2-1 at 0xf73fa4ec>}

.. tip::

    if it's not cleaned up, something's holding it up. Likely you've stored a
    reference to that object or to its parent object somewhere else.

.. tip::

    read up on python garbage collection.


