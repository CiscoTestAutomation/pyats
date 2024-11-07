May 2023
==========

May 30 - Pyats v23.5 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.5 
    ``pyats.aereport``, v23.5 
    ``pyats.aetest``, v23.5 
    ``pyats.async``, v23.5 
    ``pyats.cisco``, v23.5 
    ``pyats.connections``, v23.5 
    ``pyats.datastructures``, v23.5 
    ``pyats.easypy``, v23.5 
    ``pyats.kleenex``, v23.5 
    ``pyats.log``, v23.5 
    ``pyats.reporter``, v23.5 
    ``pyats.results``, v23.5 
    ``pyats.robot``, v23.5 
    ``pyats.tcl``, v23.5 
    ``pyats.topology``, v23.5 
    ``pyats.utils``, v23.5 

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

* pyats.pyats
    * Add a cli for manifest to use symlink

* pyats.easypy
    * Add checking for using symlink for the manifest
    * Update manifest execution logic to allow jobfiles to be symlinked to another folder

* aetest
    * Modified PausePdb
        * Dumps the connection information from the testbed to the console


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* easypy
    * Added suite_id to all the jobs reports
    * Add suite_name to report data from suite-name CLI argument
    * Added label and component reporting options


