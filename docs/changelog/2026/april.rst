April 2026
==========

April 28 - Pyats v26.4
----------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.4
    ``pyats.aereport``, v26.4
    ``pyats.aetest``, v26.4
    ``pyats.async``, v26.4
    ``pyats.cisco``, v26.4
    ``pyats.connections``, v26.4
    ``pyats.datastructures``, v26.4
    ``pyats.easypy``, v26.4
    ``pyats.kleenex``, v26.4
    ``pyats.log``, v26.4
    ``pyats.reporter``, v26.4
    ``pyats.results``, v26.4
    ``pyats.robot``, v26.4
    ``pyats.tcl``, v26.4
    ``pyats.topology``, v26.4
    ``pyats.utils``, v26.4




Changelogs
^^^^^^^^^^

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* topology
    * Update testbed schema to include static testbed information

* pyats.configuration
    * Modified Configuration
        * Added environment variable expansion for values loaded from ``pyats.conf``
        * Supports both ``$VAR``and``${VAR}`` syntax in INI configuration values


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* topology
    * Removed pathspec dependency
        * Removed unused direct dependency on pathspec==0.12.1; it is already
        * Removed corresponding pathspec deprecation-warning filters from

* cisco
    * Modified testbed CLI unit tests
        * Reduced brittleness in testbed bringup help and BringUp argument assertions so dynamically added worker CLI options do not cause unrelated test failures


