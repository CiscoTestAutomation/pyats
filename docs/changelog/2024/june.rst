June 2024
==========

 - Pyats v24.6 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.6 
    ``pyats.aereport``, v24.6 
    ``pyats.aetest``, v24.6 
    ``pyats.async``, v24.6 
    ``pyats.cisco``, v24.6 
    ``pyats.connections``, v24.6 
    ``pyats.datastructures``, v24.6 
    ``pyats.easypy``, v24.6 
    ``pyats.kleenex``, v24.6 
    ``pyats.log``, v24.6 
    ``pyats.reporter``, v24.6 
    ``pyats.results``, v24.6 
    ``pyats.robot``, v24.6 
    ``pyats.tcl``, v24.6 
    ``pyats.topology``, v24.6 
    ``pyats.utils``, v24.6 

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

* easy/plugins
    * kleenex
        * Fixed clean default image issue.
    * kleenex
        * Fixed clean default image where multiple images being passed to each device, instead

* kleenex
    * clean/loader
        * Fixed a bug with clean templates, where it was not updating the clean image properly.

* topology
    * Modified schema
        * Added submodel key in device schema


