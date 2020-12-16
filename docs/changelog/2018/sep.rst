September 2018
==============

September 24, 2018
------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.12
    ``ats.kleenex``, v4.1.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

    - Now allowing bringup users to override task-scope bringup configuration
      directly from the job file.

    - Now allowing bringup of virtual devices with type 'n9000v'.


September 14, 2018
------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v4.1.7
    ``ats.easypy``, v4.1.11


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.utils pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.utils ats.easypy

Changes
^^^^^^^

    - Fixed a bug in easypy when mail_html argument is used, only text email
      format was sent

September 8, 2018
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v4.1.7

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.utils

Changes
^^^^^^^

    - Enhancement for multiprotocol file transfer utilities :

        - Now logging a descriptive warning in checkfile informing the
          details of any file stat failure encountered.
