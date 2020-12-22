January 2019
============


Jan 28, 2019
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.kleenex``, v5.1.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.kleenex

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

    - Update kleenex standalone tool to upload logfiles when
      an early exception is seen.



Jan 23, 2019 - pyATS v5.1.0
---------------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v5.1.0
    ``pyats.aereport``, v5.1.0
    ``pyats.aetest``, v5.1.0
    ``pyats.async``, v5.1.0
    ``pyats.cisco``, v5.1.0
    ``pyats.connections``, v5.1.0
    ``pyats.datastructures``, v5.1.0
    ``pyats.easypy``, v5.1.0
    ``pyats.examples``, v5.1.0
    ``pyats.kleenex``, v5.1.0
    ``pyats.log``, v5.1.0
    ``pyats.results``, v5.1.0
    ``pyats.tcl``, v5.1.0
    ``pyats.templates``, v5.1.0
    ``pyats.topology``, v5.1.0
    ``pyats.utils``, v5.1.0

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Changes
^^^^^^^

Reporter
    - AEreport ``-html_logs`` can now display logs which contains \< \>.

    - ``-html_logs`` now supports a specified target location in addition
      to defaulting to ``$PWD``

Easypy
    - support for new ``pyats run job`` CLI command - all documentation now
      reflects so

      - deprecated old ``easypy`` command - with no current plan for removal,
        as this will break many tools.

    - support for new POSIX style arguments in the command line, instead of
      custom style only used in pyATS.

    - fixed easypy polluting ``logging.root.handlers`` on import

    - log level setting is now applied to root logger instead of just easypy.

    - modified how plugins define their own parsers - now updates the main
      parser instead of each plugin owning their custom parser.

      - **deprecated** the old way of how parsers are defined in plugins.

    - ``Task()`` class now automatically passes the runtime object to downstream
      harness if required

    - internal modularization optimizations

Robot
    - support for running RobotFramework scripts within Easypy, with the
      results aggregated into Easypy report

    - support for ``pyats run robot`` CLI command - running a Robot script
      through Easypy without generating a job file

Topology
    - added ``yamllint`` to ``pyats validate testbed`` command - now prints out
      lint errors and warnings.

Miscellaneous:
    - removed httplib2 as a dependency and switched to requests instead

    - Tuned the progress notice for multiprotocol file transfer utilities
      sftp plugin to be less noisy.

    - fixed CLI core engine, now displays colours properly

    - harmonized internally how parser help is generated

    - ``find`` api enhancements

    - Fixed pyats pkg UT - now passes when no TCL tree is set.


Jan 14, 2019
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.kleenex``, v5.0.8
    ``pyats.easypy``, v5.0.4


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.kleenex pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.kleenex ats.easypy

Changes
^^^^^^^

    - Kleenex

      - Fix bringup bug seen where content from the logical testbed was
        not properly merged when multiple logical interfaces are
        connected to a single logical link (LAN segment).

    - Kleenex, Easypy

      - Fixed a bug where all devices were being cleaned when clean_devices
        was specified as an empty list.
