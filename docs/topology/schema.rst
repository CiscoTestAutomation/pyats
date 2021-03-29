.. _schema:

Topology Schema
===============

The schema controls what information can go into the *testbed file*, and how
that information should be structured. All testbed files loaded through
``topology.loader`` are checked against the production schema.

Always keep in mind that YAML is a white-space indentation sensitive markup
language (like how Python is). If your testbed file is having issues, check
your section indentations.



.. _topology_credential_password_modeling:

Credential Password Modeling
----------------------------

- Credential passwords are assumed to be plain text unless specified in
  encoded form ``"%ENC{secret encoded password}`` or
  ``"%ENC{secret encoded password, prefix=alternate_encoder}``.

- Decoding of encoded passwords may depend on pyats configuration.

- A credential may have multiple fields defined, by convention ``username``
  and ``password`` are shown, but other fields may also be present.
  All credential fields with ``password`` in their name are stored internally
  as secret strings that cannot be directly printed.

- Please see :ref:`secret_strings` for more details on how pyATS models
  secret passwords.

- A credential may have a parent (for example, topology credentials
  are considered to be the parent of all device credentials).

- Any lookups done on a child credential that are not found are automatically
  done on the parent.

- Child credentials may override parent credentials of the same name.

- If a lookup is done on a named credential that is not found, the lookup
  falls back to the ``default`` credential if it has been set.


.. _topology_credential_password_prompting:

Credential Password Prompting
-----------------------------

- During testbed loading, users are prompted to manually enter any credential
  password specified in the form ``%ASK{optional prompt text}``.
  Passwords are expected to be entered in plaintext, and are not printed as
  they are entered.


Production YAML Schema
----------------------

.. code-block:: yaml

    # Testbed File Schema
    # -------------------
    #
    #   production schema with commentary from the devs

    extends:    # Testbed file(s) to extend/build on.
                # Use this field to extend an existing yaml testbed file,
                # allowing you to create an inheritance hierarchy.
                # Supports full path/names or name of file in the same dir.
                # The content of the last file on the list forms the base and
                # is updated with the preceding file, and so on,
                # until the existing file content is updated last.
                # (optional)

    # testbed block
    # -------------
    #   information concerning/common to the whole testbed.
    testbed:

        name :  # testbed name string.
                # (default: testbed filename with prefix CONFIG. and/or postfix
                #           .yaml trimmed)
                # (optional)

        alias:  # testbed name alias.
                # (default: same as testbed name)
                # (optional)

        class:  # testbed object class.
                # use this field to provide an alternative subclass of
                # Testbed to instantiate this testbed to. can be used to
                # extend the base Testbed class functionalities
                #   Eg: module.submodule.MyTestbedClass
                # (default: ats.topology.Testbed)
                # (optional)


        credentials:
            # credential details common to the testbed
            # (optional)

            <key>:        # name of this credential.
                username: # (optional)
                password: # (optional)

                # any other credential details
                <key>: <value>

        servers:
            # servers serving/helping and providing services to this entire
            # testbed. any server described here should ideally be servicing
            # the entire testbed and accessible by all devices.
            # (optional)

            <name>: # server name goes here. each server requires its own
                    # description section
                    # (optional)

                server: # server name
                        # (optional)

                type:   # server type generic string
                        # use this to describe the type of server
                        # (optional)

                address:    # server ip address, or list of server ip addresses.
                            # (optional)

                path:       # path to root folder (eg, tftproot)
                            # (optional)

                credentials:
                    # credential details common to the server
                    # (optional)

                    # All credentials in the testbed credentials block are
                    # also available at this level if not specified here.

                    <key>:         # Name of this credential.
                        username:  # (optional)
                        password:  # (optional)

                        # Any other credential details
                        <key>: <value>

                custom:
                    # any custom key/value pairs concerning this server
                    <key>: <value>

        network:
            # any network key/value pair information concerning this testbed
            # (optional)
            <key>: <value>


        custom:
            # any custom key/value pairs common to this entire testbed
            # (optional)
            <key>: <value>


    # devices block
    # -------------
    #   all testbed devices are described here
    devices:

        <name>: # device name (hostname) goes here. Each device requires its
                # own description section within devices block

            alias:  # device name alias.
                    # (default: same as device name)
                    # (optional)

            class:  # device object class.
                    # use this field to provide an alternative subclass of
                    # Device to instantiate this device block to. can be used
                    # to extend the base Device class functionalities
                    #   Eg: module.submodule.MyDeviceClass
                    # (default: ats.topology.Device)
                    # (optional)

            type:   # device type generic string
                    # use this to describe the type of device
                    #   Eg: ASR9k
                    # (required)

            region: # device region string
                    # (optional)

            role:   # device role string
                    # (optional)

            chassis_type: # device chassis_type
                          #  Eg: single_rp/dual_rp/stack/quad
                          # (optional)

            os:     # device os string
                    #  Eg: iosxe
                    # (optional)

            series: # device series string
                    #  Eg: cat3k
                    # (optional)

            platform:   # device platform string
                        # Eg: cat9300
                        # (optional)

            model:  # device model string
                    # (optional)

            power:  # device power string
                    # (optional)

            hardware:   # device hardware block
                        # may contain anything describing the hardware info
                        # (optional)

            peripherals:  # device hardware block
                          # may contain anything describing peripherals
                          # connected to the device.
                          # (optional)

            credentials:
                # credential details common to the device
                # (optional)

                # All credentials in the testbed credentials block are
                # also available at this level if not specified here.

                <key>:        # Name of this credential.
                    username: # (optional)
                    password: # (optional)

                    # Any other credential details
                    <key>: <value>

            connections:
                # block describing the 'ways', 'methods' and 'paths' of
                # connecting to this device. eg, telnet, ssh, netconf, etc
                # (required)

                defaults:
                    # block used to specify and/or alter the default
                    # connection manager behavior
                    # (optional)

                    class:  # the default connection implementation class to be
                            # used by connection manager when arguments such as
                            # 'cls' in connect() and 'factory' in start_pool()
                            # is not provided.
                            # (optional)

                    alias:  # the default alias name if 'alias' is not provided
                            # to apis such as connect(), start_pool(), etc.
                            # (optional)

                    via:    # the default path to use if 'via' is not provided
                            # to apis such as connect(), start_pool(), etc.
                            # (default: None - let the connection class decide)
                            # (optional)

                    connections: # a list of subconnections for a multi-console
                                 # device.
                                 # Supported by unicon connector implementation.
                                 # (optional)

                    connections_arguments: # arguments to apply when creating a
                                 # multi-console device connection.
                                 # Supported by unicon connector implementation.
                                 # (optional)
                                 <key>: <value>


                <name>:
                    # connection information on methods/ways to talk to this
                    # testbed device.
                    # (optional)

                    class:  # connection class to use. use this field to
                            # provide an alternative connection class to use
                            # to connect to this connection
                            # (default to the above default/class)
                            # (optional)

                    protocol:   # connection protocol
                                # (optional)

                    host:   # device hostname
                            # (optional)

                    ip:     # device connection ip address
                            # if a hostname is provided in the ip block,
                            # it be dns lookup-up and converted to IP address
                            # during testbed yaml loading.
                            # (optional)

                    port:   # port to connect to
                            # (optional)

                    credentials:
                        # credential details specific to this connection
                        # (optional)

                        # All credentials in the device and testbed credentials
                        # blocks are also available if not specified here.

                        <key>:        # Name of this credential.
                            username: # (optional)
                            password: # (optional)

                            # Any other credential details
                            <key>: <value>

                    # all other key/values under a connection information block
                    # that gets passed to the connection class constructor
                    <key>: <value>

            clean:
                # section containing all static key/value pairs required to
                # invoke clean on this device. See <Kleenex Integration> section
                # below for usage details.
                # (optional)
                <key>: <value>

            custom:
                # any custom key/value pairs specific to this device
                # (optional)
                <key>: <value>



    # topology block
    # --------------
    #   describes the actual interfaces and links
    topology:

        links:
            # section describing the links used in this testbed.
            # this section is optional. It is only needed if there's a need
            # to specify additional/custom values for the named link.
            # (optional)

            <name>: # link name. each link that has extended descriptions
                    # needs to have its own section under links
                    # (optional)

                alias:  # link alias.
                        # (default: same as link name)
                        # (optional)

                class:  # link object class.
                        # use this field to provide an alternative subclass of
                        # Link to instantiate this link block to. can be used
                        # to extend the base Link class functionalities
                        #   Eg: module.submodule.myLinkClass
                        # (default: ats.topology.Link)
                        # (optional)

                <key>: <value>  # any other key/values custom to this link
                                # goes here as standard yaml syntax
                                # (optional)

        <device>:   # each device's interface/link gets its own block named
                    # using the device name/hostname. the device mentioned
                    # here must be also described under the device block.
                    # (optional)

            interfaces: # begin the device interface description section
                        # (required)

                <intfname>: # each device interface requires its own section
                            # under the interfaces block
                            # interface names must be unique per device
                            # (optional)

                    type:   # interface type string
                            # (mandatory)

                    alias:  # interface alias.
                            # (default: same as interface name)
                            # (optional)

                    link:   # string name of the link this interface is
                            # connected to. Unique link names here yield
                            # unique links. If a linkname is also described
                            # in the link section above, the extended info
                            # for that link is used.
                            # (optional)

                    ipv4:   # ipv4 interface address and mask
                            # this is loaded and converted to
                            # ipaddress.IPv4Interface object
                            # (optional)

                    ipv6:   # ipv6 interface address and mask
                            # this is loaded and converted to
                            # ipaddress.IPv6Interface object
                            # A list of IPv6 addresses may also be provided.
                            # (optional)

                    class:  # interface object class. use this field to provide
                            # an alternative subclass of Interface class to
                            # instantiate this interface section with. can be
                            # used to extend the base Interface class functions
                            #   Eg: module.submodule.myInterfaceClass
                            # (default: ats.topology.Interface)
                            # (optional)

                    <key>: <value>  # any other key/values custom to this
                                    # interface goes here
                                    # (optional)

