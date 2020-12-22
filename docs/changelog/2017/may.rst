May 2017
========

May 24, 2017
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v3.3.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aetest

Changes
^^^^^^^

* Now supports test script ``__version__`` in ``float`` format.


May 11, 2017
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v3.3.1
    ``ats.tims``, v3.3.1
    ``ats.aereport``, v3.3.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.easypy
    bash$ pip install --upgrade ats.tims
    bash$ pip install --upgrade ats.aereport

Changes
^^^^^^^

* added ``-tims_config_id`` option to Easypy for TIMS config_id field.


May 8, 2017 - pyATS v3.3.0
--------------------------

    *May pyATS be with you.*

`v3.3.0` is a major release, **gearing up the infrastructure for release to
Cisco external customers as an independent product.** Soon, pyATS will be
available through licensing to any Cisco direct customer (and as well, used in
the realm of Cisco Advanced Services & Technical Assistance Center.)

    - increased modularity & pluggable-ness, removing core dependency to
      Cisco engineering environment and tooling.
    - deep integration with Jenkins with the release of pyATS Jenkins plugins.


In addition, along with pyATS ``v3.3.0`` we are announcing the release of the
following packages in cisco-shared:

Genie
    introducing Genie SDK & Genie Harness: enabling automation engineers to
    write Stimulus, Events & Activities style testcases (a.k.a triggers &
    verifications) using Genie ops and conf objects. For more details, see
    Genie website: http://wwwin-genie.cisco.com/

Jenkins Plugins
    no more free-style projects & command-line maddness. Along with `v3.3.0` we
    are also releasing two Jenkins plugins:

        - **pyATS Project Plugin:** allowing users to create pyATS-focused
          projects directly within Jenkins, recognizing all pyATS featuresets,
          and running scripts seamlessly as a build step on docker and/or remote
          servers.

        - **pyATS Results Plugin:** enabling Jenkins to understand and display
          Cisco automation results, including result values such as `Blocked`,
          `PASSX`, and allowing post-build result archive upload to S\ :sup:`3`\
          (next-generation SSR), TRADe, and Kafka in the future.

Webdriver
    with the push towards Cisco DNA/SDN solutions, many people are heading
    strong into web-based testing. Search no more: ``WebDriver`` is a new Cisco
    pyATS PyPI package, designed to make the use of Selenium simpler & easier
    in pyATS. It enables users to define their browser test environment in
    their topology file, and removes the need to write boilerplate code for
    many UI actions. See `WebDriver Documentation`_ for details.

Dyntopo.laas
    Introducing modelling of management links and interfaces to better
    interwork with Genie.  See `Dyntopo.Laas Documentation`_ for details.

Uniclean
    Created plugins for IOS-XE ASR/ISR and 3850 Newton stack.
    Extensive refactoring of the existing NX-OS plugin.
    See `Uniclean Documentation`_ for details.

Unicon
    Now offering a ``learn_hostname`` feature to allow better integration with
    some kinds of LaaS-NG reserved devices.  Moonshine support from Ensoft.
    See `Unicon Documentation`_ for details.

.. _WebDriver Documentation: http://wwwin-pyats.cisco.com/cisco-shared/webdriver/latest/index.html

.. _Dyntopo.Laas Documentation: wwwin-pyats.cisco.com/cisco-shared/dyntopo/latest/laas/changelog/2017/may.html#may-8

.. _Unicon Documentation: wwwin-pyats.cisco.com/cisco-shared/unicon/latest/changelog/2017/may.html#may-8

.. _Uniclean Documentation: wwwin-pyats.cisco.com/cisco-shared/uniclean/latest/changelog/2017/may.html#may-8

.. csv-table:: New Module Versions
    :header: "Modules", "Version"
    :widths: 30, 70

    ``ats``, v3.3.0
    ``ats.aereport``, v3.3.0
    ``ats.aetest``, v3.3.0
    ``ats.async``, v3.3.0
    ``ats.connections``, v3.3.0
    ``ats.datastructures``, v3.3.0
    ``ats.easypy``, v3.3.0
    ``ats.examples``, v3.3.0
    ``ats.kleenex``, v3.3.0
    ``ats.log``, v3.3.0
    ``ats.results``, v3.3.0
    ``ats.tcl``, v3.3.0
    ``ats.templates``, v3.3.0
    ``ats.tims``, v3.3.0
    ``ats.topology``, v3.3.0
    ``ats.utils``, v3.3.0

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # install new pyATS version
    bash$ pip install --upgrade ats


Changes
^^^^^^^

    | *The reason to move on: courage.*
    | *The courage to move on and do something new that betters all of us.*

Documentation
    - Installation documentation now moved to pyATS Wiki:
      https://wiki.cisco.com/pages/viewpage.action?pageId=80375302

    - Support documentation now moved to pyATS Wiki:
      https://wiki.cisco.com/pages/viewpage.action?pageId=80917403

    - Git documentation now moved to pyATS Wiki:
      https://wiki.cisco.com/display/PYATS/Bitbucket+Repo

Easypy
    - ``-no_log_copy`` is now deprecated, and replaced with ``-no_upload``.

    - AEreport TIMS results file now includes AEtest diagnostic/version
      information

    - Easypy now accepts a new argument ``-job_uid``, a unique identifier for
      this run. This is repoted as ``jobid`` field in AEReport.

    - updated Easypy to accept TIMS global custom attributes with any space when
      wrapped with curly brackets.

    - Easypy ``runtime`` is now no-longer a true global. Within the code,
      it is now passed by reference instead of by import.

      - in order to maintain backwards compatibility, a default, global instance
        of Easypy is perserved for 99.9% of command-line usage.

    - Introduced new multiprocessing datastructure manager under
      ``runtime.synchro`` attribute. Use this to synchronize data (dict, lists
      etc) between your tasks and your job file

    - Easypy plugin system received a major overhaul. See plugin documentation
      for details of the new design.

        - The legacy environment config file input has been removed and replaced
          with global and per run config files.

        - Plugin base class changed. Now plugins gain the ability to handle
          their own exceptions.

        - When plugins exception out in a pre-section, its post-section will
          now be called to cleanup.

    - Now supports uploading archives to S\ :sup:`3`\  (next-generation SSR),
      and Kafka, in addition to TRADe.

    - Fixed a bug preventing Easypy from generating html email report using
      customized html template

    - jobfile ``main()`` now accepts a ``runtime`` argument that describes the
      current runtime environment

    - redesigned how easypy command line arguments parsers are collected &
      displayed

    - reporting mechanism received a total overhaul.

        - introducing a new mechanism for reporter propagation

        - original reporting functionality is no longer a plugin, and thus is
          no longer dependent on the plugin system order. All user plugins
          should now be able to read report results at the end.

        - the integration of this new reporting mechanism is not yet connected
          to AEtest's reporters. This integration will occur in the next release.

AEReport
    - AEReport server now less prone to become a lingering process if the parent
      process terminates unexpectedly.

Kleenex
    - clean engine now allows cleaner to modify ``device.clean``, which is sent
      back from the worker to the main process and the user's ``device.clean``
      updated.

    - The dyntopo.xrut orchestrator is no longer loaded by default when
      migrating a pre-v3.0.0 bringup clean YAML file.

    - Added cli_parse_helpers to utils, upgraded kleenex_main and kleenex easypy
      plugin to accept ``-clean_device "dev1 dev2 dev3"``.

    - Fixed a bug preventing a Kleenex/bringup micro-clean and a typical clean from
      being done in the same integrated easypy run.

    - Kleenex now invokes cleaners properly when clean and bringup are combined.

    - Support added for kleenex clean timeouts

Topology
    - Now doing markup before validation phase in testbed loader to better
      enable Genie/LaaS-NG integration.

    - Added ``%I{logical_interface_name}`` construct to testbed YAML markup
      processor to allow actual interface name to be substituted.  This is
      useful when combining clean post-config with Kleenex bringup.

    - Refactored core topology objects to split common with pyATS-core specific
      functionality. Now sharing base classes with dyntopo/common.

    - Enhanced markup debugging to provide better information to the user.

    - Removed topology custom block usage warning

AEtest
    - Skipped testcase due to ``-ids`` and ``-groups`` argument usage no longer
      show up as ``SKIPPED`` and is no longer displayed instead

    - Fixed a bug in AEtest where objects with `__testcls__` attributes were
      being mistakenly treated as AEtest sections.

    - Fixed a bug in AEtest where standalone execution always overwrote AETest's
      module logger level to INFO regardless of user input.

    - now provides a better exception when Test sections misses 'self' keyword

    - Fixed a bug in AEtest where task id with forward slash make runinfo file
      fails to create and total execution fails

    - AEtest now preserves the overwritten test section execution order as its
      parent

    - Raised the logging severity level from info to error when ``failed``,
      ``errored``, or ``aborted`` result method is called from AEtest test
      sections

    - now provides a better exception when sections have duplicate uids.

    - Discovery functionality reworked: now returns a list of test instances
      instead of classes

    - AEtest processors now support exception processors for customized
      exception handling

    - Fixed a bug where post-processors are not run when a section error out.

    - Fixed a bug where section UID is overwritten during looping

    - Fixed a bug where decorators on top of AEtest section decorators didn't
      work.

Connections
    - ``ConnectionPool`` workers now rotate and distribute work evenly amongst
      workers.

    - new connection hook feature, enabling users to hook onto a connection 
      service and modify its behaviors before/after.

Miscellaenous
    - new ``classproperty`` decorator in datastructures
    - new ``MetaClassFactory`` class in datastructures
    - new ``ArgsPropagatingParser`` class in utils
    - Fixed a bug with WeakList where casting it to `tuple` yielded a tuple of
      weak references instead of actual objects
    - Installation updated to include support for Bitbucket

*And, as usual, a plethora of bug fixes in addition to potential new bugs that
we are neither aware of, nor able to zap... yet.*

**1971 unittests and counting**
