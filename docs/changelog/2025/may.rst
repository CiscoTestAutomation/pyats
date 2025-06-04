May 2025
==========

 - Pyats v25.5 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v25.5 
    ``pyats.aereport``, v25.5 
    ``pyats.aetest``, v25.5 
    ``pyats.async``, v25.5 
    ``pyats.cisco``, v25.5 
    ``pyats.connections``, v25.5 
    ``pyats.datastructures``, v25.5 
    ``pyats.easypy``, v25.5 
    ``pyats.kleenex``, v25.5 
    ``pyats.log``, v25.5 
    ``pyats.reporter``, v25.5 
    ``pyats.results``, v25.5 
    ``pyats.robot``, v25.5 
    ``pyats.tcl``, v25.5 
    ``pyats.topology``, v25.5 
    ``pyats.utils``, v25.5 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* utils
    * fileutils
        * removed fileutils logic and moved it to filetransferutils pkg in genielibs.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* reporter
    * server
        * Changed from select.select() to select.poll() to avoid file descriptor leak
    * client
        * Added retry logic for connection to server

* easypy
    * Replace special characters in job UID with `_`
    * Ingore testscript path for rerun check

* pyats
    * Add log_level option to cmd utility function

* pyats.cisco
    * Make TIMS testcase lookup optional


