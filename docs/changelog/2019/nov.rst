November 2019
=============

November 29, 2019
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.easypy``, v19.11.1
    ``pyats.cisco``, v19.11.1

Changes
^^^^^^^

- Easypy Plugins can be loaded through Python entry points

November 26, 2019
-----------------
.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.11
    ``pyats.aereport``, v19.11
    ``pyats.aetest``, v19.11
    ``pyats.async``, v19.11
    ``pyats.cisco``, v19.11
    ``pyats.connections``, v19.11
    ``pyats.datastructures``, v19.11
    ``pyats.easypy``, v19.11
    ``pyats.kleenex``, v19.11
    ``pyats.log``, v19.11
    ``pyats.reporter``, v19.11
    ``pyats.results``, v19.11
    ``pyats.robot``, v19.11
    ``pyats.tcl``, v19.11
    ``pyats.topology``, v19.11
    ``pyats.utils``, v19.11

Changes
^^^^^^^

Easypy
    - now returns a more detailed Linux return code based on nature of failure

    - ``--html-logs`` feature now generates ``TaskLog.<jobname>.html`` file to
      try to avoid overwriting previous log files


Cisco
    - uploading to TRADe now defaults to using REST api instead of cli

Reporter
    - Testcase ID duplicates are now properly reported in the final report

    - internal tweaks on report yaml format

    - removed YAML tags in favour of 'type' key

    - testscripts -> tasks (testscript refers to file, not execution)

    - moved details out of extra for all sections

    - Results.yaml version '2'

Pause on Phrase
    - Pause on phrase should now properly open ``stdin`` on pausing

Kleenex
    - It is no longer mandatory to specify images for devices/groups in the
      clean YAML file

Topology
    - Added peripherals keyword to device schema

utils.FileUtils
    - Changed local FileUtil package name from 'linux' to 'localhost' to avoid
      conflict with genie FileUtils

    - Removed `darwin` from FileUtil package, it is now supported by `localhost`

    - Fixed a bug where FileUtil will pick up the incorrect server block if the
      provided address is a sub string of any address in the testbed

Plugins
    - job.details() or task.details() will retrieve the aggregated test
      execution information

Processors
    - Including processor information in Results.yaml files

    - Mechanism for processors to change section result

Results
    - Results are **no longer** singletons, and cannot be compared with ``is``

    - Results can contain a reason and data associated with that result

Generic Changes
    - removed `setproctitle` as a dependency from all packages


November 8, 2019
----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.aetest``, v19.10.2

Changes
^^^^^^^

- Tasks now return Skipped when all Testcases are Skipped

November 7, 2019
----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.log``, v19.10.1

Changes
^^^^^^^

- fixed a bug with ``pyats logs view`` command on localhost to sometimes guess
  the host name wrong

November 4, 2019
----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.aetest``, v19.10.1
    ``pyats.reporter``, v19.10.1
    ``ats.cisco``, v19.10.1

Changes
^^^^^^^

- TIMS versions reporting and propagation (internal to cisco only)
- step banner changed to strictly ASCII instead of Unicode.
