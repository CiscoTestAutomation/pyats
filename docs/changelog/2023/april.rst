April 2023
==========

April 25 - Pyats v23.4 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.4 
    ``pyats.aereport``, v23.4 
    ``pyats.aetest``, v23.4 
    ``pyats.async``, v23.4 
    ``pyats.cisco``, v23.4 
    ``pyats.connections``, v23.4 
    ``pyats.datastructures``, v23.4 
    ``pyats.easypy``, v23.4 
    ``pyats.kleenex``, v23.4 
    ``pyats.log``, v23.4 
    ``pyats.reporter``, v23.4 
    ``pyats.results``, v23.4 
    ``pyats.robot``, v23.4 
    ``pyats.tcl``, v23.4 
    ``pyats.topology``, v23.4 
    ``pyats.utils``, v23.4 

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

* pyats.easypy
    * Update the plugin loading in the plugins and update the black_box test.

* install
    * Fix for installer to source venv for pip format json command.

* update
    * Fix to pick up ats packages instead of pyats


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* easypy
    * moved AEPluginReporter and AEPluginContext and report_func Wrapper from Plugin Bundle
        * move the reporter from plugin bundle to easypy reporter


