March 2020
==========

Mar 3, 2020
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.reporter``, v20.2.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.reporter

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.reporter

Changes
^^^^^^^

Reporter
  - No longer dumping arbitrary object __dict__ to results.yaml

