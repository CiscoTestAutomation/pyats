July 2016
=========

July 26, 2016 - pyATS v3.1.0
----------------------------

    *Newer is usually better!*

Building on the new foundations set forth by ``v3.0.0``, ``v3.1.0`` introduces 
an arsenal of exciting new, mostly backward compatible features:

    - Support for 64-bit Python
    - Customizable Easypy HTML reports
    - Support for Easypy :ref:`easypy_rerun`
    - Step-debug feature revamp
    - Introduction of a new ``mpip`` tool for managed ``pip`` upgrade/downgrade
    - Removed hard-coded virtual environment dependency
    - Generic :ref:`generic_find` object
    - AEtest custom script discovery & section ordering
    - Topology graph generation (as part of Easypy)


.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats``, v3.1.0
    ``ats.aereport``, v3.1.0,
    ``ats.aetest``, v3.1.0,
    ``ats.async``, v3.1.0,
    ``ats.connections``, v3.1.0, 
    ``ats.datastructures``, v3.1.0,
    ``ats.easypy``, v3.1.0,
    ``ats.examples``, v3.1.0,
    ``ats.kleenex``, v3.1.0,
    ``ats.log``, v3.1.0,
    ``ats.results``, v3.1.0,
    ``ats.tcl``, v3.1.0,
    ``ats.templates``, v3.1.0,
    ``ats.tims``, v3.1.0,
    ``ats.topology``, v3.1.0,
    ``ats.utils``, v3.1.0,


In addition, along with pyATS ``v3.1.0``` we are releasing the following
packages in cisco-shared:

Abstract_ (new)
    package enabling token-based library abstraction, enabling
    users to build os/platform/release/feature/etc and reference them 
    dynamically in their scripts without hard-coded imports.

`Yang Connector`_ (new)
    pyATS connection class, implementing YANG/NETCONF connection over SSH using
    Paramiko. 

DynTopo_ (updated)
    LaaS-NG users may now request L1 links with a variety of speed and media
    options.

Genie_ (updated)
    Design uplift, including attribute helpers, CliBuilder, and managed
    attributes.

MetaParser_ (updated)
    Uplifted MetaParser package with integrated support for abstraction.

.. _Abstract: http://wwwin-pyats.cisco.com/cisco-shared/abstract/html/

.. _DynTopo: http://wwwin-pyats.cisco.com/cisco-shared/dyntopo/html/

.. _Genie: http://wwwin-pyats.cisco.com/cisco-shared/genie/html/

.. _MetaParser: http://wwwin-pyats.cisco.com/cisco-shared/metaparser/html/

.. _Yang Connector: http://wwwin-pyats.cisco.com/cisco-shared/yang/connector/html/

.. _custom_discovery: http://wwwin-pyats.cisco.com/documentation/latest/aetest/control.html#custom-discovery-and-order


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # install new pyATS version
    bash$ pip install --upgrade ats


Changes
^^^^^^^
   
AEreport
  - Modified `generate_xunit` to reflect similar test cases count between xUnit
    and pyATS result count.

  - Now supports step objects.

  - Runtime calculation is now being done properly when a task dies suddenly.

AEtest
  - Major improvements in step debug feature, including:
    
    - A new more streamlined schema featuring regex-based
      device and step name specification

    - User defined functions may now be specified

    - Now supports nested steps

  - New discovery engine, supporting user defined custom discovery classes. Now
    users have the ability to alter the testcase/section discovery and ordering
    processes. For more information, refer to :ref:`aetest_discovery_class`
    documentation
  
  - Pause on phrase enhancement - touching the pause file shuts down the timer, 
    allowing users to debug at their leisure.
    
  - Affix functionality for ``skip``, ``skipIf``, ``skipUnless`` decorators

  - Skipped testcases are no longer reported when skipped due to usage of
    ``uids`` and ``groups`` feature.
  
  - Long names in testcases and steps, are truncated to 80 characters in the
    reports.

  - Fixed a bug in parameter map where backup/restore during ``__call__`` should
    refer only to local parameter

Easypy
  - Refactored Email generation to use the new `EmailMsg` utils module with 
    support for HTML report notifications.

    - attachments are now accepted using MIMEMultipart formats in both HTML and 
      text format

    - Jinja2 templating engine is now used to render the email HTML template

    - now supports custom HTML email templates

  - :ref:`easypy_rerun` functionality: a re-run file is now generated as the end
    of each run. Users may now re-run a given resultset using the re-runf file 
    plus additional rerun conditions. For more information, refer to 
    :ref:`easypy_rerun` documentation

  - Users may now modify the email recipient list through ``easypy.runtime``.

  - Fixed an issue with the easypy email subsystem where email contents with
    embedded braces were not being properly rendered.

  - The runtime directory is now preserved if a ``disk-quota-full`` error occurs

  - Easypy now returns ``1`` (failure) if any job or task plugin exception 
    occurs.

  - Refactored kleenex failure handling, now when the ``-pdb`` command line
    parameter is specified:
    
    - Cleaners are run serially instead of in parallel.
    
    - In the event an exception is thown by a cleaner or bringup worker,
      an interactive debugger is automatically opened at the point of failure. 

  - Refactored plugin exception and return code processing.
    Please see :ref:`easypy_return_codes` for details.

  - Now generates a topology graph in pdf format as part of the run, providing
    a visual reference of their topology input file.

Installation
  - support for 64-bit pyATS installation & python binaries.

  - support for providing alternate git user with ``--git-user`` argument

  - support for no git-checking and/or repository cloning with ``--no-git``
    argument

  - now only automatically installing the csccon (default router connection)
    package.  No longer automatically installing dyntopo, tclclean, hltapi
    packages.

  - updated to latest ``pip`` and ``setuptools``

  - install script now installs ``Csccon`` in addition to all pyATS core
    packages. No other cisco-shared packages are installed by default.

  - environment checks have been tightened up. Installation now also checks for
    ``gcc-c++`` package's existence in addition to existing ones. Server
    without this package may need to install it as root using ``yum``.

Kleenex
  - Now users may overwrite loopback interface configuration coming back from
    the bringup orchestrator.

  - Debug enhancements, including a new kleenex tool ``-debug`` parameter
    (please see :ref:`kleenex_standard_args` for details).
    Debug mode is also selected when the ``-pdb`` command line parameter is
    specified.
    When debug mode is in force:

      - Cleaners are run serially instead of in parallel.
      - If a cleaner or bringup worker throw an exception, an interactive
        debugger is automatically opened at the point of failure.

Tcl
  - Fixed a bug in ``tcl.cast_any()`` where lists were not being properly cast
    when it contains ``Tcl_Obj``

Topology
  - Schema - support for ipv6 hostname translation using ``getaddrinfo``.

  - Grapher - New tool allowing users to generate a network topology graph that
    displays devices and links by using a testbed object.

Utils
  - Standardize email generation library in pyATS (EmailMsg)

  - Refactored unit tests to work more reliably in CI environment.

  - New :ref:`generic_find`: a generic find function, enabling searching for 
    arbitrary objects through a given set of requirements.

Miscellaneous
    - Removed ``sys.environ['VIRTUAL_ENV']`` dependency. Now uses ``sys.prefix``
      instead

    - AEtest, Kleenex, Topology, Utils: added ``extends`` capability to testbed
      YAML loader. Please see :ref:`schema` for details.
      
      - Refactored and harmonized extends processing across testbed, datafile
        and kleenex loaders.

    - New mpip (managed pip) script: ``pip`` wrapper, enabling users to manage
      their package versions & roll-back to earlier versions easier.

*And, as usual, a plethora of bug fixes in addition to potential new bugs that
we are neither aware of, nor able to zap... yet.*

**1811 unittests and counting**


July 4, 2016
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.kleenex``, v3.0.7,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex


Changes
^^^^^^^

  - `DE15484 <https://rally1.rallydev.com/#/22527801475d/detail/defect/57205796721>`_
    - Now properly handling the case in which the logical and actual device
    names are equal.  This is most often seen when doing LaaS-NG orchestration.

  - `US108415 <https://rally1.rallydev.com/#/22527801475d/detail/userstory/57205799628>`_
    - Now detecting loopback interfaces and merging them directly from the
    logical to the actual topology.

  - Fixed a minor debug logging bug introduced in kleenex version 3.0.5.

  - install script updated to include ``--no-git`` argument: disables all git
    checkings & git repository cloning
 
  - pypi server is now updated to support searching:

    .. code-block:: bash

        bash$ pip search ats.aetest
