February 2023
==========

February 28 - Pyats v23.2 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.2 
    ``pyats.aereport``, v23.2 
    ``pyats.aetest``, v23.2 
    ``pyats.async``, v23.2 
    ``pyats.cisco``, v23.2 
    ``pyats.connections``, v23.2 
    ``pyats.datastructures``, v23.2 
    ``pyats.easypy``, v23.2 
    ``pyats.kleenex``, v23.2 
    ``pyats.log``, v23.2 
    ``pyats.reporter``, v23.2 
    ``pyats.results``, v23.2 
    ``pyats.robot``, v23.2 
    ``pyats.tcl``, v23.2 
    ``pyats.topology``, v23.2 
    ``pyats.utils``, v23.2 

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

* pyats.utils
    * Modified %CLI markup
        * Added support for default value, including list syntax support

* install
    * Updated the pyats installer.
        * The installer can now install all the required and optional packages.

* topology
    * Updated the schema to support management apis


