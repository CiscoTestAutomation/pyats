May 2026
==========

May 26 - Pyats v26.5
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.5 
    ``pyats.aereport``, v26.5 
    ``pyats.aetest``, v26.5 
    ``pyats.async``, v26.5 
    ``pyats.cisco``, v26.5 
    ``pyats.connections``, v26.5 
    ``pyats.datastructures``, v26.5 
    ``pyats.easypy``, v26.5 
    ``pyats.kleenex``, v26.5 
    ``pyats.log``, v26.5 
    ``pyats.reporter``, v26.5 
    ``pyats.results``, v26.5 
    ``pyats.robot``, v26.5 
    ``pyats.tcl``, v26.5 
    ``pyats.topology``, v26.5 
    ``pyats.utils``, v26.5 




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* aetest-pkg
    * Modified Discovery
        * Consolidated shared section validation, instantiation, loop expansion, and retry expansion logic across script, testcase, and common discovery
        * Preserved existing discovery ordering, invalid-context checks, and duplicate CommonSetup, CommonCleanup, Setup, and Cleanup errors
        * Added docstrings and type hints to discovery helper functions and discovery classes
        * Preserved the initial retry result in retry data so discoverer-driven retries and direct ``retry_generator`` callers convert successful failed or errored retries to ``PASSX`` consistently

* cisco
    * Modified TestbedExportSubcommand
        * Changed LaaSv2 testbed export to call the refactored ``dyntopo.laasv2.exporter`` API instead of the removed ``dyntopo.laasv2.testbed`` module.
        * Stopped printing ``None`` after YAML when exporting to stdout.

* installer
    * Modified Python version selection
        * Updated the supported managed Python range to 3.10 through 3.14 for current pyATS releases.
        * Allowed pyATS 26.3 and older installs to continue using the legacy Python 3.9 through 3.13 range.
        * Allowed major.minor --py-version requests to match installed patch-level Python binaries.
        * Validated custom --py-home and Ubuntu system python3 binaries against the supported range.

* topology-pkg
    * schema
        * Added media_type optional field to management under device schema.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* topology
    * Added server schema support for interfaces and management routes
        * `interfaces` - per-interface dict keyed by name with optional `ipv4`/`ipv6` addresses.
        * `management.routes` - list of `{subnet, interface}` dicts for IPv4/IPv6 route entries.

* aetest-pkg
    * Added ``section_results`` support for retry decorator
        * When ``section_results=["passed"]`` is specified, tests are retried on pass to gauge stability by repeating N times
    * Modified RetryDecorator
        * Added support for per-testcase retry count overrides via the ``testcases`` kwarg
        * When a testcase UID is matched in ``testcases``, its ``retries`` value takes priority over the decorator-level default
        * Falls back to decorator-level ``retries`` when no matching UID is found, the key is absent, or the value is falsy


