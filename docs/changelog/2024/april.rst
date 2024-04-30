April 2024
==========

April 30 - Pyats v24.4 
----------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.4 
    ``pyats.aereport``, v24.4 
    ``pyats.aetest``, v24.4 
    ``pyats.async``, v24.4 
    ``pyats.cisco``, v24.4 
    ``pyats.connections``, v24.4 
    ``pyats.datastructures``, v24.4 
    ``pyats.easypy``, v24.4 
    ``pyats.kleenex``, v24.4 
    ``pyats.log``, v24.4 
    ``pyats.reporter``, v24.4 
    ``pyats.results``, v24.4 
    ``pyats.robot``, v24.4 
    ``pyats.tcl``, v24.4 
    ``pyats.topology``, v24.4 
    ``pyats.utils``, v24.4 

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
                                      New                                       
--------------------------------------------------------------------------------

* pyats.easypy
    * Added Tips Plugin
        * A new plugin that provides a way to display tips and tricks to users

* pyats.topology
    * Updated Device class `repr`, added alias value


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* easypy
    * Fix device recovery data type for tftp address
    * Modified Plugin Reporting
        * Plugins now report errors as results even when the plugin is not specified to report anything. This prevents the overall result showing Passed when a plugin had an error.

* iosxe
    * Added RerunPlugin
        * Remove commonSetup, commonCleanup, testcases if it is none.

* easypy/plugins
    * kleenex
        * updated logic to add device recovery section even if there are no clean image attributes.

* pyats.connections
    * Modified connection manager
        * Updated logic to support service wrapper with connection pools
    * Pass Steps object to service wrapper if none found

* pyats.aetest
    * Modified Steps class to support index offset

* pyats.async
    * Support Steps with pcall
    * Modified child process logic to update steps offset for child processes
    * Add logic to propagate step failures in subprocess

* bringup
    * Manager
        * Fixed bug preventing manager from halting exit with pyats clean command

* kleenex
    * loader
        * Update to load and check the logical testbed in _preprocess_add_cli_images in order to get correct image_set for iol devices.

* pyats.cisco
    * Fix telemetry upload

* utils/fileutils
    * http
        * Added logic for http stat in fileutils.


