June 25, 2018
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.8


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

    - testbed.clean.yaml is now written to the archive on clean failure.


.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.topology``, v4.1.3


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.topology

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.topology

Changes
^^^^^^^

    - Further refactoring of the fix made in v4.1.2 to support
      logical devices (which do not have aliases).

June 22, 2018
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.topology``, v4.1.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.topology

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.topology

Changes
^^^^^^^

    - fixed a bug where devices were allowed to have the same alias within a
      testbed


June 20, 2018
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.7


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

    - fixed a bug with rerun feature where testcases containing special
      characters were not being rerun correctly



June 10, 2018
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.6


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

    - provided workaround in easpy plugins crashing due to
      https://bugs.python.org/issue33395
