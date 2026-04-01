March 2026
==========

March 31 - Pyats v26.3 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.3 
    ``pyats.aereport``, v26.3 
    ``pyats.aetest``, v26.3 
    ``pyats.async``, v26.3 
    ``pyats.cisco``, v26.3 
    ``pyats.connections``, v26.3 
    ``pyats.datastructures``, v26.3 
    ``pyats.easypy``, v26.3 
    ``pyats.kleenex``, v26.3 
    ``pyats.log``, v26.3 
    ``pyats.reporter``, v26.3 
    ``pyats.results``, v26.3 
    ``pyats.robot``, v26.3 
    ``pyats.tcl``, v26.3 
    ``pyats.topology``, v26.3 
    ``pyats.utils``, v26.3 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* pyats.clean
    * Modified _preprocess_add_cli_images in BaseKleenexFileLoader
        * Added warning when --clean-device-image specifies a hostname or alias

* aetst-pkg
    * Modified Steps
        * Changed raise signals.XXXX(reason, data,...) to raise signals.XXXX(reason, data=data,...)

* kleenex-pkg
    * Updated the logic to update device recovery information on template action ignore.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* easypy/debug.py
    * Added support for ``env.hide_list`` in pyATS configuration (``pyats.conf``) under


