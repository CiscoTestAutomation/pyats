Creating Topology
=================

There are two ways to create a topology within your testscript:

    #. create each testbed object from ``topology`` module classes and craft
       their interconnects together manually (eg, by assigning interfaces to
       each device).

    #. create a YAML testbed description file, and load it using the
       topology loader function.

.. tip::

    Unless you need to create topology on the fly, the better
    option is always to use YAML files to specify your topology.

.. hint::

    You can pass in a testbed YAML to ``pyats run job`` using the
    ``--testbed-file`` option, which automatically invokes
    ``topology.loader`` to load the YAML file and pass the testbed object to
    your script. The value following ``--testbed-file`` can be a file path or 
    a URL.

.. _topology_testbed_file:

Testbed File
------------

Most users will most likely be running their
testscripts using a *testbed file* as input, and relying on the loader to
convert the YAML description into testbed objects.

.. code-block:: bash

    # Examples
    # --------
    #
    #   starting scripts using pyats run job and passing in testbed file/url
    #   using --testbed-file argument

    pyats run job jobfile.py --testbed-file /path/to/my/testbed/file/testbed.yaml
    
    pyats run job jobfile.py --testbed-file "https://<url>/testbed.yaml"

Easypy then invokes ``topology`` module to load and convert this
information into topology object instances, and pass it to the user script.
For example, in :ref:`aetest<aetest_jobfile_execution>` the provided
testbed object is accessible using the ``testbed`` parameter.

Internally, the following is really what happened:

.. code-block:: python

    # Details
    # -------
    #
    #   how testbed file was loaded into testbed object

    from pyats.topology import loader

    # load testbed file
    testbed = loader.load('/path/to/my/testbed/file/testbed.yaml')

    # voila!

``topology.loader.load()`` API takes in a loadable input (such as path to a YAML
testbed file or a URL to a YAML testbed file), parses the information, and makes 
appropriate Class constructor calls to construct the corresponding objects, 
including building the topology interconnect relationships.

Testbed files need to follow the standard testbed-file format (a.k.a schema).
The :ref:`schema` controls how and what information can go into each testbed
file, and provides standard best practices so that testbed description is
unanimous for all.

.. note::

    when ``topology.loader`` loads a testbed file, if the testbed name is not
    specified within ``testbed:`` section, the loader substitutes the file name
    as the testbed name, with prefix/post-fix such as ``CONFIG.`` and ``.yaml``
    trimmed.

.. tip::

    there may be cases where users wishes to perform their own loading of
    the testbed file, or in rare cases, deal with more than one testbed at a
    time per script. In those cases, use the ``topology.loader.load()`` API to
    facilitate the conversion of testbed file to objects.

.. _testbed_file_markups:

Testbed File Markups
--------------------

See :ref:`yaml_file_markup`


Manual Creation
---------------

If needed, you can always create and/or manipulate testbed objects manually.
This is the better option when you need to add or remove testbed components
on the fly.

.. code-block:: python

    # Example
    # -------
    #
    #   creating a simple testbed topology from scratch

    # import testbed objects
    from pyats.topology import Testbed, Device, Interface, Link

    # create your testbed
    testbed = Testbed('manuallyCreatedTestbed',
                      alias = 'iWishThisWasYaml',
                      passwords = {
                        'tacacs': 'lab',
                        'enable': 'lab',
                      },
                      servers = {
                        'tftp': {
                            'name': 'my-tftp-server',
                            'address': '10.1.1.1',
                        },
                      })

    # create your devices
    device = Device('tediousProcess',
                    alias = 'gimmyYaml',
                    connections = {
                        'a': {
                            'protocol': 'telnet',
                            'ip': '192.168.1.1',
                            'port': 80
                        }
                    })

    # create your interfaces
    interface_a = Interface('Ethernet1/1',
                            type = 'ethernet',
                            ipv4 = '1.1.1.1')
    interface_b = Interface('Ethernet1/2',
                            type = 'ethernet',
                            ipv4 = '1.1.1.2')

    # create your links
    link = Link('ethernet-1')

    # now let's hook up everything together
    # define the relationship.
    device.testbed = testbed
    device.add_interface(interface_a)
    device.add_interface(interface_b)
    interface_a.link = link
    interface_b.link = link

Note that in the example above, a very simple testbed of one device and two
interface connected in a loopback configuration is performed. We also gave it
some information w.r.t. how to connect to it, as well as interface ip and tftp
information. Before we bore you out - this didn't even use up half the available
properties and arguments to creating each testbed object. The point is to show
you that it can be done, though a bit tedious.

Note also that the above approach chose to create all objects first, and then
connecting them together after. You can also choose to do it dynamically, for
example, creating ``Device`` objects and using its ``interfaces`` argument to
pass in its interface objects from the start. As well, all object properties,
such as ``Testbed.tacacs``, can be updated/changed after object is created.

.. hint::

    testbed object creation should be automatable quite easily. you can write
    your own loader classes to do the load of your own custom testbed files.
