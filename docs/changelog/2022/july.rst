July 2022
==========

July 21 - Pyats v22.7 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.7 
    ``pyats.aereport``, v22.7 
    ``pyats.aetest``, v22.7 
    ``pyats.async``, v22.7 
    ``pyats.cisco``, v22.7 
    ``pyats.connections``, v22.7 
    ``pyats.datastructures``, v22.7 
    ``pyats.easypy``, v22.7 
    ``pyats.kleenex``, v22.7 
    ``pyats.log``, v22.7 
    ``pyats.reporter``, v22.7 
    ``pyats.results``, v22.7 
    ``pyats.robot``, v22.7 
    ``pyats.tcl``, v22.7 
    ``pyats.topology``, v22.7 
    ``pyats.utils``, v22.7 

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

* pyats.topology
    * Update schema to correctly reflect peripheral structure

* pyats.easypy
    * Modified MailBot:
        * Enabled {runtime} formatting for custom subjects on CLI
        * Added `email.subject` configuration option

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* ats.devat
    * Add DevAT package to pyats repo


