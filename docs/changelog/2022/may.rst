May 2022
==========

May 30 - Pyats v22.5 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.5 
    ``pyats.aereport``, v22.5 
    ``pyats.aetest``, v22.5 
    ``pyats.async``, v22.5 
    ``pyats.cisco``, v22.5 
    ``pyats.connections``, v22.5 
    ``pyats.datastructures``, v22.5 
    ``pyats.easypy``, v22.5 
    ``pyats.kleenex``, v22.5 
    ``pyats.log``, v22.5 
    ``pyats.reporter``, v22.5 
    ``pyats.results``, v22.5 
    ``pyats.robot``, v22.5 
    ``pyats.tcl``, v22.5 
    ``pyats.topology``, v22.5 
    ``pyats.utils``, v22.5 

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* log/command
    * Removed archive zip files counting
        * The code prevent archive being fully extracted.

* pyats/easypy/manifest/virtualenv.py
    * Combine cli arguments of "pyats run manifest my_manifest.tem --arg1 value1"
    * If multiple arguments are given, translate the original form to "pyats run job

* pyats.easypy
    * Update manifest implementation to support IXIA TCL libraries

* pyats.reporter
    * Modified Task
        * Fixed bug when rolling up plugin results when the plugin has no sections
    * Modified ReporterServer
        * Fixed error message when a temporary directory has a sym-linked path

* pyats.utils
    * Remove version pinning of 'cryptography' package

* utils
    * server_name number fix
        * local address to be updated only if server name and server number is not given..

* pyats.robot
    * Removed robotframework version pinning, get valid execution options from RobotSettings


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats.easypy
    * Added `task-uids` command line option to filter tasks


