.. _topology_concept:

Everything is an Object
=======================

As opposed to creating a module where the topology information is stored
internally, and asking users to query that information via API calls, pyATS 
``topology`` module approached the design from a completely different angle:

    - using objects to represent real-world testbed devices

    - using object attributes & properties to store testbed information and
      meta-data

    - using object relationships (references/pointers to other objects) to
      represent topology interconnects

    - using object references & python garbage collection to clean up testbed
      left-overs when objects are no longer referenced.

The text graph below should give a good high-level pictorial view of how
``topology`` objects are referenced & interconnected.

.. code-block:: text

    +--------------------------------------------------------------------------+
    | Testbed Object                                                           |
    |                                                                          |
    | +-----------------------------+          +-----------------------------+ |
    | | Device Object - myRouterA   |          | Device Object - myRouterB   | |
    | |                             |          |                             | |
    | |         device interfaces   |          |          device interfaces  | |
    | | +----------+ +----------+   |          |   +----------+ +----------+ | |
    | | | intf Obj | | intf Obj |   |          |   |  intf Obj| | intf Obj | | |
    | | | Eth1/1   | | Eth1/2 *-----------*----------*  Eth1/1| | Eth1/2   | | |
    | | +----------+ + ---------+   |     |    |   +----------+ +----------+ | |
    | +-----------------------------+     |    +-----------------------------+ |
    |                                     |                                    |
    |                               +-----*----+                               |
    |                               | Link Obj |                               |
    |                               |rtrA-rtrB |                               |
    |                               +----------+                               |
    +--------------------------------------------------------------------------+

.. _topology_objects:

Testbed Object
--------------

``Testbed`` object is the top container object, containing all testbed devices
and all subsequent information that is generic to the testbed.

    - within a testbed, links & device names must be unique

.. code-block:: text

    +--------------------------------------------------------------------------+
    | Testbed object                                                           |
    +==========================================================================+
    | attributes    | description                                              |
    |---------------+----------------------------------------------------------|
    | name          | testbed name, should be unique                           |
    | alias         | testbed alias, defaults to testbed name                  |
    | devices       | dict of testbed device (name:Device)                     |
    | tacacs        | dict of TACACS information common to the testbed         |
    | passwords     | dict of password information common to the testbed       |
    | credentials   | dict of credentials common to the testbed                |
    | servers       | dict of testbed server (name:dict). testbed servers are  |
    |               | those that services the entire testbed, such as ftp,     |
    |               | tftp and ntp servers.                                    |
    | clean         | dict of clean parameters (name:value). clean parameters  |
    |               | are those used to clean up (reload) testbed devices      |
    | custom        | dict of custom fields (name:value), non-standard testbed |
    |               | object meta-data goes here.                              |
    | testbed_file  | full path and name of the testbed file used to create    |
    |               | this testbed object (only available through YAML load)   |
    +==========================================================================+
    | properties    | description                                              |
    |---------------+----------------------------------------------------------|
    | links         | returns the set of unique Link objects connected to this |
    |               | testbed's device interfaces                              |
    +==========================================================================+
    | methods       | description                                              |
    |---------------+----------------------------------------------------------|
    | add_device    | adds a device (Device object) to this testbed            |
    | remove_device | removes a device (Device object) from this testbed       |
    | squeeze       | removes all unwanted devices, interfaces and links       |
    |               | from this testbed                                        |
    | connect       | connects to all or multiple devices in the testbed       |
    |               | in parallel together                                     |
    | disconnect    | disconnects all or multiple devices in the testbed       |
    |               | in parallel together                                     |
    | destroy       | destroys all or multiple device connections in the       |
    |               | testbed in parallel together                             |
    | execute       | executes commands against all or multiple devices in the |
    |               | testbed in parallel together                             |
    | configure     | configures commands against all or multiple devices in   |
    |               | the testbed in parallel together                         |
    | parse         | parse commands against all or multiple devices in the    |
    |               | testbed in parallel together                             |
    +==========================================================================+

.. code-block:: python

    # Example
    # -------
    #
    #   creating testbed objects

    from pyats.topology import Testbed, Device

    # create some device objects for demonstration's sake
    device_a = Device('A')
    device_b = Device('B')
    device_c = Device('C')
    device_d = Device('D')

    # creating an empty testbed
    testbed_a = Testbed(name = 'emptyTestbed')

    # creating a testbed with an alias
    testbed_b = Testbed(name = 'myTestbed',
                        alias = 'yetAnotherTestbed')

    # creating a testbed with devices
    testbed_c = Testbed(name = 'testbedWithDevicesFromStart',
                        devices = [device_a, device_b])

    # adding devices into testbeds
    testbed_d = Testbed(name = 'testbedToReceiveDevices')
    testbed_d.add_device(device_c)

    # removing devices from a testbed
    testbed_e = Testbed(name = 'testbedToRemoveDevices',
                        devices = [device_d])
    testbed_e.remove_device(device_d)

    # squeezing a testbed to keep only wanted devices
    testbed_e = Testbed(name = 'testbedToSqueeze',
                        devices = [device_a, device_b, device_c])
    testbed_e.squeeze(device_b.name, device_c.name)

    # connect to all devices in this testbed in parallel
    testbed_e.connect()

    # connect to specific devices in this testbed in parallel
    # and optionally, use specific via paths
    testbed_e.connect(device_a, device_b,
                      via = {device_a.name: 'vty',
                             device_b.name: 'mgmt'})

    # testing whether testbed contains a device
    # use the "in" operator
    assert device_d not in testbed_e
    assert device_c in testbed_d

    # looping over a testbed's devices
    for device in testbed_c:
        print(device.name)

    # Setting default credentials on a testbed
    # Note that, once set, credentials may be accessed via dot notation.
    testbed_a.credentials['default'] = dict(username='defaultuser', password='defaultpw')
    assert testbed_a.credentials.default.username == 'defaultuser'

    # Setting credentials on a testbed
    # Note that, once set, credentials may be accessed via dot notation.
    testbed_a.credentials['tbcreds'] = dict(username='tbuser', password='tbpw')
    assert testbed_a.credentials.tbcreds.username == 'tbuser'

    # execute commands against all devices in parallel
    testbed.execute('show version')

    # configure all devices in the testbed in parallel
    testbed.configure('no logging console')

    # configure some devices in parallel
    # Note: devices is a list of Device objects
    devices = testbed.devices[dev] for dev in testbed.devices \
                    if testbed.devices[dev].os=='iosxe']
    testbed.configure('no logging console', devices=devices)

    # parse commands from all devices in the testbed in parallel
    testbed.parse('show version')

.. note ::
   Please see :ref:`secret_strings` for more details on how pyATS models
   credential passwords.

.. note ::
   Please see :ref:`topology_credential_password_modeling` for details on
   how credential passwords are modelled in the topology schema.

.. _topology_device_object:

Device Objects
--------------

``Device`` objects represent any piece of physical and/or virtual hardware that
constitutes an important part of a testbed topology.

    - each device may belong to a testbed (added to a ``Testbed`` object)

    - each device may host arbitrary number of interfaces (``Interface``
      objects)

    - interface names must be unique within a device

.. code-block:: text

    +--------------------------------------------------------------------------+
    | Device object                                                            |
    +==========================================================================+
    | attributes        | description                                          |
    |-------------------+------------------------------------------------------|
    | name              | device name (a.k.a hostname)                         |
    | alias             | device alias, defaults to device name                |
    | os                | device os such as iosxe, iosxr, nxos and etc
    | type              | device type (string)                                 |
    | testbed           | parent testbed object. internally this is a weakref  |
    | interfaces        | dict of device interfaces (name:Interface)           |
    | tacacs            | dict of TACACS information unique to this device     |
    | passwords         | dict of password information unique to the device    |
    | credentials       | dict of credentials for the device                   |
    | connections       | dict of connection descriptions (name:dict). this is |
    |                   | a description of connection methods to this device   |
    |                   | (eg: telnet, ssh, netconf & etc)                     |
    | connectionmgr     | connection manager (ConnectionManager obj), manages  |
    |                   | all the connections to this device                   |
    | clean             | dict of clean parameters (name:value). clean params  |
    |                   | are those used to clean up (reload) this device      |
    | custom            | dict of custom fields (name:value), non-standard     |
    |                   | device object meta-data goes here.                   |
    +==========================================================================+
    | properties        | description                                          |
    |-------------------+------------------------------------------------------|
    | links             | returns the set of unique Link objects connected to  |
    |                   | this device's interfaces                             |
    | remote_devices    | returns the set of unique devices connected to this  |
    |                   | device via its interface links                       |
    | remote_interfaces | returns the set of unique interfaces connected to    |
    |                   | this device's interfaces via interface links         |
    +==========================================================================+
    | methods           | description                                          |
    |-------------------+------------------------------------------------------|
    | add_interface     | adds an interface (Interface object) to this device  |
    | remove_interface  | removes an interface (Interface object) from this    |
    |                   | device                                               |
    | find_links        | find and return a set of links connected to the      |
    |                   | provided destination object (Device/Interface)       |
    +==========================================================================+


.. code-block:: python

    # Example
    # -------
    #
    #   creating device objects

    from pyats.topology import Testbed, Device, Interface

    # create some interfaces for adding to devices
    intf_a = Interface('Eth1/1', 'ethernet')
    intf_b = Interface('Eth2/1', 'ethernet')

    # creating a testbed for demonstration's sake
    testbed = Testbed('exampleTestbed')

    # creating an empty device
    device_a = Device('emptyDevice')

    # giving device a different alias
    device_a.alias = 'newAlias'

    # set device os
    device_a.os = 'iosxe'

    # creating a device with connection parameters
    device_b = Device('deviceThatCanBeConnected',
                      os='iosxe',
                      connections={
                          'mgmt': {
                              'protocol': 'telnet',
                              'ip': '1.1.1.1'
                          },
                      })

    # adding interface to device objects
    device_b.add_interface(intf_a)

    # creating device with interfaces
    device_c = Device('deviceCreatedWithIntfs',
                      os='iosxe',
                      interfaces = [intf_b])

    # associating a device to a testbed can be done either by performing
    # a testbed.add_device() call, or directly by setting a device's testbed
    # attribute, which automatically performs the parent add_device() call
    device_c.testbed = testbed

    # checking if an intf object belongs to a device can be done
    # using the in operator
    assert intf_b in device_c

    # loop through interfaces on a device
    for intf in device_c:
        print(intf.name)

    # Setting credentials on a device
    #
    # Testbed credentials may be read via device credentials
    # if they have not been defined at a device level and the device has
    # an assigned testbed.
    #
    # Once set, credentials may be accessed via dot notation.
    testbed.credentials['default'] = dict(username='defaultuser', password='defaultpw')
    assert testbed.credentials.default.username == 'defaultuser'

    testbed.credentials['tbcreds'] = dict(username='tbuser', password='tbpw')
    device_c.credentials['devcreds'] = dict(username='devuser', password='devpw')
    assert 'tbcreds' in device_c.credentials
    assert 'devcreds' in device_c.credentials

    # Missing credentials fall back to default credential if present
    assert testbed.credentials.unknowncred.username == 'defaultuser'

    # Although credential passwords are encoded and not directly readable
    # once set, it is possible to convert them back to plaintext.
    from pyats.utils.secret_strings import to_plaintext
    assert to_plaintext(device_c.credentials.devcreds.password) == 'devpw'

    # Setting credentials on a connection
    #
    # Device credentials may be read via connection credentials
    # if they have not been defined at a connection level.
    #
    # Testbed credentials may also be read via connection credentials
    # if they have not been defined at a device level and the device has an
    # assigned testbed.
    #
    # Once set, credentials may be accessed via dot notation.
    con = device_b.connections.mgmt
    device_b.testbed = testbed
    con.credentials['concreds'] = dict(username='connuser', password='conpw')
    assert 'tbcreds' in con.credentials
    assert 'concreds' in con.credentials

    # Provide a connection-level default credential
    con.credentials['default'] = dict(username='condefun', password='condefpw')


.. note ::
   Please see :ref:`secret_strings` for more details on how pyATS models
   credential passwords.

.. note ::
   Please see :ref:`topology_credential_password_modeling` for details on
   how credential passwords are modelled in the topology schema.

Interface Objects
-----------------

``Interface`` objects represent any piece of physical/virtual interface/port
that connects to a link of some sort. Eg: Ethernet, ATM, Loopback.

    - each interface connects to a single link (``Link`` object)

    - each interface should belong to a parent device (``Device`` object)

    - within a parent device, each interface name needs to be unique


.. code-block:: text

    +--------------------------------------------------------------------------+
    | Interface object                                                         |
    +==========================================================================+
    | attributes        | description                                          |
    |-------------------+------------------------------------------------------|
    | name              | interface name                                       |
    | alias             | interface alias, defaults to interface name          |
    | type              | interface type (string)                              |
    | device            | parent device object. internally this is a weakref   |
    | link              | link this interface is connected to (Link obj)       |
    | ipv4              | ipv4 address information (ipaddress.IPv4Interface)   |
    | ipv6              | ipv6 address information (ipaddress.IPv6Interface    |
    |                   | or a list of ipaddress.IPv6Interface)                |
    +==========================================================================+
    | properties        | description                                          |
    |-------------------+------------------------------------------------------|
    | remote_devices    | returns the set of unique devices connected to this  |
    |                   | interface via its connected link                     |
    | remote_interfaces | returns the set of unique interfaces connected to    |
    |                   | this interface via its connected link                |
    +==========================================================================+


.. code-block:: python

    # Example
    # -------
    #
    #   creating interface objects

    from pyats.topology import Device, Link
    # creating some objects to be used in demonstration
    device = Device('myDevice')
    link = Link('newlink')

    # create a simple interface
    interface_a = Interface('Ethernet1/1', type = 'ethernet')

    # create an interface that belongs to a device
    interface_b = Interface('Ethernet1/1',
                            type = 'ethernet',
                            device = device)

    # create another interface that belongs to another device
    # and also connected to a link
    interface_c = Interface('Ethernet2/1',
                            type = 'ethernet',
                            alias = 'myinterface',
                            link = link,
                            device = device)

    # manually connecting a link to an interface
    interface_b.link = link

    # manually assigning an interface to a device. this automatically
    # invokes device.add_interface() to keep the relationship consistent
    interface_a.device = device


Link Objects
------------

``Link`` objects represent the connection between two or more interfaces
within a testbed topology. Note that in the case of a link connected to more
than two interfaces, the link can also be interpreted as a layer-2 switch.

    - link names within a testbed must be unique

    - links may contain one or more interfaces (``Interface`` object)

.. code-block:: text

    +--------------------------------------------------------------------------+
    | Link object                                                              |
    +==========================================================================+
    | attributes           | description                                       |
    |----------------------+---------------------------------------------------|
    | name                 | link name                                         |
    | alias                | link alias, defaults to link name                 |
    | interfaces           | list of interfaces connected to this link. note   |
    |                      | that the interface objects are stored as weakrefs |
    +==========================================================================+
    | properties           | description                                       |
    |----------------------+---------------------------------------------------|
    | connected_devices    | returns the set of unique devices connected to    |
    |                      | this link                                         |
    +==========================================================================+
    | methods              | description                                       |
    |----------------------+---------------------------------------------------|
    | connect_interface    | adds an interface (Interface obj) to this link    |
    | disconnect_interface | removes an interface (Interface obj) from this    |
    |                      | link                                              |
    +==========================================================================+

.. code-block:: python

    # Example
    # -------
    #
    #   creating link objects

    from pyats.topology import Interface, Link
    # creating some objects to be used in demonstration
    interface_a = Interface('Ethernet1/1', type = 'ethernet')
    interface_b = Interface('Ethernet2/1', type = 'ethernet')
    interface_c = Interface('Ethernet2/1', type = 'ethernet')

    # creating an empty link
    link_a = Link('emptyLink')

    # creating a link with a few interface
    link_b = Link('newLink',
                  alias = 'myLink',
                  interfaces = [interface_a, interface_b])

    # adding interfaces to links
    link_b.connect_interface(interface_c)

    # check whether an interface obj is connected to a link
    # using the 'in' operator
    assert interface_c in link_b

    # loop through interfaces
    for intf in link_b:
        print(intf.name)
