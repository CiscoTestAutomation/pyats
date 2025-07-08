June 2025
==========

June 29 - Pyats v25.6 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v25.6 
    ``pyats.aereport``, v25.6 
    ``pyats.aetest``, v25.6 
    ``pyats.async``, v25.6 
    ``pyats.cisco``, v25.6 
    ``pyats.connections``, v25.6 
    ``pyats.datastructures``, v25.6 
    ``pyats.easypy``, v25.6 
    ``pyats.kleenex``, v25.6 
    ``pyats.log``, v25.6 
    ``pyats.reporter``, v25.6 
    ``pyats.results``, v25.6 
    ``pyats.robot``, v25.6 
    ``pyats.tcl``, v25.6 
    ``pyats.topology``, v25.6 
    ``pyats.utils``, v25.6 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* topology-pkg
    * Added an optional key "order" under the testbed server schema


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* easypy
    * Replay
        * Changed the use of request_id to item_id in replay plugin

* pyats
    * kleenex
        * Moved functionality from pyats.kleenex to dyntopo
    * devat/device compliance
        * Fix the stack check to only check for devices with child devices and platform cat9k which has category as grou
        * Add support for handling lab name

* pyats.devat
    * device compliance
        * only include needed attributes
        * add option to buffer to local sqlite db before pushing records

* easypy-pkg
    * Merge the clean config from kleenex processor with the actual clean config

* topology
    * Moved `rommon` attribute to `management` attribute to avoid service conflict.

* easypy/plugins/kleenex
    * Modified Kleenex logic to add JIT clean configs.
    * Removed recursive updates which fixes clean groups.
    * Fixed markups issue.

* ats.kleenex
    * Modified bringup logic that prepares prepares testbed


--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* kleenex-pkg
    * Added result url part the kleenex run


