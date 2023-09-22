September 2023
==========

September 26 - Pyats v23.9 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.9 
    ``pyats.aereport``, v23.9 
    ``pyats.aetest``, v23.9 
    ``pyats.async``, v23.9 
    ``pyats.cisco``, v23.9 
    ``pyats.connections``, v23.9 
    ``pyats.datastructures``, v23.9 
    ``pyats.easypy``, v23.9 
    ``pyats.kleenex``, v23.9 
    ``pyats.log``, v23.9 
    ``pyats.reporter``, v23.9 
    ``pyats.results``, v23.9 
    ``pyats.robot``, v23.9 
    ``pyats.tcl``, v23.9 
    ``pyats.topology``, v23.9 
    ``pyats.utils``, v23.9 

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
                                      New                                       
--------------------------------------------------------------------------------

* pyats
    * Added BaseServiceWrapper class

* pyats.aetest
    * Added support for YAML Markup with datafiles, including testbed references

* pyats.utils
    * add new function chainattrget
    * Added duplicate key detection in yaml loader

* pyats.easypy
    * Added section result statistics to job report


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* pyats.kleenex
    * Update device name mapping logic to support missing entries from orchestrator
    * Fix device names used with actual testbed vs logical testbed for use with clean image overrides

* pyats.topology
    * Updated management schema type for protocols.

* pyats.utils
    * Updated implementation of enforce_max_key_value_length to support hierarchical dictionaries

* kleenex
    * Modified KleenexMarkupProcessor
        * Delayed processing of testbed markups to support logical testbeds
    * Modified kleenex_main
        * Reloaded clean file to process testbed markups after topology bringup

* easypy
    * Modified Kleenex Plugin
        * Reloaded clean file to process testbed markups after topology bringup


