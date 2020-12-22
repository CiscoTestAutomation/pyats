March 2018
==========

Mar 29, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v4.1.1
    ``ats.cisco``, v4.1.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
    
    # DevNet Community
    bash$ pip install --upgrade pyats.aetest pyats.cisco

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.aetest ats.cisco

Changes
^^^^^^^

    - fixed a bug where processors on testcases that inherit from each other
      where not inheriting properly

    - now supports uploading to TRADe via background using ``-bg_upload``
      argument **[Cisco Only]**


Mar 25, 2018 - pyATS v4.1.0
---------------------------

    *What happened to v4.0.0?*

In case you are wondering - we didn't intentionally skip over `v4.0.0`: that 
number was used when pyATS was initially released to 
DevNet [https://developer.cisco.com/site/pyats/] at the end of 2017. 

`v4.1.0` is a new milestone in pyATS release. We've re-aligned internal Cisco
pyATS with the external DevNet version with the help of some new tech. As a
result, the two releases now share the same development branch, features, and
code-base. 

Any internal Cisco-only behavior is plugged back via a new package:
``ats.cisco``, which is only available when pyATS is installed through the
internal Cisco PyPI server.

In addition, pyATS now fully supports Python ``3.5+`` and ``3.6+``, and can now
install and run on Mac OSX platforms.


.. csv-table:: New Module Versions
    :header: "Modules", "Version", "Comments"
    :widths: 10, 70, 20

    ``ats``, v4.1.0, 
    ``ats.aereport``, v4.1.0, 
    ``ats.aetest``, v4.1.0, 
    ``ats.async``, v4.1.0
    ``ats.cisco``, v4.1.0, "new package"
    ``ats.connections``, v4.1.0, 
    ``ats.datastructures``, v4.1.0, 
    ``ats.easypy``, v4.1.0, 
    ``ats.examples``, v4.1.0, 
    ``ats.kleenex``, v4.1.0, 
    ``ats.log``, v4.1.0, 
    ``ats.results``, v4.1.0, 
    ``ats.tcl``, v4.1.0, 
    ``ats.templates``, v4.1.0, 
    ``ats.tims``, "N/A", "package removed - content moved to ``ats.cisco``"
    ``ats.topology``, v4.1.0, 
    ``ats.utils``, v4.1.0, 

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    # (remember to remove defunct packages)
    bash$ pip install --upgrade ats
    bash$ pip uninstall ats.tims

Changes
^^^^^^^

Easypy
    - plugins may now disable itself using ``self.disable = True`` at any 
      pre/post level

    - Added a check to ensure all installed pyATS core packages have the same
      ``{major}.{minor}`` version and thus do not conflict.

    - moved the topology grapher into a cisco-shared ``topographer`` package.

    - now uses ``pwd`` for default log/runinfo storage when, and defaults to
      a more readable archive directory format. **[DevNet Only]**

    - no longer attempts to always create ``users`` directory under 
      ``sys.prefix`` **[DevNet Only]**

    - added new experimental feature ``-html_logs``, which will generate an
      HTML formatted, user-friendly log file inside the job results folder.

    - removed reference to Tcl-ATS in report email

    - now requires ``-invoke_clean`` in order to start a clean even when
      clean file is provided

AEtest
    - support for new class-based context processors and generator-based
      context processors in addition to pre/post and exception processors

    - you can now define processors with arguments in datafiles

    - processors can now be modified (added to) from job file

    - fixed a bug with aetest where processors could not modify section results

    - updated AEtest sections with a new result context implementation

    - steps now also support ``from_exception`` argument

    - all deprecation notices have now been removed - eg, their warnings now
      in full effect. Please update your code accordingly

Connections
    - connection hook exception handlers may now suppress the exception, and
      alter the return value.

    - connection manager now defaults to Unicon **[DevNet Only]**

Cisco
    - this is a new package introduced in `v4.1.0` internal to Cisco. When 
      installed, this package updates your pyATS's instance behavior to be tuned
      for internal Cisco usage. This package is not released to DevNet. 
      **[Cisco Only]**

    - when installed, set default connection class to Csccon **[Cisco Only]**

    - when installed, default easypy upload to TRADe **[Cisco Only]**

    - when installed, enables upload of results to TIMS **[Cisco Only]**

    - when installed, tracks usages in CES **[Cisco Only]**

    - documentation for Cisco-specific behaviors can be found in the Cisco
      pyATS Wiki. **[Cisco Only]**

AEReport
    - AEreport now generates STEP-related information in ``ResultsDetails.xml``.

      - added Step XREF information (source file/line)

    - AEreport now includes a ``success_rate`` value in both the
      ``ResultsDetail.xml`` under each section, and in ``ResultsSummary.xml``.
      This now standardizes how success rates % is calculated.

    - fixed a bug with AEreport not generating log file position for steps

    - fixed a bug in AEreport not accepting None as value type

Tcl
    - support for Tcl non-8.4 **[DevNet Only]**

    - suppoort for Tcl to work without Tcl-ATS **[DevNet Only]**

Logs
    - removed hard-coding earms-trade log link when new logs are forked

Kleenex
    - Extended the role-based image syntax to:
     
      - allow clean images to be populated via remote directory scan filtered
        by inclusion/exclusion patterns.

      - validate the number of expected images for a given role (cardinality).

    - Simplified tracebacks seen during Kleenex clean/bringup operations.

    - Now input testbed and clean YAML files are copied to the log directory.

Topology:
    - Fixed bug in topology.squeeze that was causing erratic results when
      extend_devices_from_links was specified as `False`.

Results:
    - removed Null result (this was an implementation detail)
    - updated ResultContext with new logic, changing results together and 
      automatically rolling up results

Utils
    - Added ``%ENV{environment_variable_name}`` construct to testbed YAML markup
      processor to allow actual environmental value to be substituted.

    - Added ``%CALLABLE{a.b.c}`` and ``%CALLABLE{a.b.c(x,y,z)}`` construct to
      testbed YAML markup processor to allow actual result of callable to be
      substituted.

    - Added ``%INCLUDE{absolute_yaml_file_path}`` construct to testbed YAML
      markup processor to allow content of yaml to be substituted.

    - Updated ``%I{logical_interface_name}`` markup constructor to
      ``%INTF{logical_interface_name}``

    - Added ``%EXTEND_LIST{listname}`` markup constructor to enable YAML-based
      datafiles to extend list types.

    - Moved ``mpip`` managed pip utility into a cisco-shared ``mpip`` package.

    - ``Find`` api can return multi line requirements and merge them together.

    - Added ``NotExists`` to build ``Find`` requirements.

    - Added a new pluggable framework to support multiprotocol file operations
      such as copying files to/from a remote server.  Other value-added 
      operations are also supported, including remote directory listing,
      retrieval of remote file details, and doing rename/delete/chmod on
      remote files.


*And, as usual, a plethora of bug fixes in addition to potential new bugs that
we are neither aware of, nor able to zap... yet.*

**1980 unittests and counting**
