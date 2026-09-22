November 2024
==========

November 26 - Pyats v24.11
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.11
    ``pyats.aereport``, v24.11
    ``pyats.aetest``, v24.11
    ``pyats.async``, v24.11
    ``pyats.cisco``, v24.11
    ``pyats.connections``, v24.11
    ``pyats.datastructures``, v24.11
    ``pyats.easypy``, v24.11
    ``pyats.kleenex``, v24.11
    ``pyats.log``, v24.11
    ``pyats.reporter``, v24.11
    ``pyats.results``, v24.11
    ``pyats.robot``, v24.11
    ``pyats.tcl``, v24.11
    ``pyats.topology``, v24.11
    ``pyats.utils``, v24.11




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* pyats core
    * Modified version update
        * Allow for a list of pypi servers to be used for updating to enable fallback

* cisco
    * trade
        * add logging when the upload to taas is failed
    * Modified Testbed Exporter
        * Updated call to convert_to_pyats as it is now an async function


