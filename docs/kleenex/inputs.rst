Input Files
===========

Kleenex introduces a new input file, responsible for feeding different
information to the runtime engine: the ``clean_file``.
This file comes with its own schema, and is defined using YAML_ format.

The primary design goal of this input files is to *provide sufficient
standardization* to the look & feel of how dynamic testbed cleaning
datasets are passed to the infrastructure, whilst *maintaining enough
flexibility* to accomodate for various differences between device-specific
details & user implementations.

.. _YAML: http://www.yaml.org/spec/1.2/spec.html


.. _clean_file:

Clean File
----------

Where as a :ref:`Topology Testbed File <topology_testbed_file>` is mostly
static, describing the physical nature of the topology and its devices, a clean
file is considered to mostly contain the corresponding volatile information, eg:

    - which clean implementation to use, what is the cleaning sequence
    - arguments for instantiating and running each cleaner
    - where device images (and pies/SMUs, if applicable) are located
    - specific information related to device cleaning and image loading
    - base configuration required to operate each device
    - etc.

Consider the clean file & its content as an addendum to :ref:`Testbed File
<topology_testbed_file>`: each clean file's content defines a set of devices
and how to clean them.

When Kleenex loads a testbed's clean file, its content is parsed and stored
(updated) into the ``Device.clean`` attribute of each
:ref:`Device object<topology_device_object>`. This tight integration allows
runtime accessess to each device's specific clean information
directly through the object model. Multiple clean files can be loaded at once,
which will add to or overwrite the values of the previous clean files.

The specific runtime clean information loaded from the clean file for each
device is applied to its corresponding device object's ``clean`` dictionary
using **recursive dictionary update**. This allows the user to provide default,
static clean content in the testbed topology file and potentially overwrite it
using the clean file before a run when needed.


Images specified via filename
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is an example of specifying clean images via fully specified path names:

.. code-block:: yaml

    # Example
    # -------
    #
    #   demonstrating how clean file content is loaded
    #   and applied to device objects for user reference

    --- # assuming we have this simple testbed.yaml file
    devices:
        example-device:
            type: example-type
            connections:
                default:
                    protocol: telnet
                    ip: 1.1.1.10
                    port: 500
    ...

    --- # and we had this clean.yaml clean-file for this testbed
    cleaners:
        AwesomeClean:
            module: mollymaid.cleaners
            devices: [example-device, ]
            timeout: 1200

    devices:
        example-device:
            images:
                - /path/to/device/image/r99.9.9.bin

            awesomeclean:
                check_image_md5: True

            timeout: 900


During runtime, when the above testbed and clean files are loaded by Kleenex,
the resulting content would be as follows:

.. code-block:: python

    # Example
    # -------
    #
    #   pseduo-code demonstrating how clean content is applied to device objects

    # after the above testbed is loaded, you start with the following:
    testbed
    # <pyats.topology.testbed.Testbed object at 0xf705c40c>
    testbed.devices
    # {'example-device': <Device example-device at 0xf705cccc>}

    # the device would only have the static clean information
    # defined within the testbed yaml file
    testbed.devices['example-device'].clean
    # {'golden_image': '/path/to/golden/image.bin',
    #  'preclean': 'switchname example-device\n'
    #              'username admin password cisco123\n'
    #              'no password strength-check\n'
    #              'interface mgmt0\n'
    #              '    ip address 1.1.1.10 255.255.255.0\n'
    #              '    no shutdown\n'
    #              'vrf context management\n'
    #              '    ip route 0.0.0.0/0 1.1.1.1\n'
    #              'feature telnet\n',
    #  }

    # --------------------------------------------------
    # once the clean information is applied, it is added
    # directly to the device's clean dictionary, and the
    # resulting device.clean becomes the following:
    testbed.devices['example-device'].clean
    # {'awesomeclean': {'check_image_md5': True},
    #  'golden_image': '/path/to/golden/image.bin',
    #  'images': ['/path/to/device/image/r99.9.9.bin'],
    #  'preclean': 'switchname example-device\n'
    #              'username admin password cisco123\n'
    #              'no password strength-check\n'
    #              'interface mgmt0\n'
    #              '    ip address 1.1.1.10 255.255.255.0\n'
    #              '    no shutdown\n'
    #              'vrf context management\n'
    #              '    ip route 0.0.0.0/0 1.1.1.1\n'
    #              'feature telnet\n',
    #  'timeout': 900}}
    #
    # notice how the content of clean file got applied?
    #
    # Note: the clean timeout value if defined at the device level is always
    # used even if it is also specified at the global level.


Images specified via URL
^^^^^^^^^^^^^^^^^^^^^^^^

Images for a particular device may be specified individually via URL
or collectively via a URL of a directory in which images may be found.

.. note ::

    Neither image nor image directory URLs need to contain
    authentication details, which are instead retrieved from the server block
    of the :ref:`testbed configuration<schema>`.

.. note ::

    URL-formatted images are only supported for use by clean plugins
    and not by bringup orchestrator plugins.


.. _clean_image_url_formats:

Allowable image URL formats
"""""""""""""""""""""""""""
Image URLs take the following form :
``<protocol>://<server>.<domain>:<port>/path/to/image/my_image``

When an image is specified in a non-URL form a protocol of ``file`` is assumed.


The list of available protocols is platform-dependent
but may include the following:


.. csv-table:: Possible available clean image protocols

    file, ftp, tftp, sftp, scp

.. _clean_image_dir_url_formats:

Allowable image directory URL formats
"""""""""""""""""""""""""""""""""""""

A set of images may be specified by first specifying a set of
roles and image inclusion patterns, and then specifying a
remote directory from which the image list is to be populated.

Image directory URLs take the following form :
``<dir-protocol>://<server>.<domain>:<port>/path/to/image/``

Where ``dir-protocol`` is a protocol capable of retrieving a file listing.
If ``<dir-protocol>`` is not specified then a protocol of ``file`` is assumed.
A protocol of ``file`` is assumed when an image path is specified in
non-URL form.

The list of available directory protocols is platform-dependent
but may include the following:

.. csv-table:: Possible available clean image directory protocols

    file, ftp, sftp


Clean File Markups
------------------

The following :ref:`testbed_file_markups` are allowed in clean YAML files:
%ENV, %CALLABLE, %INCLUDE.

The following markups are also allowed:

.. code-block:: text

    # Syntax
    # ------
    #
    #   Clean YAML markup syntax

    # reference to arbitrary attribute within the clean file
    %{a.b.c}

    # reference to current clean device name.
    # This also works under the platforms: block.
    %{self}

    # reference to attributes within the current clean device section
    # This also works under the platforms: block.
    %{self.x.y.z}

    # reference to attributes within the testbed content.
    %{testbed.x.y.z}

    # reference to attributes within the testbed device section corresponding
    # to the current clean device name.
    # This also works under the platforms: block.
    %{testbed.self.x.y.z}

Clean File Loading
------------------

.. code-block:: yaml

    # Example
    # -------
    #
    #   demonstrating how clean file content is loaded
    #   and applied to device objects for user reference

    --- # assuming we have this simple testbed.yaml file
    testbed:
        servers:
            golden_img_svr.domain.com:
                # Auth details for svr to allow below url to work.
                credentials:
                    default:
                        username: jdoe
                        password: my_pw

            img_svr.domain.com:
                # Auth details for svr to allow below urls to work.
                credentials:
                    default:
                        username: jdoe
                        password: my_pw

    devices:
        example-device:
            type: example-type
            connections:
                default:
                    protocol: telnet
                    ip: 1.1.1.10
                    port: 500

        another-example-device:
            type: example-type
            connections:
                default:
                    protocol: telnet
                    ip: 1.1.1.10
                    port: 501
    ...

    --- # and we had this clean.yaml clean-file for this testbed
    cleaners:
        AwesomeClean:
            module: mollymaid.cleaners
            devices: [example-device, ]
            timeout: 1200

    devices:
        example-device:
            images:
                rp:
                    file: /path/to/device/image/r99.9.9.bin
                    include: r\d+\.\d\.\d\.bin
                    exclude: file_pat_to_exclude
                    cardinality: 1

                pie:
                    file: ftp://img_svr.domain.com/path/to/mypies/k9sec.bin
                    include: k9sec
                    cardinality: ANY


        another-example-device:
            images:
                role_defaults:
                    base_dir:  sftp://img_svr.domain.com/path/to/device/images/
                               # Is dir due to trailing slash.
                               # It is ignored if there is not at least one
                               # <role_name>/include pattern specified.
                    cardinality: 1
                rp:
                    include: r\d+\.\d\.\d\.bin
                    exclude: file_pat_to_exclude

            # Static clean information may also be specified in the clean file
            # instead of only the testbed file.  Note how the markup refers
            # to content in the testbed file's block for this device.
            apply_configuration:
                configuration: |
                    switchname another-example-device
                    username admin password cisco123
                    no password strength-check
                    interface mgmt0
                        ip address %{testbed.self.clean.mgt_itf.ipv4.address} %{testbed.self.clean.mgt_itf.ipv4.net.mask}
                        no shutdown
                    vrf context management
                        ip route 0.0.0.0/0 1.1.1.1
                    feature telnet

            awesomeclean:
                check_image_md5: True

            timeout: 900


.. _clean_schema:

Clean Schema
------------

The following describes the top-level skeleton clean file schema. When Kleenex
is provided a clean file, its content is always checked against the schema below
for consistency.

The clean schema is intended to provided only *sufficient* consistency across
the board, whilst maintaining enough *flexibility* in order to accomodate
various different user implementations.

``clean_devices``
    optional key containing a list of devices to clean sequentially. If not
    specified here or via the ``--clean-devices`` CLI parameter, defaults to
    cleaning all devices specified in the clean file that are also present
    in the testbed file.

``extends:``
    section allowing the ability for one clean file to include/extend other
    clean files (extension and/or inheritance relationship). When one clean file
    extends another, the other file forms the basis, and contents of the
    current file is then applied on top using *recursive dictionary update*.

``cleaners:``
    section defining :ref:`Cleaner classes <kleenex_cleaners>`. Declare all
    clean classes to be used for cleaning this testbed's devices, including the
    mapping of which cleaner is to be used for which device and/or group of
    devices.  If not specified then it is autopopulated by assigning to a
    default cleaner class all devices defined in the clean file (including all
    devices specified by group or platform) which are also defined in the
    testbed file.

``devices:``
    section defining device specific clean information, sub-keyed by device
    name. All key/value pairs for each device are updated into
    the corresponding device object during runtime for ease of access.

``platforms:``
    section defining platform specific clean information, sub-keyed by platform
    name. All key/value pairs for each platform are updated into
    the corresponding device object(s) with matching platform  during runtime
    for ease of access.

``groups:``
    section allowing users to group common information for multiple devices
    (eg, a platform family) together, reducing copy/pasting. During runtime,
    group information is expanded to *per device* definition and then added to
    each device's object, similarly to how the above device section works.

    .. tip::

        if the same device belongs to a group and has its device specific
        section, the group information forms the basis, and the device specific
        info is applied on top.

.. code-block:: yaml

    # Clean File Schema
    # -----------------
    #
    #   production clean file schema with commentary from the devs

    extends:    # Clean file(s) to extend/build on.
                # Use this field to extend an existing yaml clean file,
                # allowing you to create an inheritance hierarchy.
                # Supports full path/names or name of file in the same dir.
                # The content of the last file on the list forms the base and
                # is updated with the preceding file, and so on,
                # until the existing file content is updated last.
                # (optional)


    # clean_devices
    # -------------
    #
    # This optional key specifies the devices to be cleaned.
    # Devices may be specified by their actual name or their alias.
    #
    # This key may be used to clean devices sequentially.
    #
    # In the following example, device_a, device_b and device_c are
    # cleaned in parallel, and only once complete are device_d and device_e
    # cleaned in parallel.
    #
    # It may be overridden by specifying the CLI parameter clean_devices.
    #
    # clean_devices: [[device_a, device_b, device_c], [device_d, device_e]]


    # cleaners block
    # --------------
    #
    #   information regarding how kleenex cleaners are to be configured
    #   kleenex support per device/group cleaner mapping
    cleaners:

        <cleaner class>:    # Clean class implementation to instantiate
                            # This needs to be the actual class definition name
                            # to be used for cleaning one or more device.
                            # eg: PyatsDeviceClean
                            # (mandatory)

            module:         # Module where the cleaner class can be
                            # imported from. Eg, genie.libs.clean
                            # (mandatory)

            devices:        # List of cleanable devices using this cleaner class
                            # devices here need to be defined either in groups
                            # or as specific devices below.  Any devices
                            # without a corresponding testbed topology
                            # entry are ignored with a warning.
                            # Either device name or device alias may be
                            # specified.
                            # (optional)

            platforms:      # list of platforms
                            # Specify the list of platforms that belong to this
                            # group. The cleanable devices are derived from
                            # testbed topology devices with matching platform.
                            # (optional)

            groups:         # List of groups of cleanable devices using this
                            # cleaner class. any groups used here need to be
                            # defined in the groups: block down below
                            # (optional)

            timeout:        # Clean timeout in seconds.
                            # At runtime this clean timeout is used
                            # if not specified at the device level.
                            # If timeout is specified at neither level,
                            # the clean worker runs without timing out.
                            # (optional)

            # any key/value pair to be used to configure this cleaner
            # these are passed as kwargs to the class's __init__()
            <key>: <value>


    # platforms block
    # ---------------
    #
    #   clean information specific to a particular platform.
    platforms:              # A block of clean information specific to a
                            # particular platform.
                            # This block applies to every device in your
                            # testbed topology file with matching platform
                            # value.

        <platform name>:    # Platform name
                            #
                            # (mandatory)
            # platform content has an identical schema to the devices block.


    # devices block
    # -------------
    #
    #   clean information specific to each device.
    devices:

        <device name>:      # Device name (hostname)
                            # This defines the block of clean information
                            # specific to this device. This must correspond to
                            # the same device in your testbed topology file.
                            # (mandatory)


            images:         # Image(s) to be loaded for this device
                            # (2 for NXOS N7K, 1 for for most other platforms)
                            #
                            # A single image may be specified directly
                            # without using a list.
                            #
                            # Images may also be sub-keyed by role:
                            # images/<image_role>/[list of images] or
                            # images/<image_role>/single_image
                            #
                            # For example:
                            #   images:
                            #     kick: /path/to/kick.img
                            #     system: /path/to/system.img
                            #     smu: [/path/to/smu1.img, /path/to/smu2.img]
                            #
                            # Images are assumed to be filesystem-based unless
                            # they are specified as URLs of the following form:
                            # <protocol>://<server>.<domain>:<port>/path/to/image/my_image
                            # where available <protocol> values are platform
                            # dependent but could be one of the following :
                            # ftp, tftp, sftp, scp
                            #
                            # Authentication details are discovered from the
                            # servers block of the testbed topology via one
                            # of the following forms:
                            #
                            # servers:
                            #   <server>:
                            #     credentials:
                            #       ftp:
                            #         username: my_user
                            #         password: my_pw
                            #
                            # or
                            #
                            # servers:
                            #   alternate_server_name:
                            #     server: server.com
                            #     credentials:
                            #       ftp:
                            #         username: my_user
                            #         password: my_pw
                            #
                            # or
                            #
                            # servers:
                            #   alternate_server_name:
                            #     address: <server's IP address>
                            #     credentials:
                            #       ftp:
                            #         username: my_user
                            #         password: my_pw
                            #
                            # For example:
                            #  images:
                            #    kick:
                            #      file: [ftp://server.com/path/to/my/image]
                            #
                            #
                            # Images may also be specified by directory when
                            # additional validation/searching parameters
                            # are provided.
                            #
                            # For example:
                            #  images:
                            #    role_defaults:
                            #      base_dir : ftp://server.com/path/to/images
                            #      cardinality: 1
                            #    kick:
                            #      include: '.*kick.*\.bin'
                            #
                            # (optional)


                role_defaults: # Default role-based properties that apply
                               # to all defined roles unless specifically
                               # overridden at the role level.
                               #
                               # Keys shown as mandatory in this section
                               # must be specified at the role level for
                               # each defined role if not specified here.
                               # (Optional)


                        base_dir : # A directory in which the image(s)
                                   # may be found.  May be filesystem-based or
                                   # a URL of the following form:
                                   # <dir-protocol>://<server>.<domain>:<port>/path/to/image/
                                   # where available <dir-protocol> values are
                                   # platform dependent but could be one of the
                                   # following : ftp, sftp
                                   #
                                   # May only be specified when one or more
                                   # roles with include patterns are defined.
                                   # images/<role_name>/file content is then
                                   # populated from the specified directory.
                                   #
                                   # This key does not appear in the final
                                   # loaded content.
                                   #
                                   # May not be specified together with
                                   # file.
                                   # (mandatory if file not specified)


                        file: # An explicit image filename or URL (or list of
                              # filenames/URLs).
                              #
                              # Any image filename specified via URL is
                              # expected to exist, otherwise an
                              # exception is thrown.
                              #
                              # May not be specified together with base_dir.
                              #
                              # (mandatory if base_dir not specified)


                        include: # A regular expression that images
                                 # must match.
                                 #
                                 # This key does not appear in the final
                                 # loaded content.
                                 #
                                 # (mandatory only when images are specified
                                 # via base_dir).


                        exclude: # A regular expression that images
                                 # must not match.
                                 #
                                 # This key does not appear in the final
                                 # loaded content.
                                 #
                                 # (optional)


                        cardinality: # The exact number of images
                                     # that may be specified.
                                     #
                                     # It may also be specified as
                                     # ANY (case insensitive), which
                                     # means that zero or more images are
                                     # allowed.
                                     #
                                     # This key does not appear in the final
                                     # loaded content.
                                     #
                                     # (mandatory when base_dir is specified)


                <role_name>: # A role (such as system, kickstart or smu)
                             # that is recognized by this device's cleaner
                             # class.
                             #
                             # May be specified as a single filename or URL or
                             # a list of filenames/URLs.
                             #
                             # Any filename specified via URL is
                             # expected to exist, otherwise an
                             # exception is thrown.
                             #
                             # May also contain any key documented under
                             # role_defaults, the value here overrides
                             # the value in role_defaults (if specified).
                             #
                             # If specified as blank, role_defaults must
                             # not be blank, and all mandatory keys must
                             # be specified in role_defaults, otherwise
                             # an exception is thrown.


            timeout:        # Clean timeout in seconds.
                            # At runtime this clean timeout is used even
                            # if specified at the global level.
                            # If timeout is specified at neither level,
                            # the clean worker runs without timing out.
                            # (optional)

            # any key/value pair to be stored to this device object's
            # Device.clean attribute. (nested dictionary update)
            <key>: <value>


    # groups block
    # ------------
    #
    #   clean information common to a group of devices
    groups:

        <group name>:       # group name (arbitrary string)
                            # define a group of devices that share the same
                            # clean definitions.
                            # (mandatory)


            devices:        # list of devices
                            # Specify the list of devices that belong to this
                            # group (either device name or device alias may
                            # be specified).
                            # (Do not specify more than a single group type)
                            # (choose only one from os, platforms, devices group types.)


            platforms:      # list of platforms
                            # Specify the list of platforms that belong to this
                            # group. The devices in this group are derived from
                            # testbed topology devices with matching platform.
                            # (Do not specify more than a single group type)
                            # (choose only one from os, platforms, devices group types.)
            

            os:             # list of os
                            # Specify the list of os that belong to this
                            # group. The devices in this group are derived from
                            # testbed topology devices with matching os.
                            # (Do not specify more than a single group type)
                            # (choose only one from os, platforms, devices group types.)
                            


            images:         # Image(s) to be loaded for this group's
                            # devices (2 for NXOS N7K,
                            # 1 for for most other platforms)
                            # A single image may be specified directly
                            # without using a list.
                            #
                            # Images may also be sub-keyed by role:
                            # images/<image_role>/[list of images] or
                            # images/<image_role>/single_image
                            #
                            # For example:
                            #   images:
                            #     kick: /path/to/kick.img
                            #     system: /path/to/system.img
                            #     smu: [/path/to/smu1.img, /path/to/smu2.img]
                            #
                            # Images are assumed to be filesystem-based unless
                            # they are specified as URLs of the following form:
                            # <protocol>://<server>.<domain>:<port>/path/to/image/my_image
                            # where available <protocol> values are platform
                            # dependent but could be one of the following :
                            # ftp, tftp, sftp, scp
                            #
                            # For example:
                            #  images:
                            #    kick:
                            #      file: [ftp://server.com/path/to/my/image]
                            #
                            # Images may also be specified by directory when
                            # additional validation/searching parameters
                            # are provided.
                            #
                            # For example:
                            #  images:
                            #    role_defaults:
                            #      base_dir : ftp://server.com/path/to/images
                            #      cardinality: 1
                            #    kick:
                            #      include: '.*kick.*\.bin'
                            #
                            # Please refer to the schema and examples under
                            # devices/<device_name>/images
                            # as they also apply at the group level.
                            #
                            # (optional)


            timeout:        # clean timeout in seconds.
                            # if not timeout is specified, clean worker will
                            # run without timing out.
                            # (optional)

            # any key/value pair to be stored to this group's device object's
            # Device.clean attribute. (nested dictionary update)
            <key>: <value>
