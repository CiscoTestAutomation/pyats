
.. _yaml_file_markup:

YAML File Markups
=================

The pyATS YAML loader, which is used in several places including the testbed
loader, supports pyATS specific YAML markup.

Whereas standard YAML format does not allow variable substitution and
references, ``pyats.utils.yaml.Loader`` effectively added this using specific
syntax (markups) similar to the Django template language.

Reference
---------

.. code-block:: text

    # Syntax
    # ------
    #
    #   YAML markup syntax

    # basic syntax
    # ------------
    #   %{<path>.<path>.<...>}
    #   %{<path>.<path>.<...>.keys()}
    #   %INTF{logical_interface_name}
    #   %ENV{environment_variable_name}
    #   %CALLABLE{path_to_callable}
    #   %CALLABLE{path_to_callable(param1,param2,param3)}
    #   %INCLUDE{yaml_file_path}
    #   %ASK{optional prompt text}
    #   %ENC{encoded text}
    #   %ENC{encoded text, prefix=x}
    #   %CLI{cli_argument_name}
    #   %CLI{another_cli_arg, default=<value>}
    #   %CLI{another_list, default=[<value>,<value>]}
    #   %EXTEND_LIST{key}
    #   %EXTEND_LIST{path.to.value1,path.to.value2}
    #
    #   - use %{ } to denote the begin and end of a markup block
    #   - use . to separate reference path
    #   - use 'self' as first word to reference current device
    #   - use '.keys()' to get the key values for a path
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
    #     Supports single and double dash argument style. A default value
    #     can be specified using `, default=` syntax. A list can be specified
    #     as default value.
    #   - The %EXTEND_LIST{ } form can be used for keys to extend a list
    #     from another YAML file. The same syntax can also be used to create
    #     a value by extending one or more list references.


Markup Examples
---------------

.. code-block:: text

    # reference to current device name
    %{self}

    # reference to attributes within current device
    %{self.x.y.z}

    # reference to logical interface within current device
    # (replaced with actual interface name)
    %INTF{logical_interface_name}

    # reference to arbitrary attribute within this YAML file
    %{a.b.c}

    # reference to the list of keys of this attribute within this YAML file
    %{d.e.keys()}

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

    # A default value can be specified for the %CLI markup.
    %CLI{another_flag, default=12}

    # A default value can be a list
    %CLI{another_flag, default=[1,2]}

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
.. note::

    Make sure to enclose strings with % sign in quotes
    in the yaml file.  For example::

        testbed:
            name: my_testbed

            credentials:
                password: "%ASK{Your password}"

YAML itself does not distinguish the markups from regular text (strings).
Before the creation of testbed objects, the loader walks through the generated
data and replaces all markup languages with referenced data.
Any syntax outside of the above is neither recognized nor processed.


Testbed YAML Examples
---------------------

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

EXTEND_LIST usage examples
--------------------------

`%EXTEND_LIST` markup can be used in two ways: as a key markup or as a value markup.

1. Example EXTEND_LIST usage for key markup.

Example YAML file to be extended:

.. code-block:: yaml

    parameters:
        sections: [a, b]

YAML file extending the file above:

.. code-block:: yaml

    extends: a.yaml

    parameters:
        "%EXTEND_LIST{sections}": [c]

Example code loading an extended YAML file:

.. code-block:: python

    from pyats.utils.yaml import Loader
    loader = Loader(enable_extensions=True)
    data = loader.load('b.yaml')
    print(data)

The output from above script is show below. As you can see,
the list data was extended from [a, b] to [a, b, c].

.. code-block:: text

    {'parameters': {'sections': ['a', 'b', 'c']}}


2. Example EXTEND_LIST usage for values.

It's also possible to created a list from one or more other lists using
the EXTEND_LIST markup with one or more references to list values.

.. code-block:: yaml

    parameters:
        base_config:
            CE1:
                bgp:
                    address_families:
                        ipv4:
                            neighbors:
                                1.1.1.1: {}
                                1.1.1.2: {}
                        ipv6:
                            neighbors:
                                - 1::1
                                - 1::2

    CE1_neighbors: "%EXTEND_LIST{parameters.base_config.CE1.bgp.address_families.ipv4.neighbors.keys(),parameters.base_config.CE1.bgp.address_families.ipv6.neighbors}"


The output from above data after loading is shown below. The single lists of
neighbors is created by combining the two lists using their markup reference.

.. code-block:: text

        {
            "parameters": {
                "base_config": {
                    "CE1": {
                        "bgp": {
                            "address_families": {
                                "ipv4": {
                                    "neighbors": {
                                        "1.1.1.1": {},
                                        "1.1.1.2": {}
                                    }
                                },
                                "ipv6": {
                                    "neighbors": [
                                        "1::1",
                                        "1::2"
                                    ]
                                }
                            }
                        }
                    }
                },
                "CE1_neighbors": [
                    "1.1.1.1",
                    "1.1.1.2",
                    "1::1",
                    "1::2"
                ]
            }
        }
