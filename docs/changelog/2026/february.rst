February 2026
==========

February 24 - Pyats v26.2 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.2 
    ``pyats.aereport``, v26.2 
    ``pyats.aetest``, v26.2 
    ``pyats.async``, v26.2 
    ``pyats.cisco``, v26.2 
    ``pyats.connections``, v26.2 
    ``pyats.datastructures``, v26.2 
    ``pyats.easypy``, v26.2 
    ``pyats.kleenex``, v26.2 
    ``pyats.log``, v26.2 
    ``pyats.reporter``, v26.2 
    ``pyats.results``, v26.2 
    ``pyats.robot``, v26.2 
    ``pyats.tcl``, v26.2 
    ``pyats.topology``, v26.2 
    ``pyats.utils``, v26.2 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* pyats.bringup
    * Fix interface naming in _populate_enhanced_logical_testbed_config
        * Use logical_intf_key instead of logical_intf_name for actual_intf_name assignment
        * Resolves issue where interfaces with alias different from key were incorrectly named
    * Fixed interface alias causing empty topology during testbed merge.
    * Used original interface key instead of redirected alias for dev_intf_xref lookup in _populate_enhanced_logical_testbed_config.

* log-pkg
    * Fix asyncio deprecation warning for python 3.14

* kleenex-pkg
    * Fix asyncio deprecation warning for python 3.14

* reporter-pkg
    * Fix asyncio deprecation warning for python 3.14

* cisco-pkg
    * Rest
        * change the protocol from http to https for tims upload in order to avoid the redirection issue.

* devat-pkg
    * DeviceCompliance
        * Add support for `PYATS_DEV_COMPLIANCE_EXTRA_ATTRS` environment variable, which is a comma separated list of additional attributes which will be included for each device payload published to business telemetry topic
        * internal support for OAuth authentication in Kafka client

* pyats
    * Fix UT for python support 3.14


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* topology-pkg
    * Updated topology/loader/base.py
        * Added schema support for segments.


