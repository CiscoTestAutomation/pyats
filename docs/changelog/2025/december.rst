December 2025
==========

December 30 - Pyats v25.11
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v25.11
    ``pyats.aereport``, v25.11
    ``pyats.aetest``, v25.11
    ``pyats.async``, v25.11
    ``pyats.cisco``, v25.11
    ``pyats.connections``, v25.11
    ``pyats.datastructures``, v25.11
    ``pyats.easypy``, v25.11
    ``pyats.kleenex``, v25.11
    ``pyats.log``, v25.11
    ``pyats.reporter``, v25.11
    ``pyats.results``, v25.11
    ``pyats.robot``, v25.11
    ``pyats.tcl``, v25.11
    ``pyats.topology``, v25.11
    ``pyats.utils``, v25.11




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* kleenex-pkg/clean/loader/_impl
    * Update the logic to handle clean when device is not provided in the

* devat-pkg
    * Update device compliance to check for password complexity for devices

* aetest
    * Testscripts that are unable to load will now properly report their failure in the Reporter.

* topology.schema
    * Added 'os' key to server definition


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats-pkg
    * Added Manifest Schema Support for Per-Profile Tags
        * Enhanced manifest schema to support optional 'tags' field within profile definitions

* reporter
    * Added ability to override Task result in Reporter server API.


