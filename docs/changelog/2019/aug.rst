August 2019
===========

August 27, 2019 - pyATS v19.8
-----------------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.8
    ``pyats.aereport``, v19.8
    ``pyats.aetest``, v19.8
    ``pyats.async``, v19.8
    ``pyats.cisco``, v19.8
    ``pyats.connections``, v19.8
    ``pyats.datastructures``, v19.8
    ``pyats.easypy``, v19.8
    ``pyats.kleenex``, v19.8
    ``pyats.log``, v19.8
    ``pyats.results``, v19.8
    ``pyats.robot``, v19.8
    ``pyats.tcl``, v19.8
    ``pyats.topology``, v19.8
    ``pyats.utils``, v19.8

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats

Changes
^^^^^^^

- exception display on loading bad/non-existent script file is now more
  intuitive

- Now properly handling empty credential blocks if specified.

- Now allowing a list of IPv6 interfaces to be specified on an interface.

- Prevent 100% success rate in situation where a testscript fails to run.

- Now allowing device aliases to be specified in clean YAML in cleaners and
  groups.

- Introduction of %{testbed.x} and %{testbed.self.y} clean YAML markups that
  reference content in the testbed YAML file.

- UTC timestamp confguration option


August 6, 2019
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.cisco``, v19.7.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.cisco

Changes
^^^^^^^

- Updated the ``pyats version`` command to ignore deprecated pyats packages.

August 9, 2019
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.aereport``, v19.7.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.report

Changes
^^^^^^^

- Reverted 'name' tag back to 'jobName' in ResultsSummary.xml

August 30, 2019
---------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.robot``, v19.8.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.robot

Changes
^^^^^^^

- Fixed robot harness result returning