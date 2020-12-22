.. _pyats_file_transfer_utilities:

Multiprotocol File Transfer Utilities
=====================================

These utilities provide a common OS and protocol agnostic framework for
client-side file-based operations such as:

* Transferring a single file to or from a remote server,

* Changing permissions, renaming, deleting and obtaining details of
  single remote files,

* Obtaining a remote directory listing,

* Performing existence and stability checking of a single remote file.


This framework strives to eliminate the need for multiple similar
file transfer packages, all doing the same thing slightly differently, and
to harmonize on a common extensible architecture that provides a consistent
look and feel to users.

Linux client support is provided out of the box and additional file utility
support may be added for other OS by installing available external plugin
packages.

These operations are supported across a variety of protocols, to the extent
allowed by the protocol and OS themselves (for example, it is not possible to
request a remote directory listing via tftp from a Linux client).  It may not
be possible to request a chmod on platform XYZ because its ftp protocol
client may not have this capability.

Files and directories are specified in the compact and expressive
URL form [#f3]_, such as::

    protocol://server.domain.com:port/path/to/file_or_directory

If the file or directory is not specified in URL form, then local form [#f2]_
is assumed (for example,  ``/path/to/file`` is internally converted to
``file:/path/to/file``).


Abstraction by OS
-----------------
All file operations are, by default, done relative to the local execution
host.  The following example shows a sample operation on a Linux client:

.. code-block:: python

    ---------------------------------------------------------------------------
    # Contents of testbed YAML file tb.yaml

    testbed:
      servers:
        server_alias:
          server: myserver.domain.com
          address: 1.1.1.1
          credentials:
            ftp:
              username: my_username
              password: my_password
    ---------------------------------------------------------------------------

    # Example of Linux based file operations
    #
    from pyats.utils.fileutils import FileUtils
    from pyats.topology import loader
    tb = loader.load('tb.yaml')


    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    futils.copyfile(
        source = 'file:/device/local/path/to/file',
        destination = 'ftp://myserver.domain.com/remote/path/to/file')

In order for file operations to be done relative to a remote device (instead of the local execution host),
an external package providing file utilities plugins for this OS must be pip-installed.
The following example shows a sample operation on such a host:

.. code-block:: python

    ---------------------------------------------------------------------------
    # Contents of testbed YAML file tb.yaml
    devices:
        my_xyz_device:
            os: xyz
            connections:
                protocol: telnet
                ip: 1.2.3.4
                port: 5678

    testbed:
      servers:
        server_alias:
          server: myserver.domain.com
          address: 1.1.1.1
          credentials:
            ftp:
              username: my_username
              password: my_password
    ---------------------------------------------------------------------------

    # Example of remote device based file operations
    # (external plugin required)
    #
    from pyats.utils.fileutils import FileUtils
    from pyats.topology import loader
    tb = loader.load('tb.yaml')

    futils = FileUtils.from_device(tb.devices['my_xyz_device'])
    futils.copyfile(
        source = 'file:/device/local/path/to/file',
        destination = 'ftp://myserver.domain.com/remote/path/to/file')


Multi-Homed Server Handling
---------------------------

In the cases when a server has multiple IP addresses specified, the plugin
does a one-shot determination of which IP address is reachable (slow path)
and then uses this cached address from then on (fast path).

Here's an example on a linux plugin:

.. code-block:: python

    ---------------------------------------------------------------------------
    # Contents of testbed YAML file tb.yaml

    testbed:
      servers:
        server_alias:
          server: myserver.domain.com
          address:
              - 1.1.1.1
              - 2.2.2.2
          credentials:
            ftp:
              username: my_username
              password: my_password
    ---------------------------------------------------------------------------

    # Example of Linux based file operations
    #
    from pyats.utils.fileutils import FileUtils
    from pyats.topology import loader
    tb = loader.load('tb.yaml')


    # Note the use of server alias here.
    #
    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    futils.copyfile(
        source = 'file:/device/local/path/to/file',
        destination = 'ftp://server_alias/remote/path/to/file')

    # The linux plugin pings the first address and, if reachable, uses that
    # address instead of the specified hostname (server_alias).
    # Otherwise, the next address in the list is pinged.
    # If no address is reachable, the hostname used defaults to
    # the server key (myserver.domain.com) if provided.



Linux Plugin
------------
This plugin provides file-based operations on a Linux client (including Mac),
and is the default plugin returned by a call to ``FileUtils()`` when ``os``
is not specified.

The server portion of any of this plugin's URL inputs may be specified as a
name having a valid DNS lookup or as an explicit IP address but if there is no
corresponding entry provided in the testbed servers block, users restrict
themselves to using only the protocols such as scp and sftp that support local
key-based authentication.

Examples
^^^^^^^^
Here are some examples of file-based operations from a Linux client:

.. code-block:: python

    ---------------------------------------------------------------------------
    # Contents of testbed YAML file tb.yaml
    testbed:
      servers:
        server_alias:
          server: myserver.domain.com
          address: 1.1.1.1
          credentials:
            default:
              username: my_username
              password: my_password

    ---------------------------------------------------------------------------
    # Examples
    # --------
    #
    from pyats.utils.fileutils import FileUtils
    from pyats.topology import loader
    tb = loader.load('tb.yaml')


    # This with statement ensures that any sessions are automatically closed
    # if something goes wrong.
    with FileUtils(testbed=tb) as futils:
        # Copy local file to remote location (note the two ways of specifying server name):
        futils.copyfile(
            source = '/local/path/to/file',
            destination = 'ftp://server_alias/remote/path/to/file')

        futils.copyfile(
            source = 'file:///local/path/to/file',
            destination = 'tftp://myserver.domain.com/remote/path/to/file',
            timeout_seconds=80)


        # Copy remote file to local location, specifying the server via its address:
        futils.copyfile(
            source = 'scp://1.1.1.1/path/to/file',
            destination = '/local/path/to/file')

        # Copy remote file to a relative local location, when the local file
        # does not have a leading slash:
        # NOTE : Due to restrictions documented in RFC3986 section 3.3
        # it is not possible to specify the 'file://' prefix for this kind of operation.

        import os
        os.chdir('/local/path/to')
        futils.copyfile(
            source = 'scp://1.1.1.1/path/to/file',
            destination = 'file')

        # Copy remote file to a relative local location, when the local file
        # has a leading single or double dot.
        # NOTE : Due to restrictions documented in RFC3986 section 3.3
        # it is not possible to specify the 'file://' prefix for this kind of operation.

        import os
        os.chdir('/local/path/to')
        futils.copyfile(
            source = 'scp://1.1.1.1/path/to/file',
            destination = './file')

        # Copy remote file to a local location relative to the calling user's
        # home directory.
        # NOTE : Due to restrictions documented in RFC3986 section 3.3
        # it is not possible to specify the 'file://' prefix for this kind of operation.

        import os
        os.chdir('/local/path/to')
        futils.copyfile(
            source = 'scp://1.1.1.1/path/to/file',
            destination = '~/file')

        # Copy remote file to a local location relative to the named user's
        # home directory.
        # NOTE : Due to restrictions documented in RFC3986 section 3.3
        # it is not possible to specify the 'file://' prefix for this kind of operation.

        import os
        os.chdir('/local/path/to')
        futils.copyfile(
            source = 'scp://1.1.1.1/path/to/file',
            destination = '~nameduser/file')


        # Delete a remote file:
        futils.deletefile(target = 'sftp://myserver.domain.com/remote/path/to/file')


        # Change permissions of a remote file:
        import stat
        mode  = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IXOTH
        futils.chmod(target = 'ftp://myserver.domain.com/remote/path/to/file', mode=mode)


        # Get details of a remote file (such as length and permissions):
        file_details = futils.stat(
            target = 'sftp://myserver.domain.com/remote/path/to/file')
        import stat
        stat.filemode(file_details.st_mode)
        '-rwxrwxrwx'


        # Obtain a remote directory listing (top-level only):
        futils.dir(target = 'ftp://myserver.domain.com/remote/path/to/')
        ['ftp://myserver.domain.com/remote/path/to/file',]


        # Rename a remote file:
        futils.renamefile(
            source = 'ftp://myserver.domain.com/remote/path/to/file',
            destination = 'ftp://myserver.domain.com/remote/path/to/renamed_file')


        # Check the existence of a remote file:
        futils.checkfile(target = 'ftp://myserver.domain.com/remote/path/to/file')


        # Check that a remote file exists and has a stable length (is not in the
        # middle of being written):

        futils.checkfile(
            target = 'ftp://myserver.domain.com/remote/path/to/file',
            check_stability=True)


        # Requesting an operation unsupported by the specified protocol
        # (expected to throw an exception):
        futils.checkfile(target = 'tftp://myserver.domain.com/remote/path/to/file')


Supported protocols
^^^^^^^^^^^^^^^^^^^

This section describes the supported protocols and the operations they offer.

An operation (such as ``copyfile``) against a protocol (such as ``ftp``)
requires a protocol-named credential (such as ``ftp``) to be declared at the
server or testbed level.  If not declared, then the ``default`` credential is
used.

Please see :ref:`topology_credential_password_modeling` for details.

Protocol support by operation
"""""""""""""""""""""""""""""

.. csv-table:: Protocol support by operation
    :header: "Operation", "ftp", "tftp [#f5]_", "scp [#f1]_", "sftp [#f1]_"

    ``copyfile``, Y, Y, Y, Y
    ``deletefile``, Y,,, Y
    ``chmod``, Y,,,Y
    ``stat``, Y,,, Y
    ``dir``, Y,,, Y
    ``renamefile``, Y,,, Y
    ``checkfile``, Y,,, Y
	``getspace``, ,,Y,Y


TFTP
""""
Support for this protocol is only available when the execution server has
the ``curl`` [#f4]_ system package installed.  This package is commonly
installed on most Linux distributions.


FTP
"""
This protocol is supported natively.

.. note::
   All operations on this plugin support an argument ``strip_leading_slash``,
   which defaults to `True`, and thus causing the leading filename or path
   slash to be stripped before being sent to the remote server.
   Some servers require this to be set to `False`.


SCP
"""
In order to enable support for this plugin, please execute the following
command manually:

.. code-block:: bash

    pip install scp paramiko

If local keys are available, they are also considered for authentication.


SFTP
""""
In order to enable support for this plugin, please execute the following
command manually:

.. code-block:: bash

    pip install paramiko


If local keys are available, they are also considered for authentication.

.. _pyats_file_transfer_base_api:

API Guide
---------

Common APIs
^^^^^^^^^^^

The following APIs are supported on any FileUtils instance:

from_device
"""""""""""

Create a FileUtils instance from a device.  This is typically used to
access client-side file utilities on a non-Linux host, if such support has been
made available via an external pip-installed plugin package.

The device is expected to have an ``os`` member, which is used to select
the appropriate FileUtils plugin to be created.

.. code-block:: python

    futils = FileUtils.from_device(device=testbed.devices['my_xyz_device'])

Context Manager
"""""""""""""""

A ``FileUtils`` instance may be used as a context manager, thus ensuring
all sessions are properly closed whether or not the operation succeeded.
Within the context block the session for a particular protocol is set up
only once and is then reused thereafter.


.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        file_details = futils.stat("sftp://server.domain.com/path/to/file")
        file2_details = futils.stat("sftp://server.domain.com/path/to/file2")

close
"""""

Close all sessions on a ``FileUtils`` instance.

Some protocol implementations (such as ``scp`` and ``sftp``) keep their
sessions open until they are explicitly closed.



.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    try:
        file_details = futils.stat("sftp://server.domain.com/path/to/file")
        file2_details = futils.stat("sftp://server.domain.com/path/to/file2")
    finally:
        futils.close()


checkfile
"""""""""
Check for remote file existence and (optionally) stability.

If ``check_stability`` is specified as `True`, multiple checks are done to
ensure the file length is stable (it could be in the middle of being copied).


.. csv-table:: ``checkfile`` arguments
    :header: "Argument", "Type", "Description"

            ``target``, `str`, Remote file to check
            ``check_stability``, `bool (default = False)<bool>`, Whether or not to check file length stability.
            ``max_tries``, `int (default = 3)<int>`, Maximum number of times to check the file before aborting.
            ``delay_seconds``, `int (default = 2)<int>`, Delay between retries
            ``timeout_seconds``, `int (default = 60)<int>`, Connection timeout


.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        futils.checkfile("sftp://server.domain.com/path/to/file")



Linux APIs
^^^^^^^^^^

The following APIs are supported on any FileUtils Linux instance:


copyfile
""""""""
Copy a single file either from local to remote or remote to local.

Remote to remote transfers are not supported (the user is expected to
make multiple calls to do this).

Local to local transfers are not supported.

.. csv-table:: ``copyfile`` arguments
    :header: "Argument", "Type", "Description"

            ``source``, `str`, Source file for copy
            ``destination``, `str`, Destination file for copy
            ``timeout_seconds``, `int (default = 1200)<int>`, Copy timeout [#f6]_
			``quiet``, `bool (default = False)<bool>`, quiet mode to suppress printing of copy progress

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        futils.copyfile(
            source = 'scp://1.1.1.1/path/to/file',
            destination = '/local/path/to/file')

deletefile
""""""""""
Delete a single remote file.


.. csv-table:: ``deletefile`` arguments
    :header: "Argument", "Type", "Description"

            ``target``, `str`, File to delete
            ``timeout_seconds``, `int (default = 60)<int>`, Connection timeout


.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        futils.deletefile("sftp://server.domain.com/path/to/file")


dir
"""
Retrieve filename URLs contained in the top level of a remote directory.


.. csv-table:: ``dir`` arguments
    :header: "Argument", "Type", "Description"

            ``target``, `str`, Directory whose contents are to be retrieved
            ``timeout_seconds``, `int (default = 60)<int>`, Connection timeout


.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        futils.dir("sftp://server.domain.com/path/to/")

    ['sftp://server.domain.com/path/to/file',]


stat
""""
Retrieve details of a remote file in a structure similar to that of
``os.stat``.


.. csv-table:: ``stat`` arguments
    :header: "Argument", "Type", "Description"

            ``target``, `str`, File whose details are to be retrieved
            ``timeout_seconds``, `int (default = 60)<int>`, Connection timeout


.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        file_details = futils.stat("sftp://server.domain.com/path/to/file")

        import stat
        print(stat.filemode(file_details.st_mode))

    '-rwxrwxrwx'


chmod
"""""
Change the permissions of a remote file.

.. csv-table:: ``chmod`` arguments
    :header: "Argument", "Type", "Description"

            ``target``, `str`, File whose permissions are to be changed
            ``mode``, `int`, File permissions (same format as `os.chmod`)
            ``timeout_seconds``, `int (default = 60)<int>`, Connection timeout

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        import stat
        mode  = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IXOTH
        futils.chmod(target = 'ftp://myserver.domain.com/remote/path/to/file', mode=mode)



renamefile
""""""""""
Rename a single remote file.

.. csv-table:: ``renamefile`` arguments
    :header: "Argument", "Type", "Description"

            ``source``, `str`, Remote file to rename
            ``destination``, `str`, New remote file name
            ``timeout_seconds``, `int (default = 60)<int>`, Connection timeout

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        futils.renamefile(
            source = 'ftp://myserver.domain.com/remote/path/to/file',
            destination = 'ftp://myserver.domain.com/remote/path/to/renamed_file')


getspace
""""""""""
Get the available disk space at target directory in bytes.

.. csv-table:: ``getspace`` arguments
    :header: "Argument", "Type", "Description"

            ``target``, `str`, Directory location to check available disk space
            ``timeout_seconds``, `int (default = 60)<int>`, Connection timeout


.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    with FileUtils(testbed=tb) as futils:
        futils.getspace("sftp://server.domain.com/path/to/")

    29832314880


Developer's Guide
-----------------
This section gives guidance on how to develop a FileUtils plugin for a device
with a non-Linux OS.

File operations are expected to be performed relative to
(ie. via running commands on) the device,
Users are expected to first connect to the device and then instantiate the
device's FileUtils plugin using ``FileUtils.from_device``.


Suggested Package File Layout
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    |-- .gitignore                        Tell git to ignore many common file types
    |-- README.rst                        Points to src/myfutils/README.rst
    |-- DESCRIPTION.rst                   Long description of package
    |-- MANIFEST.in                       Extra files to be packaged
    |-- setup.py                          For PyPi distribution of your package and
    |                                     unit test execution.
    |-- tests                             Sym-link to the src/myfutils/tests folder
    |-- docs                              Sphinx online documentation for your package
    |   |-- README.rst
    |   `-- changelog
    `-- src                               All sources for package myfutils
        |-- __init__.py                   Module declaration file
        `-- myfutils
            |-- __init__.py               Module declaration file
            |-- README.rst                Instructions to the installing user.
            |-- fileutils.py              Top-level fileutils, inherits from
            |                             ats.utils.fileutils.FileUtils
            |-- plugins                   All FileUtils OS plugins are under this directory
            |   |-- xyz                   Plugin module providing support for OS xyz
            |       |-- __init__.py       Module declaration file
            |       |-- fileutils.py      Fileutils module for OS xyz
            |       `-- ftp               Optional subplugin (child) module providing
            |           |                 support for protocol ftp on OS xyz
            |           `-- __init__.py   Module declaration file
            |           `-- fileutils.py  Fileutils module providing ftp services
            |                             for OS xyz
            |-- tests                     Unit tests for the package

Protocol-level Abstraction
^^^^^^^^^^^^^^^^^^^^^^^^^^
A parent module advertises file utilities for a specific OS and implements
user-facing operations defined by the base class.

If it has any contained packages they are treated as subplugins that a
parent may instantiate via ``get_child``.  In this way, a parent may delegate
processing of a file operation to a protocol-specific child object which is
created only when the user invokes an operation against that protocol.

When a user executes ``from pyats.utils.fileutils import FileUtils`` all
advertised OS-specific plugins (and any subplugins underneath them) are
automatically loaded.

A child object is expected to both be contained by and inherit from the
parent class.  A child object has access to its parent object via its
``parent`` member (which is set to `None` on a parent object).  A parent object
has access to its child objects via its ``children`` member.

Every child must implement each user-facing operation implemented by its
parent, and raise a ``NonImplementedError`` if it does not support the
operation.

The first time a child is allocated for a given protocol by calling
``get_child`` it is instantiated and added to a cache.
Subsequent calls by the parent to ``get_child`` return the cached object.
This allows a child to maintain session state if required.

It is possible to remove a child from the cache so the next time ``get_child``
is called a new object is instantiated.


Package Designer's Responsibilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Define one or more OS-specific plugins and ensure they inherit from
  ``pyats.utils.fileutils.FileUtils``.

- Ensure plugins implementing the ``dir`` operation return a list of files
  expressed in URL form.

- Define a plugin point for each provided OS fileutils implementation to allow
  it to be automatically loaded by the core and be made accessible to users:

  .. code-block:: python

    # setup.py
    ...
    # console entry point
    entry_points = {
        'pyats.utils.fileutils.plugins' : [
            'xyz = myfutils.plugins.xyz',
        ],
    },


- Ensure each input URL is checked for remote/local and refuse any operations
  that are not supported.

- Parse each input URL with ``urllib.parse.urlparse`` and ignore unsupported
  parts with a warning (for example, embedded username/password, fragments
  or query parameters).

- Implement the ``close`` method and, if children have been allocated via
  ``get_child`` delegate the close to each child.

Sample Implementation
^^^^^^^^^^^^^^^^^^^^^

Here is a sample implementation of a FileUtils plugin for platform XYZ and
protocol ``ftp``.

The parent class:

  .. code-block:: python

      from pyats.utils.fileutils import FileUtils as FileUtilsBase

      class FileUtils(FileUtilsBsae):
        DEFAULT_COPY_TIMEOUT_SECONDS = 1200

        def close(self):
            """ Deallocate any resources being held.  """
            for child_name, child_obj in self.children.items():
                child_obj.close()


        def copyfile(self, source, destination,
                timeout_seconds = DEFAULT_COPY_TIMEOUT_SECONDS,
                *args, **kwargs):
            """ Copy a file to/from a remote server. """

            from_scheme = self.get_scheme(source)
            to_scheme = self.get_scheme(destination)

            from_scheme_is_local = self.is_local(source)
            to_scheme_is_local = self.is_local(destination)

            if from_scheme_is_local and to_scheme_is_local:
                raise Exception("fileutils module {} does not allow "
                    "copying between two local files.".format(self.__module__))

            if not from_scheme_is_local and not to_scheme_is_local:
                raise Exception("fileutils module {} does not allow "
                    "copying between two remote files.".format(self.__module__))


            abstraction_scheme = to_scheme if from_scheme_is_local else from_scheme

            # Get implementation
            child = self.get_child(abstraction_scheme, **kwargs)

            # Execute copy
            return child.copyfile(source, destination, timeout_seconds,
                *args, upload=from_scheme_is_local, **kwargs)



The child (protocol-specific) class:

    .. code-block:: python

        from urllib.parse import urlparse
        from .. import FileUtils as FileUtilsXyzBase

        class FileUtils(FileUtilsXyzBase):

            def copyfile(self, source, destination,
                    timeout_seconds = DEFAULT_COPY_TIMEOUT_SECONDS,
                    *args, upload, **kwargs):

            from_parsed_url = urlparse(source)
            to_parsed_url = urlparse(destination)
            if upload:
                from_path = from_parsed_url.path

                to_server_name = to_parsed_url.hostname
                to_parsed_port = to_parsed_url.port
                to_path = to_parsed_url.path
                server_name = to_server_name
                port = to_parsed_port
            else:
                to_path = to_parsed_url.path
                from_server_name = from_parsed_url.hostname
                from_parsed_port = from_parsed_url.port
                from_path = from_parsed_url.path

                server_name = from_server_name
                port = from_parsed_port

            # Get auth details
            username, password = self.get_auth(server_name)

            # Transfer the file by executing commands on the device.
            if upload:
                upload_ftp_file(
                    from_path=from_path,
                    to_path=to_path,
                    device=self.parent.device,
                    username=username,
                    password=password,
                    timeout=timeout_seconds)
            else:
                download_ftp_file(
                    from_path=from_path,
                    to_path=to_path,
                    device=self.parent.device,
                    username=username,
                    password=password,
                    timeout=timeout_seconds)






API Guide for Plugin Developers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

is_local
""""""""

Returns `True` if the URL refers to a local resource.


.. csv-table:: ``is_local`` arguments
    :header: "Argument", "Type", "Description"

            ``url``, `str`, URL to check

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    assert futils.is_local("file:///path/to/local/file"


is_remote
"""""""""

Returns `True` if the URL refers to a remote (ie. non-local) resource.


.. csv-table:: ``is_remote`` arguments
    :header: "Argument", "Type", "Description"

            ``url``, `str`, URL to check

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    assert futils.is_remote("ftp://server.com/path/to/remote/file"


get_protocol
""""""""""""

Returns the URL protocol (scheme).


.. csv-table:: ``get_protocol`` arguments
    :header: "Argument", "Type", "Description"

            ``url``, `str`, URL to parse

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    assert futils.get_protocol("ftp://server.com/path/to/remote/file") == 'ftp'


get_auth
""""""""

Get authentication details from self.testbed

Returns (username, password) as strings or `None` if not found.


.. csv-table:: ``get_auth`` arguments
    :header: "Argument", "Type", "Description"

            ``server_name_or_ip``, `str`, Server name or alias or IP address.

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    username, password = futils.get_auth(server_name)


get_hostname
""""""""""""

Get hostname details from self.testbed.

The hostname is set to:

- the contents of the ``address`` key if present in the testbed's server block.

  - if multiple address is present (eg, the server block contains a list of
    addresses), the first network-reachable address (eg, responds to ping), is
    returned

- Otherwise, the contents of the ``server`` key if present in the testbed's
  server block.

- Otherwise, the server alias.

- Otherwise, if the server block is not found in the testbed, `None`.


.. csv-table:: ``get_hostname`` arguments
    :header: "Argument", "Type", "Description"

            ``server_name_or_ip``, `str`, Server name or alias or IP address.

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    hostname = futils.get_hostname(server_name)


get_server_block
""""""""""""""""

Get server block from self.testbed

Returns the server block dictionary.


.. csv-table:: ``get_server_block`` arguments
    :header: "Argument", "Type", "Description"

            ``server_name_or_ip``, `str`, Server name or alias or IP address.

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    server_block = futils.get_server_block(server_name)


get_child
"""""""""
Get a child FileUtils object under the current OS.
If a child does not exist in the cache it is instantiated, otherwise it is
returned from the cache.

To be called by a parent (OS-specific) FileUtils object.

The ``parent`` member of the child points back to the containing parent.
The ``children`` member of the parent holds a list of instantiated children.


.. csv-table:: ``get_child`` arguments
    :header: "Argument", "Type", "Description"

            ``abstraction_key``, `str`, The name of the protocol being abstracted

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    futils_ftp = futils.get_child('ftp')
    assert futils_ftp.parent is futils


remove_child
""""""""""""
Remove a child FileUtils object from the cache.

To be called by a parent (OS-specific) FileUtils object.

All resources are first deallocated by calling the child's ``close`` method.
The child is then removed from the cache and deleted.


.. csv-table:: ``remove_child`` arguments
    :header: "Argument", "Type", "Description"

            ``abstraction_key``, `str`, The name of the protocol being abstracted

.. code-block:: python

    from pyats.utils.fileutils import FileUtils
    futils = FileUtils(testbed=tb)
    futils_ftp = futils.get_child('ftp')
    assert futils_ftp.parent is futils




.. [#f1] Requires additional python dependencies to be manually pip-installed.

.. [#f2] Please see Appendix B of `RFC8089`_ for examples of how local
         files are expressed in URL form.

.. [#f3] Please see `RFC3986`_ for a standards-based discussion of URLs.

.. [#f4] `curl`_ is a popular file transfer system package.

.. [#f5] Requires additional system packages to be manually installed.

.. [#f6] The connection timeout is calculated as a percentage of the copy
         timeout in order to keep the API simple.

.. _RFC8089: https://tools.ietf.org/html/rfc8089#appendix-B
.. _RFC3986: https://tools.ietf.org/html/rfc3986
.. _curl: https://curl.haxx.se/
