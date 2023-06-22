June 2023
==========

June 27 - Pyats v23.6 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.6 
    ``pyats.aereport``, v23.6 
    ``pyats.aetest``, v23.6 
    ``pyats.async``, v23.6 
    ``pyats.cisco``, v23.6 
    ``pyats.connections``, v23.6 
    ``pyats.datastructures``, v23.6 
    ``pyats.easypy``, v23.6 
    ``pyats.kleenex``, v23.6 
    ``pyats.log``, v23.6 
    ``pyats.reporter``, v23.6 
    ``pyats.results``, v23.6 
    ``pyats.robot``, v23.6 
    ``pyats.tcl``, v23.6 
    ``pyats.topology``, v23.6 
    ``pyats.utils``, v23.6 

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

* pyats.easypy
    * Fixed issue with multiprocessing causing socket usage collisions

* pyats.kleenex
    * Updated bringup logic to allow users to specify any interface type


