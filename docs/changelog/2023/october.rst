October 2023
==========

October 31 - Pyats v23.10
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.10
    ``pyats.aereport``, v23.10
    ``pyats.aetest``, v23.10
    ``pyats.async``, v23.10
    ``pyats.cisco``, v23.10
    ``pyats.connections``, v23.10
    ``pyats.datastructures``, v23.10
    ``pyats.easypy``, v23.10
    ``pyats.kleenex``, v23.10
    ``pyats.log``, v23.10
    ``pyats.reporter``, v23.10
    ``pyats.results``, v23.10
    ``pyats.robot``, v23.10
    ``pyats.tcl``, v23.10
    ``pyats.topology``, v23.10
    ``pyats.utils``, v23.10

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

* pyats.kleenex
    * Modified markup processor to use chainattrget utility function to allow object attribute and key lookup

* easypy
    * Modified update_job
        * Modified update_job to format elapsedtime


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* topology
    * Updated schema for fallback credentials
        * Add fallback credentials under connection


