August 20, 2018
---------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v4.1.6
    ``ats.topology``, 4.1.4

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.topology pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.topology ats.utils

Changes
^^^^^^^

    - Enhancement for multiprotocol file transfer utilities :

        - multiple addresses can be specified per server, where the first
          network reachable address will be preferred.



August 8, 2018
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v4.1.5


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.utils

Changes
^^^^^^^

    - Fixes for multiprotocol file transfer utilities Linux plugin:

        - Now supporting Cisco switching/routing devices acting as servers.
        - Now allowing relative local paths to be specified.


August 7, 2018
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.10


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

    - fixed a bug where when rerun feature is used, unused tasks (not destined
      to rerun) are not initialized properly as processes.
