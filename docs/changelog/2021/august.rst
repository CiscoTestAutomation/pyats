August 2021
========

August 31, 2021
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.8
    ``pyats.aereport``, v21.8
    ``pyats.aetest``, v21.8
    ``pyats.async``, v21.8
    ``pyats.cisco``, v21.8
    ``pyats.connections``, v21.8
    ``pyats.datastructures``, v21.8
    ``pyats.easypy``, v21.8
    ``pyats.kleenex``, v21.8
    ``pyats.log``, v21.8
    ``pyats.reporter``, v21.8
    ``pyats.results``, v21.8
    ``pyats.robot``, v21.8
    ``pyats.tcl``, v21.8
    ``pyats.topology``, v21.8
    ``pyats.utils``, v21.8

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Feature List
^^^^^^^^^^^^

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* cisco
    * Modified get_hostinfo
        * updated for the os_ver_short and os_ver_full
    * Added get_pkg_version
        * Get version of specified packag
    * Added build_import_pkgs_list
        * build import package
    * Added get_tcl_tracker_data
        * collecting tcl proc data
    * Added get_tcl_history
        * collecting tcl history data
    * Added tcl_api_checker
        * Check if API exists in tcl collected data
    * Added tcl_history_seeker
        * Search tcl history to find APIs
    * Added get_csccon_data
        * Collecting csccon data
    * Modified build_package_repo_record
        * Modified for tcl and csccon data
    * Added preprocess_tcl_data
        * Preprocess tcl data for POST call
    * Added preprocess_tcl_history_data
        * Preprocess TCL history data for POST call
    * Added preprocess_csccon_data
        * Preprocess csccon data for POST call
    * Modified preprocess_pkg_data
        * added args for tcl and csccon
    * Modified BusinessTelemetryPlugin
        * added features for tcl and csscon
    * Added prepare_sdk_pkg
        * prepare sdk package list from pip list
    * Added pyats summary command
        * Logs out summary of job run regardless of which tool user uses
        * Summary contains status, baseline comparisons (only available for XPRESSO and SSR), etc.

* pyats
    * Added support for alternate debuggers
        * Allows a debugger to be chosen with `--pdb <debugger>`
        * Using `--pdb` without a `<debugger>` will still default to `pdb`
        * Examples
            * pyats run job job.py --pdb pudb
            * pyats run job job.py --pdb web_pdb


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* cisco
    * Modified post_upload
        * renamed dataKey to data_key
        * renamed startTime to start_time
        * renamed dataVolume data_volume
    * Modified BusinessTelemetryPlugin
        * added  self.is_sdk_env in __init__ method
        * removed  is_sdk_env from post_job
        * added user_id,is_sdk_env,job_path for the script payload in post_task
    * Modified preprocess_pkg_data
        * removed runtime argument
    * Modified preprocess_sdk_pkg_data
        * removed runtime argument
    * Modified preprocess_pip_pkg_data
        * removed runtime argument
    * Modified preprocess_import_pkg_data
        * removed runtime argument
    * Modified preprocess_tcl_data
        * removed runtime argument
    * Modified preprocess_tcl_proc_data
        * removed runtime argument
    * Modified preprocess_tcl_history_data
        * removed runtime argument
    * Modified preprocess_csccon_data
        * removed runtime argument
    * Modified construct_record
        * renamed jobuuid to job_uuid
        * renamed dataKey to data_key
        * renamed startTime to start_time
        * renamed endTime to end_time
        * renamed dataVolume to data_volume
    * Modified build_package_repo_record
        * renamed jobDataKey to job_data_key
        * renamed userId to user_id
        * renamed jobuuid to job_uuid
        * renamed dataKey to data_key
        * renamed startTime to start_time
        * renamed endTime to end_time
        * renamed dataVolume to data_volume
    * Modified get_hostinfo
        * added code for check run from container
    * Modified build_package_repo_record
        * Added tcl_pkg event
    * Modified preprocess_tcl_proc_data
        * changed event type
    * Modified preprocess_tcl_data
        * added exeption hnadling
    * Modified get_tcl_tree
        * updated logic for collecting tcl pkg data
    * Modified environment/check/__init__.py
        * Fixed deprecation warning from distro module

* easypy
    * Modify test_blackbox.py test_blackbox()
        * Add pyats-conf for disabling CRFT and BTRACE.
    * Modify clean arguments
        * Deprecate clean_image and clean_platform
        * Add clean_device_image, clean_os_image, clean_group_image and clean_platform_image

* log
    * commands/parser/yaml_parser.py
        * Set the return value to ''  for the user field.

* utils
    * Modified utils.py get_distro_info()
        * Fixed deprecation warning from distro module
    * Fixed a bug where the YAML OrderedLoader did not support merge keys

* kleenex
    * Modified arguments
        * Deprecate clean_image and clean_platform
        * Add clean_device_image, clean_os_image, clean_group_image and clean_platform_image


