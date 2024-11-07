August 2023
==========

August 29 - Pyats v23.8
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.8
    ``pyats.aereport``, v23.8
    ``pyats.aetest``, v23.8
    ``pyats.async``, v23.8
    ``pyats.cisco``, v23.8
    ``pyats.connections``, v23.8
    ``pyats.datastructures``, v23.8
    ``pyats.easypy``, v23.8
    ``pyats.kleenex``, v23.8
    ``pyats.log``, v23.8
    ``pyats.reporter``, v23.8
    ``pyats.results``, v23.8
    ``pyats.robot``, v23.8
    ``pyats.tcl``, v23.8
    ``pyats.topology``, v23.8
    ``pyats.utils``, v23.8

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

* pyats.aetest
    * Added support for YAML Markup with datafiles, including testbed references

* pyats.utils
    * add new function chainattrget

* pyats.easypy
    * Added section result statistics to job report


--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* pyats.kleenex
    * Update device name mapping logic to support missing entries from orchestrator
    * Fix device names used with actual testbed vs logical testbed for use with clean image overrides

* pyats.utils
    * Updated implementation of enforce_max_key_value_length to support hierarchical dictionaries


