January 2017
============

January 20, 2017
----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v3.2.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.utils


Changes
^^^^^^^

    - Minor refactoring, delivered to fix a breakage seen with the most recent
      release of ats.topology.


January 19, 2017
----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.topology``, v3.2.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.topology


Changes
^^^^^^^

    - Added a new option ``extend_devices_from_links`` to testbed.squeeze,
      giving users more fine-grained control.

January 17, 2017
----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.kleenex``, v3.2.1
    ``ats.easypy``, v3.2.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex ats.easypy


Changes
^^^^^^^

    - Fixed a bug preventing Kleenex Bringup and Clean from being run together
      (newly brought up devices were being ignored instead of cleaned).

