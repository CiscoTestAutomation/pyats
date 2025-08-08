July 2025
==========

July 29 - Pyats v25.7 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v25.7 
    ``pyats.aereport``, v25.7 
    ``pyats.aetest``, v25.7 
    ``pyats.async``, v25.7 
    ``pyats.cisco``, v25.7 
    ``pyats.connections``, v25.7 
    ``pyats.datastructures``, v25.7 
    ``pyats.easypy``, v25.7 
    ``pyats.kleenex``, v25.7 
    ``pyats.log``, v25.7 
    ``pyats.reporter``, v25.7 
    ``pyats.results``, v25.7 
    ``pyats.robot``, v25.7 
    ``pyats.tcl``, v25.7 
    ``pyats.topology``, v25.7 
    ``pyats.utils``, v25.7 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* cisco-pkg
    * Loading clean_config during _get_bringup_config

* pyats.cisco
    * Updated default email server to be `outbound.cisco.com` due to deprecation of `mail.cisco.com`.

* pyats.clean
    * Modified clean loader to load JIT config when using templates

* pyats.topology
    * Added timeout key to testbed.servers section

* easypy-pkg
    * Added a check to find clean.extra.yaml and treat it as a jit clean for standalone bringup

* pyats
    * Refactor plugin loading from pkg_resources.iter_entry_points to importlib.metadata.entry_points

* pyats.devat
    * device compliance
        * add check for power cycle
        * exempt linux device from some checks


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats
    * Added new CLI argument '--clean-model-image' which we can pass the list images with model name


