February 2022
=============

February 24 - Pyats v22.2 
-------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.2 
    ``pyats.aereport``, v22.2 
    ``pyats.aetest``, v22.2 
    ``pyats.async``, v22.2 
    ``pyats.cisco``, v22.2 
    ``pyats.connections``, v22.2 
    ``pyats.datastructures``, v22.2 
    ``pyats.easypy``, v22.2 
    ``pyats.kleenex``, v22.2 
    ``pyats.log``, v22.2 
    ``pyats.reporter``, v22.2 
    ``pyats.results``, v22.2 
    ``pyats.robot``, v22.2 
    ``pyats.tcl``, v22.2 
    ``pyats.topology``, v22.2 
    ``pyats.utils``, v22.2 

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
    * Kleenex_main
        * Fixed the unwanted email being sent by UT.

* topology
    * Modified schema.py
        * Added new device abstraction keys to production_schema definition

* all
    * Modified Makefile
        * Pinned 'packaging' to be version 20.0 or higher in dependencies

* pyats
    * Modified setup.py
        * Pinned 'packaging' to be version 20.0 or higher in install_requires

* pyats.manifest
    * Update manifest validate command to handle multiple files as arguments

* pyats.results
    * Check object type when setting name to avoid reporter errors

* pyats.utils
    * Add timezone info to timestamps

* fileutils
    * Fix address lookup if the passed server is not in the testbed server section


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* utils
    * Updated YAML loader
        * Added a way to pass http token to get a file over http/https

* aetest
    * Updated order of post processor runs
        * pyATS Health Checks post-processor will run after user's processors

* topology
    * Updated loader
        * testbed.raw_config is added even in case of YAML loading


