September 2022
==========

September 27 - Pyats v22.9
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.9
    ``pyats.aereport``, v22.9
    ``pyats.aetest``, v22.9
    ``pyats.async``, v22.9
    ``pyats.cisco``, v22.9
    ``pyats.connections``, v22.9
    ``pyats.datastructures``, v22.9
    ``pyats.easypy``, v22.9
    ``pyats.kleenex``, v22.9
    ``pyats.log``, v22.9
    ``pyats.reporter``, v22.9
    ``pyats.results``, v22.9
    ``pyats.robot``, v22.9
    ``pyats.tcl``, v22.9
    ``pyats.topology``, v22.9
    ``pyats.utils``, v22.9

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


* pyats.topology
    * Fixed return exit code for pyats validate testbed

* pyats installer
    * Updated pyATS installer
    * Pinned installer dependencies
    * Refactor installer builder

* pyats.cli
    * Updated cmd implementation, added encoding and ignoring errors
    * Log output of failed commands if available

* pyats.easypy
    * Add support for clean files and logical testbed per task

* easypy
    * Modified Task
    * Improved terminate to kill any subprocesses that remain after attempting to terminate


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* pyats
    * Pinned pip version to use pip index versions
    * Added wrapper for required, legacy and optional packages

* pyats.cli.commands.version
    * Added CheckAvailableVersions
        * Created method to get all available versions of a package
        * Created method to get the latest version of a list of packages

* Modified update
    * Added latest version to dialog confirming which packages will be updated
    * Added --pre argument to fetch minor and dev versions

