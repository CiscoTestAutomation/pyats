November 2015
=============


Nov 11, 2015
------------


.. csv-table:: Module Versions
    :header: "Modules", "Versions"

    ``ats.examples``, v2.1.3

Changes
"""""""

- Examples should reflect using ``-testbed_file`` rather than ``-tf``.


Upgrade Instructions
""""""""""""""""""""

- if you are upgrading from ``v2.0.1+``, it is pretty straightforward:

  .. code-block:: bash

      bash$ pip install --upgrade ats.topology ats.examples ats.bringup

- if you are upgrading from a lower version, please refer to ``v2.0.0`` and
  ``v2.0.1`` upgrade instructions first.



Nov 2, 2015
-----------


.. csv-table:: Module Versions
    :header: "Modules", "Versions"

    ``ats.bringup``, v2.1.2
    ``ats.examples``, v2.1.2
    ``ats.topology``, v2.1.1

Changes
"""""""

- Added support for invoking IOSv and NXOSv (Titanium) on a LaaS backend server.
- Added support for invoking multiple parallel LaaS topologies via the
  :ref:`async_index`.
- Changed `is_logical` testbed configuration key to `logical`, but the old form
  is still supported.
- Added working examples of using bringup to launch and test a
  topology on a LaaS backend.
- Extended the testbed schema to support LaaS server configuration for
  bringup.



Upgrade Instructions
""""""""""""""""""""

- if you are upgrading from ``v2.0.1+``, it is pretty straightforward:

  .. code-block:: bash

      bash$ pip install --upgrade ats.topology ats.examples ats.bringup

- if you are upgrading from a lower version, please refer to ``v2.0.0`` and
  ``v2.0.1`` upgrade instructions first.


