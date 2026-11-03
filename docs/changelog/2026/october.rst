October 2026
==========

 - Pyats v26.10
---------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.10
    ``pyats.aereport``, v26.10
    ``pyats.aetest``, v26.10
    ``pyats.async``, v26.10
    ``pyats.cisco``, v26.10
    ``pyats.connections``, v26.10
    ``pyats.datastructures``, v26.10
    ``pyats.easypy``, v26.10
    ``pyats.kleenex``, v26.10
    ``pyats.log``, v26.10
    ``pyats.reporter``, v26.10
    ``pyats.results``, v26.10
    ``pyats.robot``, v26.10
    ``pyats.tcl``, v26.10
    ``pyats.topology``, v26.10
    ``pyats.utils``, v26.10




Changelogs
^^^^^^^^^^

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* kleenex
    * Added process-safe coordination for parallel Clean workers, including readiness, completion, failure, and timeout handling.
    * Generated Clean coordination metadata is honored without requiring a ``clean_devices`` entry in the Clean configuration.
    * Clean now reports worker failures instead of silently omitting workers

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* kleenex
    * Keep Clean stages declared with an empty body (e.g. ``connect:``) as empty dicts instead of removing them, fixing "Stage '<name>' has no configuration in clean.yaml" errors.
    * Remove ``None``-valued entries from merged Clean configuration before it is displayed, saved, and applied to the testbed.
    * Added standalone xUnit reporting
        * Support --xunit and --xunit-include-logs with pyats clean, including an alternative output directory.
        * Keep xUnit generation disabled unless explicitly requested.
        * Finalize reporting when Clean engine initialization fails before any device section starts.
    * Easypy now reserves five minutes before an active runtime deadline and passes the remaining Clean budget through a private engine integration path.
    * Bounded that shared invocation timeout across parallel workers, sequential device groups, debug mode, and full-Clean recovery retries.
    * Added bounded worker and descendant termination with SIGKILL fallback when a runtime or per-device timeout expires.
    * Made worker-result publication atomic so deadline cleanup cannot block on a partially written result. The public ``timeout=`` API retains its per-worker behavior, including the existing ``timeout=0`` fallback; zero on the private invocation path prevents a worker from starting.
    * Fixed coordinated Clean execution in debug mode and when a worker exits before coordination completes.

* easypy
    * Modified XunitPlugin
        * Generate requested xUnit reports after job reporter finalization when a pre-job plugin fails.
        * Add a standard JUnit testcase for unsuccessful top-level job plugins and include the OneDevX reference when available.
        * Exclude non-rollup sections from XML counts and time while retaining independently reportable children.
        * Retain testcases when optional logs cannot be read.
    * Updated xUnit reports to omit intermediate retry attempts and include the final result. Runs without retries are unchanged.

* kleenex / easypy
    * Improved Clean device-selection logging
        * Log ``--clean-devices`` selections separately from configuration defaults and effective device alias/name mappings, without changing Clean targets.

* cisco
    * Modified BringupSubcommand
        * ``pyats testbed bringup --clean-file`` no longer fails with an empty ``StopIteration`` error when the clean file only has a ``bringup`` section and no cleaners.
