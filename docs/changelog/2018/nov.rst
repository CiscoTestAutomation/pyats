November 2018
=============

Nov 19, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.utils``, v5.0.3
    ``pyats.cisco``, v5.0.3 (internal only)


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.utils ats.cisco

Changes
^^^^^^^

    - `Operator` for the `Find` apis are now copyable.
    - removed httplib2 dependency and now uses requests instead
