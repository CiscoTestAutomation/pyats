January 2024
==========

30 - Pyats v24.1 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.1 
    ``pyats.aereport``, v24.1 
    ``pyats.aetest``, v24.1 
    ``pyats.async``, v24.1 
    ``pyats.cisco``, v24.1 
    ``pyats.connections``, v24.1 
    ``pyats.datastructures``, v24.1 
    ``pyats.easypy``, v24.1 
    ``pyats.kleenex``, v24.1 
    ``pyats.log``, v24.1 
    ``pyats.reporter``, v24.1 
    ``pyats.results``, v24.1 
    ``pyats.robot``, v24.1 
    ``pyats.tcl``, v24.1 
    ``pyats.topology``, v24.1 
    ``pyats.utils``, v24.1 

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

* kleenex
    * Fixed issue with kleenex loader handling device alias

* pyats.configuration
    * Removed pyATS Configuration object from sys.modules, refactored usage
        * Change "from pyats import configuration" to "from pyats.configuration import configuration"

* log-pkg
    * commands
        * remove aiohttp-swagger and its references to resolve markupsafe errors

* pyats.utils
    * Updated YAML markup processor to support markup in dictionary keys

* easypy
    * Removed
        * Removed duplicate Task Result Details and Task Result Summary

* pyats.topology
    * Updated management schema type for address and gateway.

* pyats.kleenex
    * Modified p_reference_markup
        * Parse credentials on testbed.raw_config


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* easypy.plugins
    * kleenex.py
        * Added preprocessor logic to update default clean image

* cisco.commands
    * Added pyats testbed teardown
        * Added command to teardown topology using dyntopo orchestrators
    * Added pyats testbed bringup
        * Added command to bringup topology using dyntopo orchestrators

* easypy
    * AEReporter
        * add skipped to AEPluginReporter
    * Kleenex
        * Add skip-teardown-on-failure argument to skip teardown when success rate is below 100%

* pyats.utils
    * Added load_dict_from_list
        * Added support for meta argument if passed as a list
    * Support keyword argument (kwarg) syntax with CALLABLE YAML markup

* bringup.bases
    * Added skip_teardown argument
        * Added argument to skip topology teardown after clean/bringup execution.

* easypy.plugins.kleenex
    * Added skip_teardown argument
        * Added argument to skip topology teardown after test case execution.


