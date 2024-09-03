August 2024
==========

August 27 - Pyats v24.8 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.8 
    ``pyats.aereport``, v24.8 
    ``pyats.aetest``, v24.8 
    ``pyats.async``, v24.8 
    ``pyats.cisco``, v24.8 
    ``pyats.connections``, v24.8 
    ``pyats.datastructures``, v24.8 
    ``pyats.easypy``, v24.8 
    ``pyats.kleenex``, v24.8 
    ``pyats.log``, v24.8 
    ``pyats.reporter``, v24.8 
    ``pyats.results``, v24.8 
    ``pyats.robot``, v24.8 
    ``pyats.tcl``, v24.8 
    ``pyats.topology``, v24.8 
    ``pyats.utils``, v24.8 

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

* cisco
    * Modified ixia.py
        * Added check to ensure package import

* pyats.utils
    * Modified _iter_mutable_mapping
        * Updated datafile markup processing to handle "%{testbed}" markup

* pyats.kleenex
    * Removed devices with no interfaces defined from the topology in the testbed configuration


