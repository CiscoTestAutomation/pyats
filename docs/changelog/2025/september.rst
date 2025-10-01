September 2025
==========

September 30 - Pyats v25.9

------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v25.9 
    ``pyats.aereport``, v25.9 
    ``pyats.aetest``, v25.9 
    ``pyats.async``, v25.9 
    ``pyats.cisco``, v25.9 
    ``pyats.connections``, v25.9 
    ``pyats.datastructures``, v25.9 
    ``pyats.easypy``, v25.9 
    ``pyats.kleenex``, v25.9 
    ``pyats.log``, v25.9 
    ``pyats.reporter``, v25.9 
    ``pyats.results``, v25.9 
    ``pyats.robot``, v25.9 
    ``pyats.tcl``, v25.9 
    ``pyats.topology``, v25.9 
    ``pyats.utils``, v25.9 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* pyats.topology
    * Enhanced TopologyDict.get() to support alias based lookups in addition to keys

* pyats.devat
    * Update the check for device console to exempt windows devices, and Update the exempt VRF models to include c9800cl and c9800cl.

* reporter
    * Added handling for issues encountered while terminating a client unexptectedly


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats.devat
    * Add a new method `Update_device_compliance_attribute` to update the device compliance attribute for devices based on their compliance status.

* pyats.utils
    * Added new singleton `working_set` to utils.py to take over for deprecated `pkg_resources.working_set`.


