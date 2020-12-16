September 2015
==============


Sept 22, 2015
-------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v2.1.1
    ``ats.examples``, v2.1.1

Upgrade Instructions
""""""""""""""""""""

- if you are upgrading from ``v2.0.1+``, it is pretty straightforward:

  .. code-block:: bash
    
      bash$ pip install --upgrade ats

- if you are upgrading from a lower version, please refer to ``v2.0.0`` and
  ``v2.0.1`` upgrade instructions first.


Changes
"""""""

- added demo scripts to ``examples``, including v2.1.0 demo scripts.

- ``max_failures`` argument in ``aetest`` is now "exclusive" as opposed to 
  "inclusive" after much controversy. Eg, if ``-max_failure 5``, then as soon
  as the 5th testcase fails, the script will abort. 


Sept 17, 2015
-------------

.. csv-table:: Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v2.1.1
    ``ats.connections``, v2.1.1

Upgrade Instructions
""""""""""""""""""""

- if you are upgrading from ``v2.0.1+``, it is pretty straightforward:

  .. code-block:: bash
    
      bash$ pip install --upgrade ats

- if you are upgrading from a lower version, please refer to ``v2.0.0`` and
  ``v2.0.1`` upgrade instructions first.


Bug Fixes
"""""""""

- reverted ``ats.easypy`` behavior where if ``-testbed_file`` is not provided, 
  ``testbed`` parameter in testscript is ``None``.

- fixed a merge error in ``ats.connections`` causing crashes in python-2


.. _v2.1.0:

Sept 15, 2015 - pyATS v2.1.0
----------------------------

Announcing the release & availablility of pyATS ``v2.1.0``. This is a feature
release, intended to be mostly backwards compatible to ``v2.0.0+``, introducing
new features & fixing old bugs/limitations

    *Please take a moment to study this changelog.*

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats``, v2.1.0, 
    ``ats.aereport``, v2.1.0, 
    ``ats.aetest``, v2.1.0,
    ``ats.async``, v2.1.0, "new module"
    ``ats.atslog``, v2.1.0,
    ``ats.bringup``, v2.1.0, "new module, only available Python-3"
    ``ats.clean``, v2.1.0,
    ``ats.connections``, v2.1.0,
    ``ats.datastructures``, v2.1.0,
    ``ats.easypy``, v2.1.0,
    ``ats.examples``, v2.1.0,
    ``ats.results``, v2.1.0,
    ``ats.tcl``, v2.1.0,
    ``ats.templates``, v2.1.0,
    ``ats.tgn``, v2.1.0,
    ``ats.tims``, v2.1.0,
    ``ats.topology``, v2.1.0,
    ``ats.utils``, v2.1.0,

Upgrade Instructions
""""""""""""""""""""

- if you are upgrading from ``v2.0.1+``, it is pretty straightforward:

  .. code-block:: bash
    
      bash$ pip install --upgrade ats

- if you are upgrading from a lower version, please refer to ``v2.0.0`` and
  ``v2.0.1`` upgrade instructions first.

Content
"""""""

The major driver behind ``v2.1.0`` is the support for asynchronous execution
using multiprocessing, refactoring ``easypy`` for modularity and better
plugins support, introducing ``bringup`` module for automating logical
topology/device orchestrations, and various ``aetest`` improvements & features.

- major refactoring to ``easypy`` runtime engine's interal infrastructure.

  - modularity in internal code

  - revised error catching, propagation & logging mechanisms

  - support for multiprocessing & parallel executing tasks

  - support for customizable email notification report

  - support for user plugins & plugin run stages

  - revamped ``runtime`` state query mechanism

  - better unittests

- new module ``async``

  - support for hands-off parallel function calls

- new module ``bringup``

  - support for automated orchestration of logical testbed devices using XRUT

- new ``aetest`` script execution feature

  - support for launching an interactive debugger automation on failures

  - support for maximum testcase failures before script termination

  - support for requisite testcase (testcase must-pass)

  - support for testcase run-order randomization

  - complete removal of ``self.script_args``

  - complete removal of ``Testcase.Subtest`` feature and definitions

- internal overhauls in multiple components for multiprocessing-friendly and
  awareness.

  - fork-aware ``atslog`` loggers

  - fork-aware ``aereport`` clients

- ~100 pages of new, updated, self-explanatory documentation for your weeknights
  and weekend reading pleasures.

- a whole slew of bug fixes

- *and of course, introducing new bugs.*

Easypy Changes
^^^^^^^^^^^^^^

- The internal refactoring of Easypy source code does not modify its external
  interfaces (eg, cli arguments, jobfile apis, etc). The user experience should
  be uplifted without backwards compatibility issues.
  
  - no external argument changes

  - no jobfile class/interface changes

  - easypy source code is now fully modular.

- :ref:`easypy_tasks` system overhauled

  - all jobfile  are now run within its own child process (encapsulation). (note
    that as a side-effect, ``pdb`` within child processes will fail unless
    ``/dev/stdin`` is re-opened. Refer to :ref:`mutiprocess_pdb` for details)

  - new ``Task`` class enabling both sequential and asynchronous execution of
    tasks within a jobfile. ``Task`` class is designed to provide user full
    control of task with the jobfile.

  - built-in ``TaskManager`` associated with all jobfile tasks, automatically
    notifies the user when tasks are dangling.

- :ref:`easypy_email_notification` feature overhauled

  - now sends you an exception notification when ``easypy`` components/jobfile
    crashed.

  - support for customizing the default text email report by adding and removing
    sections

  - support for subclassing & creating your own MIME RichText/HTML emails

- :ref:`easypy_plugin` feature overhaled

  - support for loading user's custom plugins and its configurations through
    YAML file defined via environment variable ``EASYPY_PLUGIN_CONFIG``

  - support for running plugins at various fixed stages during execution:
    ``pre_job``, ``post_job``, ``pre_task`` and ``post_task``.

  - support for plugin argument parsers, and combining currently active plugin's
    parsers into the master help output displayed using ``easypy -h``.
  
  - plugin documentation

- the runtime environment created by ``easypy`` has been reviewed for 
  multiprocess-friendliness. Multiple components & internal modifications were 
  done in order to accomodate process forks.

- more readily available :ref:`easypy_runtime` state information

- dangling child processes at the end of ``easypy`` execution are now quietly
  terminated. Turn on ``-logleve=DEBUG`` to see the massacre in action.

AEtest Changes
^^^^^^^^^^^^^^

- new argument ``-pdb``, allowing AEtest to automatically start an interactive
  debugging session when a failure/execption is caught. Refer to 
  :ref:`aetest_pdb` documentation for details.

- new argument ``-random``, allowing AEtest testscripts to run its testcases
  in randomized execution order. Refer to :ref:`aetest_testcase_randomization`
  documentation for details.

- new argument ``-max_failures``, allowing AEtest to automatically terminate the
  testscript if number of testcases failures exceeds the provided value. Refer
  to :ref:`aetest_max_failures` for details.

- support for requisite testcases (a.k.a testcase must-pass). A testcase with
  ``must_pass`` label, if failed, will cause the whole script to terminate.
  Refer to :ref:`aetest_requisite_testcase` documentation for details.

- ``Testcase.Subtest`` and the ability to define subtests within testcases is
  now competely removed (as discussed in v2.0.0 release note).

- ``self.script_args`` is now completely removed. Use :ref:`test_parameters`
  instead (as discussed in v2.0.0 release note).

- calling ``self.<resultapi>()`` with ``goto=[]`` within steps should now work
  as intended.

New Modules
^^^^^^^^^^^

The following new modules have been introduced in pyATS ``v2.1.0`` release.

``async``
    Module for asynchronous (parallel) execution support. This module acts as
    reminder to all core developers that asynchronous execution in pyATS 
    requires dedicated code support, offers a central location for expanding on
    the mindset behind pyATS multiprocessing, and offers a hands-off approach
    to calling functions and methods in parallel using :ref:`async_pcall` class.

    More libraries and apis will be added to this module as we go.

    Read ``async`` documentation here: :ref:`async_index`.

``bringup``
    Module for automated logical testbed/device orchestration. This module
    leverages the current abilities of XRUT to orchestrate virtual testbeds, 
    integrating its features & capabilities into pyATS, allowing ``easypy``
    script runs to automatically bring-up and tear-down virtual testbeds before
    and after the script run.

    Read ``bringup`` documentation here bringup.

Multiprocessing Tuneups
^^^^^^^^^^^^^^^^^^^^^^^

- ``atslog.TaskLogHandler`` now supports automatic on-fork creation of new log
  files. 

  - enable/disable using ``enableForked()`` and ``disableForked()`` methods.

  - by default, each Easypy task's TaskLog will has this feature enabled.

- ``aereport.AEClient`` now supports automatic re-connect to the reporting 
  server post-fork.

  - enable/disable using ``enable_forked()`` and ``enable_forked()`` methods.

  - by default, Easypy and AEtest's report client instances have this feature 
    enabled.

Misc Changes
^^^^^^^^^^^^

- install script now supports handoff (prompt-free) installation (for automating
  new pyATS installations)

- introduced new supported external PyPI packages and versions:

  .. csv-table:: New and Updated PyPI Packages
    :header: "Package", "Versions", "Comments"

    ``asynctest``, v0.4.0, "used for asyncio testing"
    ``pip``, v7.1.2,
    ``setuptools``, v18.3.1, 
    ``setproctitle``, v1.1.9, "used by AEreport and Easypy"

- fixed an issue with ``examples`` and ``templates`` packages being built to
  platform/arch specific wheels.

- other minor stuff we don't remember :-(
