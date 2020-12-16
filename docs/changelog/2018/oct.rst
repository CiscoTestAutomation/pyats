October 2018
============

Oct 29, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats``, v5.0.1
    ``pyats.cisco``, v5.0.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats ats.cisco

Changes
^^^^^^^

    - modified the new ``pyats`` command to no longer require a virtual
      environment to function


Oct 25, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.kleenex``, v5.0.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.kleenex

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

    - Now allowing the bringup topology name to be specified via a new
      CLI parameter -topology_name.


Oct 24, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.easypy``, v5.0.1
    ``pyats.kleenex``, v5.0.1
    ``pyats.utils``, v5.0.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy pyats.kleenex pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy ats.kleenex ats.utils

Changes
^^^^^^^

    - Extended -clean_devices syntax to allow groups of devices to be
      cleaned sequentially via easypy or the kleenex standalone tool.
      Devices in each group are still cleaned in parallel.



Oct 11, 2018
------------

.. note::

    this update is only available to internal cisco developers.

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.cisco``, v5.0.1
    ``pyats.utils``, v5.0.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.cisco ats.utils

Changes
^^^^^^^

    - relaxing the git executable lookup mechanism, and default to cisco's
      git at ``/usr/cisco/bin/git`` in case it's not in user's path.

    - fixed a bug in utils ``FlexLoader`` that resulted in module names with
      ``.`` prefix.


Oct 10, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.aereport``, v5.0.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.aereport

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.aereport

Changes
^^^^^^^

    - Adding junit-xml dependency for ats.aereport which is needed to generate
      xUnit result.


Oct 9, 2018 - pyATS v5.0.0
---------------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version", "Comments"
    :widths: 10, 30, 70

    ``pyats``, v5.0.0,
    ``pyats.aereport``, v5.0.0,
    ``pyats.aetest``, v5.0.0,
    ``pyats.async``, v5.0.0,
    ``pyats.cisco``, v5.0.0,
    ``pyats.connections``, v5.0.0,
    ``pyats.datastructures``, v5.0.0,
    ``pyats.easypy``, v5.0.0,
    ``pyats.examples``, v5.0.0,
    ``pyats.kleenex``, v5.0.0,
    ``pyats.log``, v5.0.0,
    ``pyats.results``, v5.0.0,
    ``pyats.tcl``, v5.0.0,
    ``pyats.templates``, v5.0.0,
    ``pyats.topology``, v5.0.0,
    ``pyats.utils``, v5.0.0,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Changes
^^^^^^^

Namespace
    The original pyats package naming convention vs the import was confusing
    users in DevNet/customers. This change re-aligns the package name and
    namespace.

    - the pyATS package namespace is now renamed from ``ats`` to ``pyats``.
      All imports are thus reflected as ``from pyats import x``.


    - documentation reflected to reflect this change

    - 100% backwards compatible: all existing codes, libraries and scripts that
      uses the ``ats`` namespace will continue to function sans issues.


Core
    - added ``pyats`` command line infrastructure

    - added ``version`` subcommand that outputs current pyATS version, and any
      available upgrades

Easypy
    - now generates unique runtime folders with millisecond precision,
      avoiding collisions when multiple of the same job is launched
      simultaneously.

    - default task naming changed from ``__task-%s`` to ``Task-%s``, where
      ``%s`` is substituted by the task number

Pcall
    - now all log files generated from Pcall will be copied to main Tasklog
      for simplified viewing

Logging
    - added colours to screen log output

    - logging is now multi-process & multi-thread safe

    - added infrastructure support for eventual log colour support in TaskLog

Topology
    - fixed a bug in topology yaml loader where extends key with relative
      paths did not respect current file location

    - added ``validate testbed`` subcommand that checks provided testbed
      file for consistentency and errors

Utilities
    - fixed fileutils unittests on mac

    - now lazy loads fileutils plugins

    - added flag to yaml loader to preserve order, default to False.
      (since xmlrpc servers cannot marshall OrderedDicts)

    - Introduced ``LegacyImporter`` feature, allowing package developers to
      migrate to new package namespaces/imports without affecting legacy users.

Miscellaneous
    - fix for CVE-2017-18342

    - removed unused package dependencies
