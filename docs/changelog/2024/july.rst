July 2024
==========

July 30 - Pyats v24.7 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.7 
    ``pyats.aereport``, v24.7 
    ``pyats.aetest``, v24.7 
    ``pyats.async``, v24.7 
    ``pyats.cisco``, v24.7 
    ``pyats.connections``, v24.7 
    ``pyats.datastructures``, v24.7 
    ``pyats.easypy``, v24.7 
    ``pyats.kleenex``, v24.7 
    ``pyats.log``, v24.7 
    ``pyats.reporter``, v24.7 
    ``pyats.results``, v24.7 
    ``pyats.robot``, v24.7 
    ``pyats.tcl``, v24.7 
    ``pyats.topology``, v24.7 
    ``pyats.utils``, v24.7 

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

* pyats.utils
    * Modified argv parser helper function
        * Ignore arguments after `--`
        * Allow `-` to be passed as a value

* pyats.cli
    * Modified version update
        * Ignore packages that have no matching version


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats.reporter
    * update the log offset for each sub process

* pyats
    * remove init file for declaring namespaces for all the packages to avoid deprecation messages.


