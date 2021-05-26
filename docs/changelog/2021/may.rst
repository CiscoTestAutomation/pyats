
May 2021
========

May 25, 2021
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.5
    ``pyats.aereport``, v21.5
    ``pyats.aetest``, v21.5
    ``pyats.async``, v21.5
    ``pyats.cisco``, v21.5
    ``pyats.connections``, v21.5
    ``pyats.datastructures``, v21.5
    ``pyats.easypy``, v21.5
    ``pyats.kleenex``, v21.5
    ``pyats.log``, v21.5
    ``pyats.reporter``, v21.5
    ``pyats.results``, v21.5
    ``pyats.robot``, v21.5
    ``pyats.tcl``, v21.5
    ``pyats.topology``, v21.5
    ``pyats.utils``, v21.5

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Feature List
^^^^^^^^^^^^

* utils
    * Created pyats.utils.yaml.utils
        * yaml_lookup_by_key_path allows nodes in parsed YAML data to be looked up using a list of keys
        * yaml_apply_map_to_paths allows a mapping to be applied to nodes within parsed YAML data
    * Added set_dict_by_key_path
        * Added set_dict_by_key_path function for inserting data into nested dictionaries, and for appending to lists within nested dictionaries

* Cisco Command    
    * Added upload subcommand:
        * Added logs upload subcommand (for internal use only) to upload logs
    * Added uploadhelper module:
        * Added reusable method to upload log archives
        
* Trade
    * Modified _upload_pyats_results:
        * Using post method from uploadhelper module
        
* Log
    * Modified Logs command:
        * Added upload subcommand (for internal use only)


Other Changes
^^^^^^^^^^^^^

* kleenex
    * Modified loader
        * Replace device aliases with real device names as first preprocessing stage of YAML clean file
        * Update how images provided on CLI are copied into the parsed clean file. Images provided on the CLI now override images provided in the YAML file. A number of logic errors in how the CLI images were parsed were fixed
        * Update tests to exercise the code which parses images from the CLI

* easypy
    * Modified test_kleenex_plugin
        * Updated expected 'images' key in YAML clean file so that it matches the schema provided in the documentation

* utils
    * Modified yaml loader to preserve order if specified
    * Modified markup.py:
        * Fixed bug where called the markup `${testbed}` multiple times would cause the run to slow down
            * Variable values are now stored for future use

* topology
    * Modified connection manager logic to determine via for a single connection

* dependencies
    * Updated version pinning for dependent packages
