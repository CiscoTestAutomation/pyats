January 2025
==========

 - Pyats v25.1 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v25.1 
    ``pyats.aereport``, v25.1 
    ``pyats.aetest``, v25.1 
    ``pyats.async``, v25.1 
    ``pyats.cisco``, v25.1 
    ``pyats.connections``, v25.1 
    ``pyats.datastructures``, v25.1 
    ``pyats.easypy``, v25.1 
    ``pyats.kleenex``, v25.1 
    ``pyats.log``, v25.1 
    ``pyats.reporter``, v25.1 
    ``pyats.results``, v25.1 
    ``pyats.robot``, v25.1 
    ``pyats.tcl``, v25.1 
    ``pyats.topology``, v25.1 
    ``pyats.utils``, v25.1 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* cisco
    * Modified Testbed Exporter
        * Updated call to convert_to_pyats as it is now an async function

* pyats/aetest
    * pyATS Health check logging is too noisy, added logic to handle it.

* kleenex
    * bringup
        * remove alias from LOGICAL_INTERFACE_KEYS_TO_IGNORE

* pyats
    * Service Wrapper
        * Updated service wrapper to search for service attributes
    * Fix syntax warning

* connections.utils
    * Modified set_parameters
        * Updated function to copy args and kwargs instead of deepcopy to work with Device objects

* cisco-pkg
    * testbed teardown
        * Made orchestrator argument optional
        * Added feature to extract orchestrator from custom key on testbed yaml

* pyats.cisco
    * Fix TIMS upload for Logical ID


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats.easypy
    * Add job and task level result rollup in easypy report.
    * remove the uids from unknown args if there is rerun file


