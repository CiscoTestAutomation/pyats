October 2020
============

Octoboer 27, 2020
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.10
    ``pyats.aereport``, v20.10
    ``pyats.aetest``, v20.10
    ``pyats.async``, v20.10
    ``pyats.cisco``, v20.10
    ``pyats.connections``, v20.10
    ``pyats.datastructures``, v20.10
    ``pyats.easypy``, v20.10
    ``pyats.kleenex``, v20.10
    ``pyats.log``, v20.10
    ``pyats.reporter``, v20.10
    ``pyats.results``, v20.10
    ``pyats.robot``, v20.10
    ``pyats.tcl``, v20.10
    ``pyats.topology``, v20.10
    ``pyats.utils``, v20.10

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats

Changes
^^^^^^^

Easypy
  - Fix for rerun cli argument parsing for improved support with pyATS Jenkins
    Plugin

Topology/Utils
  - Improved testbed validation with line number identification for issues in
    testbed YAML file

October 1, 2020
---------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.aetest``, v20.9.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.aetest

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.aetest

Changes
^^^^^^^
  - Improved unwrapping of processors for getting the correct arguments
