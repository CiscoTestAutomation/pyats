August 2022
==========

August 26 - Pyats v22.8 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.8 
    ``pyats.aereport``, v22.8 
    ``pyats.aetest``, v22.8 
    ``pyats.async``, v22.8 
    ``pyats.cisco``, v22.8 
    ``pyats.connections``, v22.8 
    ``pyats.datastructures``, v22.8 
    ``pyats.easypy``, v22.8 
    ``pyats.kleenex``, v22.8 
    ``pyats.log``, v22.8 
    ``pyats.reporter``, v22.8 
    ``pyats.results``, v22.8 
    ``pyats.robot``, v22.8 
    ``pyats.tcl``, v22.8 
    ``pyats.topology``, v22.8 
    ``pyats.utils``, v22.8 

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
    * Fixed task-uids filter when using default Task IDs (e.g. Task-2)

* pyats.manifest
    * Add support for boolean overrides with `pyats manifest` CLI command

* manifest
    * combine_cli_args_and_script_arguments
        * Handling for any number of uses of the ``--meta`` argument

* pyats.topology
    * Updated testbed.raw_config to contain post-extend, post-markup content. This fixes issues introduced by previous changes when using Genie jinja configure and YAML reference markup.

* pyats.utils
    * Updated schemaengine to support optional advanced datatypes
    * Updated yaml loader to support advanced datatypes argument
    * Updated yaml loader to store raw/pre/mark/validated/post content


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* ats.cisco
    * bussinesstelemetry
        * Updated get_paches for collecting package from requirements.txt


