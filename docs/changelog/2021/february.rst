February 2021
=============

February 23, 2021
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.2
    ``pyats.aereport``, v21.2
    ``pyats.aetest``, v21.2
    ``pyats.async``, v21.2
    ``pyats.cisco``, v21.2
    ``pyats.connections``, v21.2
    ``pyats.datastructures``, v21.2
    ``pyats.easypy``, v21.2
    ``pyats.kleenex``, v21.2
    ``pyats.log``, v21.2
    ``pyats.reporter``, v21.2
    ``pyats.results``, v21.2
    ``pyats.robot``, v21.2
    ``pyats.tcl``, v21.2
    ``pyats.topology``, v21.2
    ``pyats.utils``, v21.2

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

    * - Automatic Genie Testbed Conversion
      - :ref:`Docs <testbed-index>`
      - | When loading a testbed file using pyATS, if Genie libraries are
        | installed, the testbed will automatically be converted to support
        | Genie APIs.
        .. code-block:: text

            $ pyats shell --testbed-file testbed.yaml
            Welcome to pyATS Interactive Shell
            ==================================
            Python 3.8.7 (v3.8.7:6503f05dd5, Dec 21 2020, 12:45:15)
            [Clang 6.0 (clang-600.0.57)]

            >>> from pyats.topology.loader import load
            >>> testbed = load('testbed.yaml')
            -------------------------------------------------------------------------------
            In [1]: type(testbed)
            Out[1]: genie.libs.conf.testbed.Testbed

            In [2]: dev=testbed.devices.R1

            In [3]: type(dev)
            Out[3]: genie.libs.conf.device.iosxe.device.Device

    * - Default Connection Aliases
      - :ref:`Docs <connection_manager>`
      - | Connection aliases now depend on plugin used. The 'default' alias
        | points to 'cli' by default. This can be changed via
        | `device.default_connection_alias`

        +--------------------------------------------+
        | *Default Connection Alias*                 |
        +-----------+--------------------------------+
        | **Alias** | **Class**                      |
        +-----------+--------------------------------+
        | cli       | unicon.Unicon                  |
        +-----------+--------------------------------+
        | rest      | rest.connector.Rest            |
        +-----------+--------------------------------+
        | netconf   | yang.connector.netconf.Netconf |
        +-----------+--------------------------------+
        | ncdiff    | yang.ncdiff.ModelDevice        |
        +-----------+--------------------------------+


Other Changes
^^^^^^^^^^^^^

Kleenex
  * Enhanced 'clean_image' and 'clean_platform' arguments to support the
    callable markup
  * Fixed clean results upload error msg - previously, it raised exception
    "Xpresso results upload failed" even if upload succeeded at 3rd retry

ConnectionManager
  * Fix to close user connection log handlers on destroy()

Log
  * Add argument "--hostname" to logviewer
  * Raise exception when no result file is found

Reporter
  * Fix UnicodeEncodeError when writing XML results file

Topology
  * Testbed validation via CLI via normal testbed loader






