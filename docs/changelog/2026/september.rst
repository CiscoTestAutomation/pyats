September 2026
==============

September 29 - Pyats v26.9
--------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v26.9
    ``pyats.aereport``, v26.9
    ``pyats.aetest``, v26.9
    ``pyats.async``, v26.9
    ``pyats.cisco``, v26.9
    ``pyats.connections``, v26.9
    ``pyats.datastructures``, v26.9
    ``pyats.easypy``, v26.9
    ``pyats.kleenex``, v26.9
    ``pyats.log``, v26.9
    ``pyats.reporter``, v26.9
    ``pyats.results``, v26.9
    ``pyats.robot``, v26.9
    ``pyats.tcl``, v26.9
    ``pyats.topology``, v26.9
    ``pyats.utils``, v26.9




Changelogs
^^^^^^^^^^

--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* topology
    * Added support for generic Global Servers requests with server ``attributes`` and service ``fields`` and ``attributes`` dictionaries, while retaining ``scope``/``selection`` and legacy direct service keys including ``service_area``.
    * Added the ``device.management.wireless`` testbed schema for C9800 WMI uplink, addressing, routes, AP profile, RMI, and redundancy-port data.
    * Added compatibility handling that normalizes wireless route ``next-hop`` keys to ``next_hop``.
    * Added validation that rejects boolean VLAN IDs and empty wireless route next-hop values.
    * Added unit coverage for wireless management, HA data, route aliases, and cross-field validation.

* kleenex
    * Added a serializable testbed configuration collector for Clean stages.
    * Transport generated testbed fragments from Clean workers to the parent engine while retaining support for legacy worker result formats.
    * Aggregate successful worker output deterministically and discard it when Clean fails or times out.
    * Overlay generated devices and topology on the effective post-bringup testbed, warn when generated values replace existing values, and validate the result with the topology loader before updating the runtime testbed.
    * Write ``testbed.clean.generated.yaml`` and ``testbed.clean.merged.yaml`` artifacts for Easypy and standalone Kleenex, with task-specific filenames for task-scope Clean.

* easypy
    * Made the runtime deadline guard configurable through the ``easypy.runtime_deadline.guard_seconds`` pyATS configuration value, with a default of 1800 seconds.
    * Limited the guard to the remaining reservation runtime.

--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* easypy
    * Improved manifest job interrupt handling
        * Ctrl-C is forwarded to all processes in the job so normal cleanup and reporting can complete.
        * A repeated Ctrl-C or a cleanup timeout forcibly terminates any remaining job processes.
        * Fixed interactive job cleanup when the signal relay exits unexpectedly.
    * Modified manifest execution
        * Forward SIGTERM to the job process group when a manifest run is terminated.
        * Terminate the job process group if SIGTERM shutdown does not finish within the shutdown timeout.
    * Modified Task
        * Record pre-registration task timeouts as ERRORED in Reporter.

* kleenex
    * Apply images supplied by CLI device, group, platform, model, and OS selectors before YAML callable markup processing so replaced image lookup callables are not evaluated.
    * Preserve the ``clean_devices`` execution plan when a generated ``clean.extra.yaml`` file is merged as JIT clean content.

* utils
    * Preserve exceptions raised by YAML callables instead of treating them as argument parsing failures and invoking the callable again with different arguments, while retaining legacy raw-string argument handling.

* pyats
    * Normalized C9800-CL as ``model: c9800`` with ``submodel: c9800_cl``.

* connections
    * Modified ``ConnectionManager.instantiate``
        * Recreates a disconnected cached connection or connection pool when explicitly supplied constructor inputs differ, including ``via``, positional and keyword arguments, pool size, and pool timeout.
        * Preserves existing connection reuse when arguments are unchanged or omitted.

* reporter
    * Modified ReportServer
        * Create and close missing task records during forced termination.
