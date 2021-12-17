December 2021
==========

December 14 - Pyats v21.12
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.12
    ``pyats.aereport``, v21.12
    ``pyats.aetest``, v21.12
    ``pyats.async``, v21.12
    ``pyats.cisco``, v21.12
    ``pyats.connections``, v21.12
    ``pyats.datastructures``, v21.12
    ``pyats.easypy``, v21.12
    ``pyats.kleenex``, v21.12
    ``pyats.log``, v21.12
    ``pyats.reporter``, v21.12
    ``pyats.results``, v21.12
    ``pyats.robot``, v21.12
    ``pyats.tcl``, v21.12
    ``pyats.topology``, v21.12
    ``pyats.utils``, v21.12

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

* aetest
    * Added script type info to the report

* clean
    * Modified kleenex_main
        * logs are no longer saved in the current working directory
        * Added runinfo_dir and archive_dir arguments

* cisco
    * Modified uploadtaas.py
        * Handled exception when requests does not return a proper JSON response.
    * Fixed path handling for TCL info

* easypy
    * Updated easypy replay plugin to add meta info to the report as extra info
    * Modified manifest execution to use job file location as working directory

* reporter
    * Modified get_git_info
        * Fixed retrieving git info for a bad path or a compiled script
    * Modified package dependency for gitpython to version <= 3.1.18 for compatibility with python 3.6
    * Added caching to get_git_info() for speed up

* pyats.reporter
    * Update git info exception handling

* pyats
    * Fixed 'pyats version update' to upgrade with minor packages properly when specifying version


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* kleenex
    * Added groups by os feature

* pyats.cisco
    * Added `pyats replay` command for Cisco internal use

* logs
    * Allow switching logviewer to dark mode
