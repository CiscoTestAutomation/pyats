March 2023
==========

March 28 - Pyats v23.3 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.3 
    ``pyats.aereport``, v23.3 
    ``pyats.aetest``, v23.3 
    ``pyats.async``, v23.3 
    ``pyats.cisco``, v23.3 
    ``pyats.connections``, v23.3 
    ``pyats.datastructures``, v23.3 
    ``pyats.easypy``, v23.3 
    ``pyats.kleenex``, v23.3 
    ``pyats.log``, v23.3 
    ``pyats.reporter``, v23.3 
    ``pyats.results``, v23.3 
    ``pyats.robot``, v23.3 
    ``pyats.tcl``, v23.3 
    ``pyats.topology``, v23.3 
    ``pyats.utils``, v23.3 

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

* pyats.manifest
    * Add support for CLI arguments with * as value

* pyats.utils
    * Fixed default value with CLI markup usage


