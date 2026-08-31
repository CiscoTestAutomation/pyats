August 2026
==========

August 25 - Pyats v26.8
-----------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.8
    ``pyats.aereport``, v26.8
    ``pyats.aetest``, v26.8
    ``pyats.async``, v26.8
    ``pyats.cisco``, v26.8
    ``pyats.connections``, v26.8
    ``pyats.datastructures``, v26.8
    ``pyats.easypy``, v26.8
    ``pyats.kleenex``, v26.8
    ``pyats.log``, v26.8
    ``pyats.reporter``, v26.8
    ``pyats.results``, v26.8
    ``pyats.robot``, v26.8
    ``pyats.tcl``, v26.8
    ``pyats.topology``, v26.8
    ``pyats.utils``, v26.8




Changelogs
^^^^^^^^^^

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* kleenex
    * Retry a device's complete Clean workflow when its cleaner reports that device recovery succeeded. The retry budget defaults to one and can be configured with ``--clean-retries`` (or ``-clean_retries`` for the legacy command) using a non-negative integer. Set it to zero to disable retries; successful recovery then leaves the unretried failure as the final Clean result.
    * Preserve the superseded attempt in ``results.json`` without including it in result rollup, and report a successful retry as ``PASSX``.
    * Add structured Clean retry attempt, trigger, and status metadata for future UI consumers.

* reporter
    * Exclude sections stopped with ``result_rollup=False`` from summaries and mark them as ignored in serialized reports.

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* topology
    * Modified topology lookup and link collection
        * Detects duplicate link names in a single pass without maintaining an incremental link registry
        * Uses keyed lookups before alias scans while preserving device object membership after a device name change

* utils
    * Modified entry-point discovery
        * Caches entry-point lookups for the lifetime of the process
    * Modified Schemaengine
        * Fixed required-key rendering so ``Required("key", description=...)`` reports the wrapped key name in missing-key errors instead of the schema wrapper text.
    * Preserve the legacy requirement ``project_name`` alias without mutating ``packaging.Requirement`` objects, adding compatibility with packaging 26.3 and later.

* ci
    * Modified pull request package builds
        * Builds both regular and Cythonized public alpha packages

* easypy
    * Modified TaskManager
        * Loads reservation end time deadlines from testbed custom data in core task handling.
        * Logs runtime deadline details before task start.
        * Reports runtime deadline task termination as an errored task.

* reporter
    * Modified ``stop_testsuite``
        * Finalize any section that was started but never stopped (e.g. a forked worker was force-terminated before reporting) so it shows a runtime and an errored result in the reports/UI instead of appearing blank with only a start time.
        * Roll the synthetic errored result up through the parent section, task, and suite summaries so reports no longer advertise a passing run while a descendant section is errored.
        * Publish a ``stop_section`` update for each finalized section so subscribers that already received the ``start_section`` get the matching runtime/result without needing a full reload.

* devat
    * Added lab-compliance reporting for PDUs without a management IP address.

* cisco
    * Modified version update
        * Include ats.cisco and ats.devat when looking up and reinstalling the latest internal package versions.
    * Modified the default SMTP configuration
        * Enabled STARTTLS for ``outbound.cisco.com`` because the Cisco SMTP relay now requires TLS connections.

* kleenex
    * Modified clean template merging
        * Preserves user-defined clean stages omitted from template order.
        * Keeps numbered and unnumbered instances of the same stage adjacent.
        * Excludes non-stage clean metadata from the execution order.
