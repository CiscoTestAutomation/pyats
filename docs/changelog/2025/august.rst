August 2025
==========

September 30 - Pyats v25.8 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v25.8 
    ``pyats.aereport``, v25.8 
    ``pyats.aetest``, v25.8 
    ``pyats.async``, v25.8 
    ``pyats.cisco``, v25.8 
    ``pyats.connections``, v25.8 
    ``pyats.datastructures``, v25.8 
    ``pyats.easypy``, v25.8 
    ``pyats.kleenex``, v25.8 
    ``pyats.log``, v25.8 
    ``pyats.reporter``, v25.8 
    ``pyats.results``, v25.8 
    ``pyats.robot``, v25.8 
    ``pyats.tcl``, v25.8 
    ``pyats.topology``, v25.8 
    ``pyats.utils``, v25.8 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* pyats.devat
    * Update check for device console to exempt linux devices.

* pyats
    * Installer
        * Removed requirement for bitbucket token as all repositories are now public.

* markup
    * Added support for runtime yaml markup


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* kleenex
    * Added support for overriding configuration values in the clean file using the `--clean-config-override` argument. This allows users to specify configuration overrides in the format `path__to__some_key=value`, enabling dynamic adjustments to the clean configuration without modifying the original file.

* easypy
    * CLI arguments and manifest meta field support for product, component, feature, owner


