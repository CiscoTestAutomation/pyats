January 2026
==========

 - Pyats v26.1 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.1 
    ``pyats.aereport``, v26.1 
    ``pyats.aetest``, v26.1 
    ``pyats.async``, v26.1 
    ``pyats.cisco``, v26.1 
    ``pyats.connections``, v26.1 
    ``pyats.datastructures``, v26.1 
    ``pyats.easypy``, v26.1 
    ``pyats.kleenex``, v26.1 
    ``pyats.log``, v26.1 
    ``pyats.reporter``, v26.1 
    ``pyats.results``, v26.1 
    ``pyats.robot``, v26.1 
    ``pyats.tcl``, v26.1 
    ``pyats.topology``, v26.1 
    ``pyats.utils``, v26.1 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* cisco-pkg
    * Added log.info to print the request pyats sent to tims.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* pyats.kleenex
    * Update logic for update_interface_with_same_name
        * update the logic to handle interfaces with same alias as well as same name
    * Enable YAML extends when loading logical testbeds in bringup.

* devat-pkg
    * DeviceCompliance
        * Removed telnet from required management protocols for DevAT device compliance.
    * DeviceCompliance
        * Updated the handeling for management interface attributes to handle the vrf check in rommon device.

* pyats-pkg
    * Modified get_required_packages
        * Added genie.lamp as a required package for Python >= 3.10, with version markers so it is only installed on supported Python versions.
    * Updated version update installer
        * Use shlex.quote when activating the virtualenv and running pip so environment markers like "; python_version >= '3.10'" are handled safely.
        * Removed the legacy ILLEGAL_CMD_CHARACTERS check.

* topology-pkg
    * Updated setup.py
        * Pinned 'pathspec' to 0.12.1
    * schema
        * Added 'vlan' & 'switchport' optional fields to 'management' under 'device' schema.

* makefile
    * Updated DEPENDENCIES
        * Pinned 'pathspec' to 0.12.1

* aetest
    * main
        * Fixed issue where datafile loading errors were not properly marking tasks
        * Added proper exception handling for DatafileError in main.py to return
        * Added conditional check for reporter.client attribute to support both

* pyats.log
    * Updated yaml parser to handle missing data

* connections/manager
    * instantiate
        * Updated the handling of connection kwargs to ensure proper passing of kwargs when establishing connections

* easypy-pkg
    * Updated setuptools requirement to >=76.0.0,<80.0.0 to fix DistributionNotFound error


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* aetest
    * Added --exclude-uids argument
        * New CLI argument to exclude specific test sections from execution
        * Excluded sections are marked as SKIPPED in test results

* devat
    * Added check for recovery image for LUX for device compliance
        * New compliance check to verify presence of recovery image on LUX devices


