June 2026
==========

June 30 - Pyats v26.6 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.6 
    ``pyats.aereport``, v26.6 
    ``pyats.aetest``, v26.6 
    ``pyats.async``, v26.6 
    ``pyats.cisco``, v26.6 
    ``pyats.connections``, v26.6 
    ``pyats.datastructures``, v26.6 
    ``pyats.easypy``, v26.6 
    ``pyats.kleenex``, v26.6 
    ``pyats.log``, v26.6 
    ``pyats.reporter``, v26.6 
    ``pyats.results``, v26.6 
    ``pyats.robot``, v26.6 
    ``pyats.tcl``, v26.6 
    ``pyats.topology``, v26.6 
    ``pyats.utils``, v26.6 




Changelogs
^^^^^^^^^^--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* cisco
    * Modified onedevx.py
        * Deprecate Trade and replace with OneDevx

* topology
    * Added ``Segment`` topology objects
        * Interfaces can reference ``segment`` entries from testbed YAML.
        * Devices and testbeds now expose connected segments through
        * Interface ``link`` and ``segment`` references are mutually exclusive.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* reporter
    * Modified TestSuite
        * Included ``ignore true`` for ignored testcases in YAML report output.
    * Add optional_reporter to utils
    * Modified TestSuite
        * Excluded testcases marked with ``ignore true`` from testcase and section report summary counts.


