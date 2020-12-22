February 2016
=============

.. warning::

    Starting Jan 1st, 2016, Python 2.x is no longer supported by pyATS. All
    development features & bug fixes will only be released for Python 3.x+
    versions.

    Please upgrade your Python dependencies as soon as possible.

February 24, 2016
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v2.2.2

Bug Fixes
^^^^^^^^^

* Standalone reporter was throwing exceptions when users try to run testcases
  without aetest. Because there was no testcase entry in the testResultDetails
  list, it wasn't able to add section information to the list. Now, if a section
  was run and testResultDetails list is empty, there will be a dummy testcase
  entry in the list as a container of sections information.

February 23, 2016
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.bringup``, v2.2.1

Bug Fixes
^^^^^^^^^

* Topology loader will not assign the testbed.name field by default anymore.

February 22, 2016
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aereport``, v2.2.1
    ``ats.aetest``, v2.2.1
    ``ats.easypy``, v2.2.1

Bug Fixes
^^^^^^^^^

* Fixed a minor problem of steps results. Order of sub-steps is now displayed
  properly.

* `US41048 <https://rally1.rallydev.com/#/22527801475d/detail/userstory/38228032210>`_ (adding step results to report email)


.. _v2.2.0:

February 4, 2015 - pyATS v2.2.0
-------------------------------

Announcing the release & availablility of pyATS ``v2.2.0``. This is a feature
release, intended to be mostly backwards compatible to ``v2.1.0``, introducing
new features & fixing old bugs/limitations

    *Please take a moment to study this changelog.*

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats``, v2.2.0,
    ``ats.aereport``, v2.2.0,
    ``ats.aetest``, v2.2.0,
    ``ats.async``, v2.2.0,
    ``ats.bringup``, v2.2.0,
    ``ats.clean``, v2.2.0,
    ``ats.connections``, v2.2.0,
    ``ats.datastructures``, v2.2.0,
    ``ats.easypy``, v2.2.0,
    ``ats.examples``, v2.2.0,
    ``ats.log``, v2.2.0, "renamed atslog -> log"
    ``ats.results``, v2.2.0,
    ``ats.tcl``, v2.2.0,
    ``ats.templates``, v2.2.0,
    ``ats.tgn``, v2.2.0,
    ``ats.tims``, v2.2.0,
    ``ats.topology``, v2.2.0,
    ``ats.utils``, v2.2.0,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

- if you are upgrading from ``v2.0.1+``, it is pretty straightforward:

  .. code-block:: bash

      bash$ pip install --upgrade ats

- if you are upgrading from a lower version, please refer to ``v2.0.0`` and
  ``v2.0.1`` upgrade instructions first.


Changes
^^^^^^^

``v2.2.0`` packs a few under-the-hood changes that enables better extendability
in the long run, and includes subtle tweaks to better the user interactive
experience. As always, refactoring of the internal code is done wherever
necessary to make room for future scalability.

In addition to ``v2.2.0``, the following **new Cisco-Shared packages** developed
by ASG team is also being released at the same time:
    
    - ``xrut``: module that allows the seamless executon of XRUT scripts under
      Easypy job file.

    - ``dyntopo``: module offering a collections of tools to launch and tear 
      down dynamic topologies, including a LaaS-NG orchestrator.  See: DynTopo_

.. _DynTopo: http://wwwin-pyats.cisco.com/cisco-shared/html/dyntopo/docs/index.html


AEtest
    - support for script :ref:`aetest_datafile`, an alternative way to alter
      your script run & augment your script with new values & etc.

    - support for :ref:`aetest_pause_on_phase`, pausing the script at a matching
      log message and allowing you to choose either an email notification, or
      automatically open up a debugger/interactive shell.

    - support for :ref:`aetest_global_processors`

    - reworked how results are reported under stand-alone execution. 

    - visual result report now includes step reports

    - fixed a bug where looped testcases were sharing the same testcase
      parameter object instance and allowed value corruptions.

Async
    - fixed an issue with ``async.Pcall`` where function returns of larger than
      64K causes the process to hang up and raise ``TimeoutError``.

    - keep in mind there is a hard-ceiling for function returns to be no 
      larger than ~78MB, limited due to the use of 32-bit Python.

BringUp
    - `US49255 <https://rally1.rallydev.com/#/18032525878d/detail/story/43458955135>`_ (allow user-defined bringup implementations):
    - Dynamic topologies are now brought up in a worker subprocess.
    - Debugging of a worker subprocess is possible via the `-pdb` CLI argument.
    - Introduced the new `ats.bringup.BringUp` object as the primary user
      interface to bringup.
    - The `ats.bringup.BringUp` object is now the recommended context manager
      for standalone scripts, although `ats.bringup.XrutBringUp` is still
      supported for back-compatibility.
    - Added the `bringup/class` key to the clean YAML schema to make it possible
      for users to contribute their own bringup implementations.
    - Changed the standalone bringup tool CLI option from
      `-xrut_tb_yaml_output_file_name` to `-tb_yaml_output_file_name`.
    - `bringup -help` now renders all CLI options correctly.
    - Refactored and split out common bringup logic that is not
      XR-UT specific.
    - Refactored `bringup` parameters to make them more similar to `ats.aetest`.
      This means that most of the parameters displayed by `bringup -help`
      may also be specified on the `easypy` command line and they will be
      passed through to the bringup subsystem
      (but they won't appear in the `easypy -help` display).
    - Refactored easypy clean plugin to bring up dynamic topologies in a
      subprocess.
    - Reworked example standalone script to use `ats.bringup.BringUp`.
    - Refactored the topology loader, pulled out common logic which is now used
      for both testbed and clean YAML loading.
    - Realigned the allowable virtual logical device types to be less
      XRUT-specific:

        .. csv-table:: Virtual logical device type mappings
            :header: "Old logical type name", "New logical type name"

            ``nxos``, ``nxosv``
            ``iol-pagent``, ``iol_pagent``
            ``ios``, ``ios_dynamips or iosv``
            ``ios-pagent``, ``ios_dynamips_pagent or iosv_pagent``
            ``xrvr``, ``iosxrv``

    - `US58901 <https://rally1.rallydev.com/#/18032525878d/detail/userstory/47562740650>`_ ,
      `US54326 <https://rally1.rallydev.com/#/18032525878d/detail/userstory/45569642625>`_ :
      Integrated the cisco-shared dyntopo bringup module for LaaS-NG, which
      introduces the concept of job-scope bringup.
    - Fixed a bug in testbed configuration merge conflict resolution,
      now conflicting values are properly resolved when they are more than
      one level deep.
    - Now warning the user if they are using the `is_logical` testbed YAML key.
      This will be removed in the next release, the `logical` key is to be used instead.
    - `US60655 <https://rally1.rallydev.com/#/22527801475d/detail/userstory/48234726165>`_ (allow user-defined logical device/interface testbed configuration):
      Users can now specify their own keys and values under logical devices and
      interfaces in their testbed configuration and see them appear in the
      actual testbed configuration.  Although it is now also possible for the user
      to overwrite keys that are auto-populated by the orchestrator (for example,
      by overwriting an auto-assigned IP address if the orchestrator supports
      such a feature), they must accept all responsibility for doing so by
      properly configuring their devices.

Clean & Connections
    - ``tcl_clean`` now supports ``tftpServer_unix`` key

    - support for ``aireos`` device type & connection.

    - fix a bug where ``tcl_clean`` block was being checked for devices not
      specified under clean file.

Easypy
    - supports for :ref:`easypy_graceful_termination` of jobfile  
      tasks through Ctrl-C (SIGINT interrupt).

    - email report now includes step details

    - Fixed an issue with ``easypy`` not setting correct folder permissions when
      creating ``/users`` and ``/users/<id>`` etc.

    - enhanced ``-xunit`` support, now includes a TRADe link.

    - fixed an issue with plugin import exceptions not being printed properly

Installation
    - install script now always checks out ``xbu-shared``, ``regression`` and
      ``cisco-shared`` repos

    - install script now checks for your ``git`` binary location, and warns error if
      it cannot find it.

    - install script now ignores ``install.log`` file and overwrites it whenever
      needed, making user's life slightly easier.

    - install script now suggests ``branch.autosetuprebase always`` as a global
      configuration, and now auto-applies ``pull.rebase`` to ``true`` for all
      checked-out repositories.

    - install script now uses ``pip.conf`` to configure ``pip``, and will always
      update ``pip`` and ``setuptools`` to latest.

    - new ``update_pip_config`` script to upgrade user's pip configurations.

    - changing pyATS PyPI server from ``ats-pypi-server.cisco.com`` to
      ``pyats-pypi.cisco.com``.

Log
    - ``atslog`` module is now renamed to just ``log``

    - backwards compatibility code is included in this release to notify users
      to make the necessary modifications.

    - logging is now overhauled to support the standard :ref:`cisco-log-format`.

    - multi-part log messages now have proper tagging

    - fixed a bug with ``logging.exception()`` calls where the stack trace was
      being logged multiple times if the provided message is multi-line.

Utils
    - refactor & standardized how YAML loading is performed throughout all
      modules.

    - support for injections into YAML loading stages

    - support for custom YAML markup processor subclasses & generalization


*And, as usual, a plethora of potential new bugs that we are neither aware of,
nor able to zap... yet.*

**1357 unittests and counting**
