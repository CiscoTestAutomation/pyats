July 18, 2018
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.9

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

    - fixed a bug where sometimes email generation crashes when error message
      contains strings that confuses the formatter
