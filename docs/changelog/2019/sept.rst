September 2019
==============

September 30, 2019
------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.easypy``, v19.9.2
    ``pyats.reporter``, v19.9.1

Changes
^^^^^^^

- Fixed issue with step descriptions not being included in final email report
- Improved Reporter logging and decreased verbosity
- jobfile now included in Results.yaml file
- Re-added option to create HTML logs

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.easypy``, v19.9.1

Changes
^^^^^^^

- ``RuninfoSymlinkPlugin`` will now silently log error if it could not create
  runinfo symlink (during race conditions)

September 24, 2019 - pyATS v19.9
--------------------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.9.2
    ``pyats.log``, v19.9.1

Changes
^^^^^^^

- Fixed a packaging issue.

- The ``pyats logs view`` command now displays a better error message if no
  logs can be found.


.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.9
    ``pyats.aereport``, v19.9
    ``pyats.aetest``, v19.9
    ``pyats.async``, v19.9
    ``pyats.cisco``, v19.9
    ``pyats.connections``, v19.9
    ``pyats.datastructures``, v19.9
    ``pyats.easypy``, v19.9
    ``pyats.kleenex``, v19.9
    ``pyats.log``, v19.9
    ``pyats.reporter``, v19.9
    ``pyats.results``, v19.9
    ``pyats.robot``, v19.9
    ``pyats.tcl``, v19.9
    ``pyats.topology``, v19.9
    ``pyats.utils``, v19.9

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats

Changes
^^^^^^^

- Introducing the new ``pyats.reporter`` package.
  This new reporting mechanism adds YAML report generation for more flexible
  reporting and human readability.

- Kleenex : Fixed bringup failure when user-defined device class was specified
  in the logical testbed content.

- Introducing the new ``pyats logs`` CLI command, which allows log archive
  listing and viewing in a local browser.

