July 2023
==========

July 24 - Pyats v23.7 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.7 
    ``pyats.aereport``, v23.7 
    ``pyats.aetest``, v23.7 
    ``pyats.async``, v23.7 
    ``pyats.cisco``, v23.7 
    ``pyats.connections``, v23.7 
    ``pyats.datastructures``, v23.7 
    ``pyats.easypy``, v23.7 
    ``pyats.kleenex``, v23.7 
    ``pyats.log``, v23.7 
    ``pyats.reporter``, v23.7 
    ``pyats.results``, v23.7 
    ``pyats.robot``, v23.7 
    ``pyats.tcl``, v23.7 
    ``pyats.topology``, v23.7 
    ``pyats.utils``, v23.7 

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

* ats.kleenex
    * Allow users to override device `type` and `alias` with values from logical testbed


