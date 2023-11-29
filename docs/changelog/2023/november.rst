November 2023
==========

November 27 - Pyats v23.11
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v23.11
    ``pyats.aereport``, v23.11
    ``pyats.aetest``, v23.11
    ``pyats.async``, v23.11
    ``pyats.cisco``, v23.11
    ``pyats.connections``, v23.11
    ``pyats.datastructures``, v23.11
    ``pyats.easypy``, v23.11
    ``pyats.kleenex``, v23.11
    ``pyats.log``, v23.11
    ``pyats.reporter``, v23.11
    ``pyats.results``, v23.11
    ``pyats.robot``, v23.11
    ``pyats.tcl``, v23.11
    ``pyats.topology``, v23.11
    ``pyats.utils``, v23.11

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

* bringup.bases
    * Added authenticate method to BringUpWorkerBase
        * Class method to handle authentication before bringup

* bringup.manager
    * Modified __enter__ to authenticate
        * Authentication is done (if required) before start_server is called

* reporter
    * Modified Testsuite/Task report
        * Testsuite and Task now have an overall result in the final report


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean
    * Modified bases.py
        * Set default loglevel to be inherited from pyats

* kleenex
    * Modified kleenex package structure
        * Split kleenex into bringup, clean, kleenex
        * Bringup contains the scripts to bringup logical devices
        * Clean contains the scripts common to bringup and kleenex
        * Kleenex contains the scripts to execute clean
    * Fixed issue with kleenex loader where the `--clean-image-json` argument wouldn't allow for device aliases to be passed
    * Added unittests to verify changes

* easypy
    * Modified kleenex plugin
        * Updated references to kleenex package structure

* pyats.topology
    * Updated schema to support services for testbed servers.

* manifest
    * Fixed issue with `parse_cli_args` where the `meta` argument would get nested in lists if it was specified more than two times

* pyats.connections.bases
    * Add CLI arguments to service wrapper
    * Updated docs
    * Detached service wrapper from easypy runtime
    * Added steps to service wrapper methods to allow for reporting


