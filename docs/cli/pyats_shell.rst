pyats shell
=============

Command that loads a testbed YAML file into topology objects, and makes it
available to the user in a Python interactive shell.

.. code-block:: text

    Usage:
      pyats shell [options]

    Description:
      Enters typical python interactive shell, setting a global variable named
      'testbed' which contains the loaded testbed YAML file

    Shell Options:
      --testbed-file FILE   testbed file to load
      --no-ipython          do not use IPython

Effectively, the goal of this api is to save you from having to type the
following every time you want to prototype something interactively:

.. code-block:: python

    from pyats.topology import loader
    testbed = loader.load('/path/to/your/testbed.yaml')

.. tip::

    call ``exit()``, or use ``Ctrl-D`` key to exit the interactive session. 


Options
-------

``--testbed-file``
    use this argument to provide a testbed YAML file, which then gets loaded
    into ``testbed`` variable, available in the new Python interactive shell.

``--no-ipython``
    by default, if IPython is installed in this virtual environment, an IPython
    interactive session will be started. Use this flag to override this
    behavior.

Example
-------

.. code-block:: text

    $ pyats shell --testbed-file tb.yaml
    Welcome to pyATS Interactive Shell
    ==================================
    Python 3.7.0 (default, Sep  6 2018, 16:54:40)
    [Clang 10.0.0 (clang-1000.10.25.5)]

    >>> from pyats.topology import loader
    >>> testbed = loader.load('tb.yaml')
    -------------------------------------------------------------------------------
    >>> testbed.devices
    TopologyDict({'nx-osv-1': <Device nx-osv-1 at 0x1134f5cc0>, 'csr1000v-1': <Device csr1000v-1 at 0x112af5ba8>})
    >>> testbed.devices['nx-osv-1'].connect()
    [2019-02-11 12:27:54,780] +++ nx-osv-1 logfile /tmp/nx-osv-1-default-20190211T122754780.log +++
    [2019-02-11 12:27:54,781] +++ Unicon plugin nxos +++
    [2019-02-11 12:27:54,784] +++ connection to spawn: telnet 172.25.192.90 17003, id: 4620986912 +++
    [2019-02-11 12:27:54,785] connection to nx-osv-1
    [2019-02-11 12:27:54,787] telnet 172.25.192.90 17003
    Trying 172.25.192.90...
    Connected to asg-virl-ubuntu.cisco.com.
    Escape character is '^]'.

    nx-osv-1#
    [2019-02-11 12:27:55,655] +++ initializing handle +++
    [2019-02-11 12:27:55,656] +++ nx-osv-1: executing command 'term length 0' +++
    term length 0
    nx-osv-1#
    [2019-02-11 12:27:55,824] +++ nx-osv-1: executing command 'term width 511' +++
    term width 511
    nx-osv-1#
    [2019-02-11 12:27:55,991] +++ nx-osv-1: executing command 'terminal session-timeout 0' +++
    terminal session-timeout 0
    nx-osv-1#
    [2019-02-11 12:27:56,161] +++ nx-osv-1: config +++
    config term
    Enter configuration commands, one per line.  End with CNTL/Z.
    nx-osv-1(config)# no logging console
    nx-osv-1(config)# line console
    nx-osv-1(config-console)# exec-timeout 0
    nx-osv-1(config-console)# terminal width 511
    nx-osv-1(config-console)# end
    nx-osv-1#
    "Escape character is '^]'.\r\n\r\r\n\rnx-osv-1# "
    >>>
    now exiting InteractiveConsole...
