January 2022
==========

January 25 - Pyats v22.1
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.1 
    ``pyats.aereport``, v22.1 
    ``pyats.aetest``, v22.1 
    ``pyats.async``, v22.1 
    ``pyats.cisco``, v22.1 
    ``pyats.connections``, v22.1 
    ``pyats.datastructures``, v22.1 
    ``pyats.easypy``, v22.1 
    ``pyats.kleenex``, v22.1 
    ``pyats.log``, v22.1 
    ``pyats.reporter``, v22.1 
    ``pyats.results``, v22.1 
    ``pyats.robot``, v22.1 
    ``pyats.tcl``, v22.1 
    ``pyats.topology``, v22.1 
    ``pyats.utils``, v22.1 

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
                                      Fix                                       
--------------------------------------------------------------------------------

* kleenex
    * Modified Arguments
        * Restored creation of timestamped subdirectory for runinfo and archives
    * Added Argument
        * `--no-archive-subdir` argument to disable creating the `yy-mm`

* pyats.utils
    * Support local address discovery for dynamic file servers using device.spawn object
    * Fix credentials for http file copy
    * Increase dict value limit check from 255 to 512

* pyats
    * Added packaging dependency

* reporter/utils
    * Updated regex in 'normalize_git_url()'
        * To have proper site url for git repository


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* kleenex
    * Kleenex_main
        * Added email report support for clean


