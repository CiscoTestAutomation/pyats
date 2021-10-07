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

Another advantage of using testbed files is to leverage the built-in markup
feature. Whereas standard YAML format does not allow variable substitution and
references, ``topology.loader`` effectively added this using specific syntax
(markups) similar to the Django template language.

.. code-block:: text

    # Syntax
    # ------
    #
    #   YAML markup syntax

    # basic syntax
    # ------------
    #   %{<path>.<path>.<...>}
    #   %INTF{logical_interface_name}
    #   %ENV{environment_variable_name}
    #   %CALLABLE{path_to_callable}
    #   %CALLABLE{path_to_callable(param1,param2,param3)}
    #   %INCLUDE{yaml_file_path}
    #   %ASK{optional prompt text}
    #   %ENC{encoded text}
    #   %ENC{encoded text, prefix=x}
    #   %CLI(cli_argument_name}
    #
    #   - use %{ } to denote the begin and end of a markup block
    #   - use . to separate reference path
    #   - use 'self' as first word to reference current device
    #   - The %INTF{ } form causes the logical interface name to be
    #     replaced with the actual interface name from the
    #     device's topology block.
    #   - The %ENV{ } form causes the environment variable name to be
    #     replaced with the actual environment value from the os.
    #   - The %CALLABLE{ } form causes the callable to be replaced with the
    #     actual return value from the callable. All defined parameters
    #     will be passed to the callable.
    #   - The %INCLUDE{ } form causes the yaml file path to be replaced
    #     with the actual content of the yaml file.
    #   - The %ASK{ } form causes the user to be prompted to enter information
    #     manually.
    #   - The %ENC{ } form causes an encoded string to be replaced with a
    #     decoded string or secret string which supports decoding.
    #   - The %CLI{ } form replaces the variable name with the value provided
    #     from the command line argument. If no command line argument was
    #     provided for this variable, the value will be an empty string.
    #     Supports single and double dash argument style.

    # reference to current device name
    %{self}

    # reference to attributes within current device
    %{self.x.y.z}

    # reference to logical interface within current device
    # (replaced with actual interface name)
    %INTF{logical_interface_name}

    # reference to arbitrary attribute within this YAML file
    %{a.b.c}

    # reference to environment variable from the os
    # (replaced with actual environment variable name)
    %ENV{environment_variable_name}

    # reference to callable without parameter
    # (replaced with actual path to callable)
    %CALLABLE{path.to.callable}

    # reference to callable with parameters param1, param2 and param3
    # (replaced with actual path to callable)
    %CALLABLE{path.to.callable(param1,param2,param3)}

    # reference to content from other YAML file
    # (replaced with actual path to YAML file)
    %INCLUDE{yaml_file_path}

    # prompt user to enter string content manually
    %ASK{optional prompt text}

    # Reference to text encoded with "pyats secret encode" command
    # Encoded credential passwords are substituted by secret strings.
    # Other encoded references are substituted with their decoded string.
    # See secret strings documentation for details.
    %ENC{<encoded text>}

    # Reference to text encoded with "pyats secret encode --prefix x" command.
    # Encoded credential passwords are substituted by secret strings.
    # Other encoded references are substituted with their decoded string.
    # See secret strings documentation for details.
    %ENC{<encoded text>, prefix=x}

    # Reference to "some_arg" will be replaced by "some_value" if
    # the command line "pyats run job --some_arg some_value" is used.
    %CLI{some_arg}

    # If the command line argument is provided without a value,
    # the value is set to boolean 'True'. The following command line
    # sets the value for "some_flag" to True.
    # "pyats run job --some_flag"
    %CLI{some_flag}

    # If the command line argument has multiple values,
    # the variable is replaced with a list of values.
    # The following command line argument creates a list
    # of values in place of the devices variable.
    # "pyats run job --devices R1 R2"
    %CLI{devices}

    # If the command line argument contains a number value,
    # either integer or float, the variable is converted from
    # a string to an integer or float.
    # "pyats run job --retries 3"
    %CLI{retries}

.. note::

    Make sure to enclose your markup in quotes if it occurs directly
    after a colon.  For example::

        testbed:
            name: my_testbed

            passwords:
                enable: lab
                line: "%{testbed.passwords.enable}"
                tacacs: "%{testbed.passwords.enable}"
            tacacs:
                username: admin

YAML itself does not distinguish the markups from regular text (strings).
Before the creation of testbed objects, the loader walks through the generated
data and replaces all markup languages with referenced data.
Any syntax outside of the above is neither recognized nor processed.

.. code-block:: yaml

    # Example
    # -------
    #
    #   yaml testbed using markup
    #   notice how markups were used as information references.
    devices:
        example_device:
            type: "%CALLABLE{mylib.get_device_type}"
            connections:
              a:
                protocol: telnet
                ip: "1.1.1.1"
                port: 2001
              alt:
                protocol: telnet
                ip: "%{self.clean.mgt_itf.ipv4.address}"

        dynamic_device: "%CALLABLE{mylib.create_device(2.2.2.2)}"
    topology:
        example_device:
            interfaces:
                Ethernet4/6:
                    alias: my_logical_interface
                    link: link-x
                    type: "%ENV{DEFAULT_INTERFACE_TYPE}"
        dynamic_device: "%INCLUDE{/path/to/dynamic/generated/device/interfaces/file}"


Testbed file can be broken down in multiple yaml files with the extend key.
Each file can represent a subset of the main testbed file.


Let's say this file is named tb1.yaml

.. code-block:: yaml

    devices:
      xr-1:
        connections:
          cli:
            ip: 10.1.1.1
            protocol: ssh
        credentials:
          default:
            password: cisco
            username: cisco
          enable:
            password: cisco
        os: iosxr
        type: iosxr


And this file is named tb2.yaml

.. code-block:: yaml

  extends: tb1.yaml
  devices:
    xr-2:
      connections:
        cli:
          ip: 10.2.2.2
          protocol: ssh
      credentials:
        default:
          password: cisco
          username: cisco
        enable:
          password: cisco
      os: iosxr
      type: iosxr

Now at run time, you can provide the tb2.yaml, which will merge tb1.yaml and
tb2.yaml together to create a merged testbed.

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
