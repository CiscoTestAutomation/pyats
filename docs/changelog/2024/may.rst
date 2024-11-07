May 2024
==========

May 28 - Pyats v24.5 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.5 
    ``pyats.aereport``, v24.5 
    ``pyats.aetest``, v24.5 
    ``pyats.async``, v24.5 
    ``pyats.cisco``, v24.5 
    ``pyats.connections``, v24.5 
    ``pyats.datastructures``, v24.5 
    ``pyats.easypy``, v24.5 
    ``pyats.kleenex``, v24.5 
    ``pyats.log``, v24.5 
    ``pyats.reporter``, v24.5 
    ``pyats.results``, v24.5 
    ``pyats.robot``, v24.5 
    ``pyats.tcl``, v24.5 
    ``pyats.topology``, v24.5 
    ``pyats.utils``, v24.5 

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

* pyats.cisco
    * Update package discovery error handling
    * Update ABS URL, add environment variable lookup


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* kleenex/worker
    * Updated logic to make device alias name as default in reporter.

* pyats/topology
    * schema
        * Update topology schema for rommon information.

* clean
    * schema
        * Updated clean schema with resources section with memory and cpu.

* cisco/commands/testbed
    * bringup
        * Updated logic to pull the dyntopo worker arguments dynamically.

* cisco/commands
    * testbed/export
        * Added export subcommand to export the testbed data using laasv2


