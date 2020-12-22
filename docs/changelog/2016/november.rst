November 2016
=============

November 28, 2016 - pyATS v3.2.0
--------------------------------

`v3.2.0` introduces some exciting new features:

    - Moonshine is now supported by the XR-UT orchestrator
    - Sunstone is now supported by the LaaS orchestrator
    - Support for Hybrid topology launch combining reservable physical devices
      with spawned virtual devices
    - External link support to enable YANG-based testing on LaaS-spawned VMs

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats``, v3.2.0
    ``ats.aereport``, v3.2.0,
    ``ats.aetest``, v3.2.0,
    ``ats.async``, v3.2.0,
    ``ats.connections``, v3.2.0,
    ``ats.datastructures``, v3.2.0,
    ``ats.easypy``, v3.2.0,
    ``ats.examples``, v3.2.0,
    ``ats.kleenex``, v3.2.0,
    ``ats.log``, v3.2.0,
    ``ats.results``, v3.2.0,
    ``ats.tcl``, v3.2.0,
    ``ats.templates``, v3.2.0,
    ``ats.tims``, v3.2.0,
    ``ats.topology``, v3.2.0,
    ``ats.utils``, v3.2.0,

In addition, along with pyATS ``v3.2.0`` we are releasing the following
packages in cisco-shared:

Genie_ (updated)
    
    - **Genie Ops**: support for learning & representing the operational states 
      of your testbed devices through Genie ops objects.

    - Support for YANG testing using YDK_ and `yang.connector`_

    - Harmonization of feature object structure between CLI/YANG and various
      device platforms

    - Parallel (asynchronous) learning & optimizations using connection pool

    - Metaparser integration for CLI and YANG parser


.. _YDK: http://ydk.cisco.com/py/docs/
.. _yang.connector: http://wwwin-pyats.cisco.com/cisco-shared/yang/connector/html/
.. _Genie: http://wwwin-genie.cisco.com/

DynTopo_ (updated)

    - XR-UT orchestrator support added :

      - Moonshine (EnXR-NG) against Csccon connection implementation

    - LaaS orchestrator support added for :

      - Sunstone (IOSXRv9k)

      - NXOSv, CSR1000v, IOSv / IOSv_pagent,
        IOSXRv (simplex, multinode and HA)

      - the spawning of hybrid topologies containing
        reserved physical devices and dynamically spawned virtual devices.

      - external links

      - remote image copy

.. _DynTopo: http://wwwin-pyats.cisco.com/cisco-shared/dyntopo/html/


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # install new pyATS version
    bash$ pip install --upgrade ats


Changes
^^^^^^^

Easypy

    - Reworked the naming of testbed and clean YAML files copied to
      the easypy archive.

Kleenex and Topology

    - Enhanced Kleenex/bringup documentation to better explain
      actual testbed construction logic.

    - The ``auto_bringup`` key was added to the testbed schema
      and describes additional steps taken during device bringup, the
      results of which are captured in ``DeviceLaunch`` log files.

    - Users wanting to do Kleenex dynamic topology bringup must now
      specify the orchestrator explicitly.
      The dyntopo/xrut orchestrator is no longer selected by default.

Misc
    
    - cumulative bug fixes from minor releases in v3.1.0+

    - preparation for migration to Bitbucket in the new year

*And, as usual, a plethora of bug fixes in addition to potential new bugs that
we are neither aware of, nor able to zap... yet.*

**1823 unittests and counting**



November 14, 2016
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aereport``, v3.1.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aereport


Changes
^^^^^^^

    - Fixed a bug that was preventing xunit report creation
      when operating in XR-UT-tethered mode
      (via the xrut cisco_shared package).



November 9, 2016
----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.kleenex``, v3.1.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex


Changes
^^^^^^^

    - fix a bug in kleenex where it only allowed physical local files and not
      files on flash/harddisk of the target device



November 7, 2016
----------------


.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v3.1.1
    ``ats.aereport``, v3.1.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.easypy ats.aereport


Changes
^^^^^^^

    - fix a bug in Easypy where sometimes custom plugins ran before core plugins
    - fixed a bug in AEreport where sw/hw/fw/tst version information was not
      being uploaded to TIMS (when provided from AEtest)

