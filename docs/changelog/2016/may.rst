May 2016
========

May 24, 2016
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.templates``, v3.0.1,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

- Fixed a minor bug under squeeze_topology


May 20, 2016
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.kleenex``, v3.0.4,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

- Added csr1000v to the list of supported virtual platforms.


May 17, 2016
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.aetest``, v3.0.4,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aetest

Changes
^^^^^^^

- Fixed a bug in AEtest where internal parameter reference mechanism breaks down
  right before the current executing scope terminates. (this is a very 
  inconspicuous bug, does not impact anything due to scope exit & garbage 
  collection)


May 11, 2016
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.aetest``, v3.0.3,
    ``ats.async``, v3.0.2,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aetest ats.async

Changes
^^^^^^^

- Fixed a bug in ``async.Pcall`` where excessive polling caused 100% cpu usage
- Fixed a bug where ``id->uid`` warning was being displayed regardless of
  input argument when ``aetest.loop.mark`` was being used
- Changed install script's ``--upgrade`` argument to ``--reinstall`` to avoid
  confusion with ``pip install --upgrade``.


May 10, 2016
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.async``, v3.0.1,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.async

Changes
^^^^^^^

- Fixed a bug that made ``iargs``, ``ikwargs`` and ``varkwargs`` Pcall 
  arguments to fail when an iterable or generator is provided.


May 9, 2016
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.easypy``, v3.0.2,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

- Fixed an inconsistency in the easypy report where testcase name was used
  instead of its unique id


May 6, 2016
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.kleenex``, v3.0.3,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

- Fixed a syntax error that was causing an unhandled exception to be thrown.

May 5, 2016
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.aetest``, v3.0.2,
    ``ats.connections``, v3.0.1,
    ``ats.topology``, v3.0.1,
    ``ats.kleenex``, v3.0.2,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aetest ats.connections ats.topology ats.kleenex

Changes
^^^^^^^

- Added some spaces in deprecation warning message
- Fixed defaulting to Csccon not working if device object was instantiated
  manually without YAML loading
- `US100754 <https://rally1.rallydev.com/#/22527801475d/detail/userstory/55308603041>`_
  (Added support for clean YAML markup processing).


May 3, 2016
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.aetest``, v3.0.1,
    ``ats.easypy``, v3.0.1,
    ``ats.kleenex``, v3.0.1,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aetest ats.easypy ats.kleenex

Changes
^^^^^^^

- Fixed a typo in AEtest ``ids`` -> ``uids`` backwards compatibility code.
- Fixed an issue where a removed unittest file was lingering in the final built
  AEtest package
- Fixed a bug where Easypy unittests were referring a wrong directory when 
  running in a user environment
- Fixed a bug in Kleenex that was causing corrupt data in the output yaml file.


May 2, 2016 - pyATS v3.0.0
--------------------------

    *Third time's the charm!*

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats``, v3.0.0
    ``ats.aereport``, v3.0.0,
    ``ats.aetest``, v3.0.0,
    ``ats.async``, v3.0.0,
    ``ats.connections``, v3.0.0, "Csccon is now moved to Cisco-Shared"
    ``ats.datastructures``, v3.0.0,
    ``ats.easypy``, v3.0.0,
    ``ats.examples``, v3.0.0,
    ``ats.kleenex``, v3.0.0, "**new:** testbed clean & orchestration engine & template"
    ``ats.log``, v3.0.0,
    ``ats.results``, v3.0.0,
    ``ats.tcl``, v3.0.0,
    ``ats.templates``, v3.0.0,
    ``ats.tims``, v3.0.0,
    ``ats.topology``, v3.0.0,
    ``ats.utils``, v3.0.0,

.. _TclClean Documentation: http://wwwin-pyats.cisco.com/cisco-shared/html/tclclean/docs/index.html
.. _HLTAPI Documentation: http://wwwin-pyats.cisco.com/cisco-shared/html/hltapi/docs/index.html


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # remove deprecated packages
    bash$ pip uninstall ats.clean ats.bringup ats.tgn

    # install new pyATS version
    bash$ pip install --upgrade ats

    # install new cisco-shared packages
    bash$ pip install csccon tclclean dyntopo hltapi

Deprecation Notice
^^^^^^^^^^^^^^^^^^

The following code usages are deprecating and will be removed by next release.
Backwards compatibility is currently provided - a warning will be generated each
time the legacy method is used. Please make the blanket change soon.

- AEtest's ``Testcase.id`` field is renamed to ``Testcase.uid`` (unique id).
  This is done in order to avoid collision with python's
  `built-in function`_ ``id()``.

  .. code-block:: python

      # Example
      # -------

      class Testcase(aetest.Testcase):

          # old style
          id = 'alt_id_of_testcase'

          # new style
          uid = 'alt_id_of_testcase'

  As a result, all AEtest options, eg: ``-ids=``, ``@loop(ids=[])`` have been
  renamed with a ``u`` prefix, eg, ``-uids=``, ``@loop(uids=[])``.

  To make a blanket change, search your source code with the following regular
  expression and add a ``u`` in front as a prefix.

  .. code-block:: text

        \.id| id | ID |'id'|`id`|`ids`|'ids'| id ?=|\(ids ?=|=ids|=id

- ``Device.config()`` method is now renamed to ``Device.configure()`` for
  consistency with ``Device.execute()``.

  Hint: search your code with the following regex to do a blank replace

  .. code-block:: text

      \.config(

- ``ats.atslog`` module renamed to ``ats.log``. This was changed in ``v2.0.0``,
  and was slated for removal this release, but we have extended it to the next
  release.

  Hint: search your code for the following

  .. code-block:: text

      from ats import atslog        ->      from ats import log
      from ats.atslog import x      ->      from ats.log import x

.. _built-in function: https://docs.python.org/3/library/functions.html#id

- Logical testbed configuration for dynamic bringup must now be specified
  via the ``-logical_testbed_file`` easypy argument.   For a limited time,
  logical devices will be accepted in the ``-testbed_file`` easypy file,
  but a warning is raised and support will be removed in the next release.

- The bringup clean schema from the previous release has been deprecated.
  If used, a warning is raised.  Support will be removed in the next release.

The following packages have now fully **deprecated** and have been removed and
replaced by other functionalities.

``ats.clean``
    replaced by ``ats.kleenex`` generic clean/orchestration engine. This legacy
    Tcl-based clean wrapper is now moved to cisco-shared as ``TclClean`` module.
    See `TclClean Documentation`_.

``ats.bringup``
    now an integral part of ``ats.kleenex`` model.

``ats.tgn``
    moved to cisco-shared as its own independent module ``hltapi``.
    Refer to `HLTAPI Documentation`_.


Changes
^^^^^^^

``v3.0.0`` introduces the new integrated bringup / clean (Kleenex) model that
we hope will help prepare the way for a new wave of user-designed clean,
bringup and connection implementations.

Although the bringup subsystem has been extensively refactored, we have
strived to maintain back-compatibility to the previous release whenever
possible.

.. note ::
    Pay attention to the various warnings that may appear, as they will
    remind you of script changes that you should schedule to make before
    certain pyATS features are removed in subsequent releases.

This release also contains many other small bug fixes and internal
refactoring to improve the user experience and set the foundation for
upcoming features.


Async
  - Added new :ref:`async_lockable` base class and
    `locked<ats.async.synchronize.locked>` decorator for auto-locking and
    unlocking of method calls and designing class objects sharable between
    multiprocesses.

AEReport
  - Description field is now supported for common subsections.

AEtest
  - now supports testcase/section metadata such as ``name``, ``diags``,
    ``hwversion``,  ``swversion``, and changing section ID during runtime
    within the code. See :ref:`aetest_aereport_reporter` for details.

  - ``Testcase.id`` is now renamed to ``Testcase.uid`` to avoid clashing with
    python ``id()`` function

  - Step results are now shown in the Easypy diagnostic report

  - warning/error/critical log messages are now automatically added to Easypy
    diagnostic report

  - (internal) reporter classes now have ``start_step`` and ``stop_step``
    reporting apis.

Bringup
  - The old bringup module is now integrated into the new
    ``kleenex`` package.

Clean
  - The old Clean module is now moved as an independent cisco-shared
    ``tclclean`` package and is now compliant to the new Kleenex model.
    See `TclClean Documentation`_.

    This is a *non-backwards compatible change*. Clean file is now very
    different. Please refer to documentation for specifics.

Connections
  - Refactored and moved Csccon wrapper code from core pyATS into an
    independent Cisco-shared package ``csccon``. See `Csccon Documentation`_.

    This is a *mostly backwards compatible change*. Most users shouldn't be
    importing Csccon directly, as it was the default connection class used.
    However, for the select few which this may impact, the following changes
    will be necessary:

    .. code-block:: python

        # before
        from ats.connection.csccon.bases import Csccon

        # after
        from csccon import Csccon

  - Csccon (cisco-shared package) overhauled to support sharing between
    multiple processes and pooling.

  - internal refactoring for better, modular support for user's own connection
    implementation

  - New documentation:

    - how stuff works in general

    - how connections and device topology objects interact

    - how to create your own connection implementations

  - support for sharing connections between forked process (no more deadlocks)

  - support for device :ref:`connectionpool`.

  - ``ConnectionManager.destroy_connection()`` has been renamed to
    ``destroy`` for simplicity and consistency.

  - ``BaseConnection.config()`` is now renamed to ``configure()`` for
    consistency. As a result, all connection implementations shall now implement
    ``configure()`` instead. Backward compatibility will be kept, but a warning
    will be displayed if ``config()`` is used.

  - changed the default connection path behavior: if the user defines a
    ``defaults/via`` key under the device connections dictionary (from YAML), it
    will be used as the default ``via`` path in ``device.connect()``.

  - added a mechanism for user to change the default connection class (instead
    of always defaulting to Csccon)

  - added a mechanism for users to change the default connection alias.

.. _Csccon Documentation: http://wwwin-pyats.cisco.com/cisco-shared/html/csccon/docs/index.html


Easypy
  - now generates a diagnostics report (diagreport) as part of a job run.

  - Testbed & clean files are now copied into your log archive.

  - Plugin exception handling has been refactored.

    - If an easypy plugin fails at ``pre_job`` or ``post_job`` stages,
      an email is sent whose title contains the name of the failing plugin,
      and a TRADe link is made available to allow the user to inspect the
      failure.

    - If an easypy plugin fails at ``pre_task`` or ``post_task`` stages,
      the task is immediately terminated and the name of the failing
      plugin is added to the exception text.

  - Now different easypy arguments are provided for specifying testbeds of
    actual devices (``-testbed_file``)
    and actual/logical devices (``-logical_testbed_file``).

  - Introduced new parameters ``-clean_devices`` and ``-clean_scope`` as
    part of the new Kleenex model.

  - (internal) aereport start/stop testscript is moved from plugin to runner


Kleenex
  - Introducing a new clean / testbed orchestration standard model
    and base classes.

  - A warning is generated if devices are specified without a cleaner class.
    The user may choose to ignore these warnings if they are bringing up
    a dynamic topology of virtual devices.

  - Moved all content from ``ats.bringup`` into ``ats.kleenex``.
    ``ats.bringup`` package is scheduled for deprecation and attempts to
    include it now cause warnings.

  - Moved XR-UT orchestrator to cisco_shared ``dyntopo`` package.

    - The ``bringup`` decoupled tool has been scheduled to be deprecated.

    - The ``dyntopo`` cisco_shared package offers an ``xrutbringup``
      decoupled tool that provides equivalent functionality.

    - The ``-orchestrator`` parameter no longer shows up in the decoupled
      tools' ``-help`` display (as the orchestrator is now hardcoded for
      each decoupled bringup tool).

  - If no orchestrator is specified, a warning is thrown and the
    XR-UT orchestrator is selected by default.  In an upcoming release
    this behavior will be removed and orchestrator specification will
    become mandatory.

  - ``-testbed_file`` easypy argument is now used to specify testbeds
    containing only actual devices.

  - ``-logical_testbed_file`` easypy argument is used to specify
    testbeds containing actual or logical devices.

  - Bringup reserves the right to create its own topology name.
    Now when the user specifies a value under ``topology/name`` in their
    logical testbed file, this value is moved under ``topology/alias``.
    If the user specifies both ``topology/name`` and ``topology/alias``
    a warning is generated that states ``topology/name`` is ignored.

  - Deprecated ``is_logical`` device key in the logical testbed file.

  - When ``-clean_scope=job`` is specified via the easypy command line,
    bringup no longer creates a separate file ``JobLog.bringup``.
    Instead, all bringup logs are now included in the JobLog.

  - Renamed the ``-bringup_no_mail`` option on the decoupled bringup tool
    to ``-no_mail`` to better align with the easypy option of the same name.

  - For one release only, the ``-testbed_file`` parameter, if it points to
    a file that contains logical routers, is treated like the
    ``-logical_testbed_file`` parameter, and a warning is raised.

  - Introduced support for bringup ``-clean_file`` migration.  This support
    will be removed in the next release.

  - Added support for "empty bringup", where bringup is attempted without
    any logical devices, but a static ``-testbed_file`` is provided.
    This was done for bringup/clean integration.

  - The topology is no longer launched and torn down
    if no logical devices are specified.
    This allows the kleenex tool to run more efficiently.

Tgn
  - The old tgn module is now moved as an independent cisco-shared
    ``hltapi`` package with new features added. Refer to `HLTAPI Changelog`_

    This is a *non-backwards compatible change*. Modify your scripts and change
    your import statements:

    .. code-block:: python

        # before
        from ats.tgn.hltapi import Ixia, Pagent

        # after
        from hltapi import Ixia, Pagent

  - added support for Spirent TestCenter HLTAPIs in the new HLTAPI cisco-shared
    package

  - added support for tight integration with topology YAML files and device
    objects in the new HLTAPI cisco-shared package

.. _HLTAPI Changelog: http://wwwin-pyats.cisco.com/cisco-shared/html/hltapi/docs/changelog/index.html

Topology
  - Now file-like objects may be loaded.

  - Added new `squeeze<ats.topology.testbed.Testbed.squeeze>` method to allow
    users to crop a testbed to a wanted subset of itself.

  - The key ``iou`` is scheduled for removal in the next release.

  - Removed ``logical`` and ``multinode_requested`` from the testbed YAML
    schema, since these keys are only used for logical testbed YAML now.

  - Removed ``tcl_clean`` keys from from the testbed YAML schema. Please read
    :ref:`kleenex_index` and :ref:`topology_kleenex_integration` on how the new
    model clean integration model works.

  - updated schema to accomodated latest connection manager integration model.


Miscellaneous
  - pyATS documentation is now versioned, you can now see old releases and
    their documentations

  - `PieStack`_ is now officially rolled out as the support platform

  - introduced a new internal warning (specifically, ``DeprecationWarning``)
    system

  - install script now displays warnings if you are installing Python-2 versions
    of pyATS

  - install script now hints about the default ATS tree ``/auto/pysw``

.. _PieStack: http://piestack.cisco.com/

*And, as usual, a plethora of bug fixes in addition to potential new bugs that
we are neither aware of, nor able to zap... yet.*

**1433 unittests and counting**
