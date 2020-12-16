December 2018
=============

Dec 20, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.utils``, v5.0.5


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.utils

Changes
^^^^^^^

    - removed an optimization from YAML schema engine that mostly worked by
      sheer luck, and failed in many other conditions.

Dec 14, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.kleenex``, v5.0.7


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.kleenex

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

    - Fix bug introduced in previous version.


Dec 13, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.kleenex``, v5.0.6
    ``pyats.utils``, v5.0.4


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.kleenex

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

    - Now allowing a clean YAML with role-based images to extend a clean
      YAML with list-based images and vice versa.


.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.kleenex``, v5.0.5


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.kleenex

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

    - Fixed clean bug seen when more than one device object is overloaded.


.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.easypy``, v5.0.3
    ``pyats.kleenex``, v5.0.4


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy pyats.kleenex

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy ats.kleenex

Changes
^^^^^^^

    - Added clean_devices to the clean YAML schema.

    - When clean_devices specified as a single list [dev1, dev2, dev3] with
      no sublists, now cleaning specified devices in parallel instead of
      serially.


Dec 3, 2018
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.easypy``, v5.0.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats ats.easypy

Changes
^^^^^^^

    - Easypy argument `-html_logs` now accepts a directory location. The
      html_log will be saved in this location as file `TaskLog.html`.
