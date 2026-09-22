July 2026
==========

July 28 - Pyats v26.7
---------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.7
    ``pyats.aereport``, v26.7
    ``pyats.aetest``, v26.7
    ``pyats.async``, v26.7
    ``pyats.cisco``, v26.7
    ``pyats.connections``, v26.7
    ``pyats.datastructures``, v26.7
    ``pyats.easypy``, v26.7
    ``pyats.kleenex``, v26.7
    ``pyats.log``, v26.7
    ``pyats.reporter``, v26.7
    ``pyats.results``, v26.7
    ``pyats.robot``, v26.7
    ``pyats.tcl``, v26.7
    ``pyats.topology``, v26.7
    ``pyats.utils``, v26.7




Changelogs
^^^^^^^^^^

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* easypy
    * Added ``TaskManager`` runtime deadline support
        * Allows Easypy to cap task execution using an absolute deadline discovered from dynamic topology metadata.
        * Applies the cap through existing ``Task.wait()`` and ``runtime.tasks.run()`` timeout paths so jobfiles do not need syntax changes.
    * Added a new plugin to copy the datafile to log.

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* easypy
    * Modified ``TaskManager`` runtime deadline handling
        * Applies a default 300-second guard before runtime deadlines.
    * Modified ``Task.wait()``
        * Detects when a task process stays alive after pyATS execution due to leaked non-daemon threads and force-terminates it instead of hanging forever.
    * Hardened OneDevx and TaaS log archive uploads
        * Increased the default upload timeout to 300 seconds while retaining the cisco.upload.timeout.api configuration override.
        * Retries transient upload failures without sleeping after the final attempt and reports final failures consistently.
        * Closes archive files after every upload attempt.
        * Adds local log-viewer guidance when OneDevx or TaaS upload fails.

* kleenex
    * Modified standalone clean reporting
        * Allows ``KleenexMain(name=...)`` to set the top-level report suite name in ``report.json`` independently from the suite id.

* reporter/kleenex
    * Report standalone Kleenex device totals in the top-level ``summary`` instead of ``pluginsummary`` while preserving normal plugin reporting.
    * Report standalone clean runs with no device sections as skipped without adding a synthetic skipped device result.
    * Preserve support for historical clean archives whose totals are stored in ``pluginsummary``.
    * Keep nested Standalone, Device, clean stage, and step summaries and results unchanged.
    * Update reporter schema validation to accept the existing top-level ``report.result`` field introduced with report version 3.4. This does not change the serialized report format or require another report version bump.

* reporter
    * Modified reporter IPC timeout handling
        * Honor ``PYATS_REPORTER_TIMEOUT`` and ``PYATS_REPORTER_MAX_RETRIES`` for reporter client/server IPC.
    * Modified section log line assignment
        * Assign log output emitted between adjacent sibling sections to the previous stopped section so trailing failure details are included in the correct report section.

* docker
    * Modified Alpine Builder
        * Updated the Alpine builder base image to Alpine 3.22.

--------------------------------------------------------------------------------
                                    Modified                                    
--------------------------------------------------------------------------------

* updated ``--meta`` parsing for easypy and replay commands to accept multiple metadata values after a single flag, such as ``--meta key1=value1 key2=value2``, while preserving repeated ``--meta`` usage and filtering plain positional or unknown arguments from the metadata values.
