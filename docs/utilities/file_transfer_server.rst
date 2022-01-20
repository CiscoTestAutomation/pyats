.. _pyats_file_transfer_server:

Embedded pyATS File Transfer Server
===================================

The embedded file transfer server allows a server to be launched automatically
with any pyATS job run. This enables file transfer with devices for the duration
of a run, with support for FTP, TFTP, SCP and HTTP. The `FileServer` class uses
the `device.spawn.pid` process ID to lookup the local IP address which is
reachable by devices in the testbed. Altnernatively, you can specify the `subnet`
argument to find the correct network interface and local IP address. Once found,
the testbed will be updated with the accurate server address, and launch a process
with file server to listen on that interface with a random port. The SCP protocol
just gathers the relevant information to add to the testbed and enable easy SCP
copying with a device, but does not start any other processes.

When an file server is started, it will auto generate random credentials. These
are only used for the duration of the run, after which they are lost. They are
also entirely unrelated to user credentials, keeping user credentials secure.

The `FileServer` class and related Easypy Plugin are found in the
`genie.libs.filetransferutils` package, and the plugin will be automatically run
with every pyATS run as long as it is installed.


Using the Plugin
----------------

To start a file transfer server using the Easypy Plugin, the server must be
defined in the testbed YAML file with `dynamic: true`, as well as some other
information.

.. code-block:: yaml

    testbed:
      servers:
        myftpserver:
          dynamic: true
          protocol: ftp
          subnet: 10.0.0.0/8  # Optional
          path: /path/to/root/dir

Additional information can be defined for dynamic servers:

  - `dynamic: true` allows the file transfer server plugin to identify it
    as a server to be started.
  - `protocol` is one of `ftp`, `tftp`, or `scp`. The default is `ftp`.
  - `subnet` is how the `FileServer` can identify which interface faces the
    testbed network so that the devices will be able to connect and copy files.
    This can also be defined in :ref:`pyats_configuration`. (optional)
  - `path` is the root directory being served by a FTP or TFTP server. The
    default is `/`

Once a server is started by the plugin, copy commands can just reference it by
name. An example using a Genie API:

.. code-block:: python

    uut.api.copy_to_device(protocol='ftp',
                           server='myftpserver',
                           remote_path='myimage.bin',
                           local_path='flash:/‘)


Using as a context manager
--------------------------

A `FileServer` can also be used as a context manager if not defined in the
testbed. It will only last for the duration of the context block, but can also
add itself to the testbed for discovery by various copy APIs during that time.


.. code-block:: python

    from genie.libs.filetransferutils import FileServer
    with FileServer(protocol='ftp',
                    path='/path/to/root/dir',
                    testbed=testbed,
                    name='mycontextserver') as fs:
        uut.api.copy_to_device(protocol='ftp',
                               server='mycontextserver',
                               remote_path='myimage.bin',
                               local_path='flash:/‘)


Caveats
-------

- Devices may not support copying to a non-standard port. The default port can
  be used by defining the `port` value of the server as well in the testbed YAML
  with the default port `69` for TFTP. However this port must be available for
  this to work, or the plugin will fail and the job will not execute.
