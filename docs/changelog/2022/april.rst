April 2022
==========

April 26 - Pyats v22.4 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.4 
    ``pyats.aereport``, v22.4 
    ``pyats.aetest``, v22.4 
    ``pyats.async``, v22.4 
    ``pyats.cisco``, v22.4 
    ``pyats.connections``, v22.4 
    ``pyats.datastructures``, v22.4 
    ``pyats.easypy``, v22.4 
    ``pyats.kleenex``, v22.4 
    ``pyats.log``, v22.4 
    ``pyats.reporter``, v22.4 
    ``pyats.results``, v22.4 
    ``pyats.robot``, v22.4 
    ``pyats.tcl``, v22.4 
    ``pyats.topology``, v22.4 
    ``pyats.utils``, v22.4 

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

* pyats.connections
    * Modified BaseConnection class to accept any argument to allow NotImlpemented error to propagate

* aetest
    * Modified Interaction UT
        * More robust UT for interaction feature

* pyats.utils
    * remove key.lower() in create_extended_dict

* pyats.topology
    * Modified TopologyDict class to allow attribute lookup of device aliases


