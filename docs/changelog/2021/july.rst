July 2021
========

July 27, 2021
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.7
    ``pyats.aereport``, v21.7
    ``pyats.aetest``, v21.7
    ``pyats.async``, v21.7
    ``pyats.cisco``, v21.7
    ``pyats.connections``, v21.7
    ``pyats.datastructures``, v21.7
    ``pyats.easypy``, v21.7
    ``pyats.kleenex``, v21.7
    ``pyats.log``, v21.7
    ``pyats.reporter``, v21.7
    ``pyats.results``, v21.7
    ``pyats.robot``, v21.7
    ``pyats.tcl``, v21.7
    ``pyats.topology``, v21.7
    ``pyats.utils``, v21.7

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

* uploadtaas.py
    * Modified upload_via_rest
        * Archive log upload responses (TRADe, logs upload, clean) are now sent to Kafka via business telemetry.

* businesstelemetry
    * Added post_upload
        * post_upload sends upload log response to telemetry, reusing post_business_telemetry

* cisco (internal)
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
    * Added internal_data.py
        * Added function that returns internal github urls and gives internal related package information

* kleenex
    * Modified kleenex_main
        * Kleenex now uploads log archives to TaaS by default
        * Added argument -no_upload to skip the upload

* trade (internal)
    * Modified upload
        * Added TaaS Log Viewer URL to reports

* utils
    * Modified Loader
        * Enhanced Loader.load_arbitrary() to load YAML files from URLs

* easypy
    * Modified AeReporter
        * Extended --meta feature to allow indidual key/value pairs, URLs, and file paths to be passed in from the command line

* reporter
    * Added Utils
        * Added 3 APIs enforce_max_key_value_length, create_extended_dict and generate_unique_key_name
    * Modified Server
        * Added in a meta verification during start_testsuite()


--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* cisco (internal)
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

* trade (internal)
    * Modified upload
        * Upload to TaaS now shows TaaS URL banner on report even when there is an error

* easypy
    * Modified HTMLLogsPlugin
        * Fixed a bad reference to the reporter which prevented HTML log

* pyats.kleenex
    * Fix kleenex log handler logic



