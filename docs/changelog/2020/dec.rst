December 2020
=============

December 15, 2020
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.12
    ``pyats.aereport``, v20.12
    ``pyats.aetest``, v20.12
    ``pyats.async``, v20.12
    ``pyats.cisco``, v20.12
    ``pyats.connections``, v20.12
    ``pyats.datastructures``, v20.12
    ``pyats.easypy``, v20.12
    ``pyats.kleenex``, v20.12
    ``pyats.log``, v20.12
    ``pyats.reporter``, v20.12
    ``pyats.results``, v20.12
    ``pyats.robot``, v20.12
    ``pyats.tcl``, v20.12
    ``pyats.topology``, v20.12
    ``pyats.utils``, v20.12

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Feature List
^^^^^^^^^^^^

.. list-table::
    :header-rows: 1

    * - Feature
      - Docs
      - Whats New

    * - Embedded pyATS File Transfer Server
      - :ref:`Docs <pyats_file_transfer_server>`
      - | A plugin in `genie.libs.filetransferutils` which starts a local file
        | transfer server if defined in the testbed YAML file.
        .. code-block:: text

            testbed:
              servers:
                myftpserver:
                  dynamic: true
                  protocol: ftp
                  subnet: 10.0.0.0/8
                  path: /path/to/root/dir


Other Changes
^^^^^^^^^^^^^
Log
  - Introduced a new UI page which lists all results
  - Removed pyats logs list command
  - ```pyats logs view``` command will open result list page,
    ```pyats logs view --latest``` command will open the last generated result.
  - For liveview section log, previously it always tails the log from the
    beginning of the section. After the change, it will tail only last 20
    lines of logs from the time you click, and display subsequent logs.
  - Specify library version for aiohttp, python-socketio, aiohttp-swagger
    to avoid incompatibility

Kleenex
  - Added BringupWorkerException catch to `BringUp`'s `__exit__` method
  - Added general Exception catch to `BringUp`'s `__exit__` method that will log
    details then re-raise the exception

Reporter
  - Enhanced dumping of json report to handle exceptions in data
  - More robust unix file socket creation in tmp directory

Easypy
  - pass `runinfo_dir` as parameter for script execution

Connections
  - Updated connection manager instantiate function in order to convert
    connection class from string to callable when creating device from json

Utils
  - Adjustments to fileutils to improve credential retrieval for servers
  - Warning for using the default pyats encoding key