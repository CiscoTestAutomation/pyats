June 2022
==========

June 27 - Pyats v22.6 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.6 
    ``pyats.aereport``, v22.6 
    ``pyats.aetest``, v22.6 
    ``pyats.async``, v22.6 
    ``pyats.cisco``, v22.6 
    ``pyats.connections``, v22.6 
    ``pyats.datastructures``, v22.6 
    ``pyats.easypy``, v22.6 
    ``pyats.kleenex``, v22.6 
    ``pyats.log``, v22.6 
    ``pyats.reporter``, v22.6 
    ``pyats.results``, v22.6 
    ``pyats.robot``, v22.6 
    ``pyats.tcl``, v22.6 
    ``pyats.topology``, v22.6 
    ``pyats.utils``, v22.6 

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
    * Task
        * Display a warning when a task is run with a testbed argument
    * Update manifest logic to support IXIA_VERSION environment variable

* pyats.aetest
    * TestScript
        * Added testbed as an internal parameter for TestScripts so that it cannot be overwritten

* pyats.topology
    * Avoid processing markup for secret string and credential objects
    * Fix the testbed.raw_config for markup resolution when using `extends` in yaml file


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats/cisco/commands
    * Added --meta arguments
        * Added --meta arguments for pyats replay
            * use case of the --meta If user wanted re-run a request, they want to append extra --meta

* pyats/manifest
    * fix cli argument overriding bug
    * Added unit test to cover the argument overriding use case


