August 2020
===========

August 25, 2020
---------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.8
    ``pyats.aereport``, v20.8
    ``pyats.aetest``, v20.8
    ``pyats.async``, v20.8
    ``pyats.cisco``, v20.8
    ``pyats.connections``, v20.8
    ``pyats.datastructures``, v20.8
    ``pyats.easypy``, v20.8
    ``pyats.kleenex``, v20.8
    ``pyats.log``, v20.8
    ``pyats.reporter``, v20.8
    ``pyats.results``, v20.8
    ``pyats.robot``, v20.8
    ``pyats.tcl``, v20.8
    ``pyats.topology``, v20.8
    ``pyats.utils``, v20.8

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Feature List
^^^^^^^^^^^^

.. list-table::
    :header-rows: 1

    * - Feature
      - Docs
      - Whats New

    * - Programmatic Testbed Validation
      - :ref:`Docs <testbed-index>`
      - | The same functionality from the command `pyats validate testbed`
        | can be accessed from an importable function within Python.
        .. code-block:: python

            from pyats.topology.utils import validate_testbed

            testbed = {...}

            problems = validate_testbed(testbed)

            if problems['warnings']:
                log.warning('Warnings generated')
            for warn in problems['warnings']:
                log.warning(warn)

            if problems['exceptions']:
                log.error('Failed to validate testbed')
            for exc in problems['exceptions']:
                log.error(exc)

    * - Processor Reporting
      - :ref:`Docs <aetest_processors>`
      - | Processor reporting can now be defined within the
        | :ref:`pyats.conf <pyats_configuration>` file. This is replacing the
        | `aereport.processors` option. Processors that have reporting enabled
        | will appear with other Test Sections and Steps in the Log Viewer.
        .. code-block:: text

            [aetest]
            processors.report = True


Other Changes
^^^^^^^^^^^^^

Logviewer
  - Added colorful icons to each section indicating the section type

Topology
  - Updated topology schema:
    Added chassis_type under device, and connections, connections_arguments
    under connections/defaults to support multiple unicon connections.
  - Allow credentials to be pickled/depickled.

Connections
  - Closed hanging connection log files after connection destroy or disconnect

Reporter/Utils
  - Fix writing UIDs as an unhashable type in the results YAML.

Kleenex
  - Simplified logging when clean stage fails