November 2017
=============


Nov 22, 2017
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v3.3.9


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

- easypy

  .. warning::

          **Backwards-incompatiable change**.  Please add the
          ``-invoke_clean`` parameter to your easypy command if you want
          clean to be executed.

  - Now clean is only executed when the ``-invoke_clean`` parameter is
    specified.

  - If ``-clean_file`` is specified it is parsed and loaded into your
    ``testbed.devices[<device_name>].clean`` object(s) as usual, whether or not
    ``-invoke_clean`` is specified.  Please see :ref:`clean_file` for details.




Nov 20, 2017
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v3.3.3


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aetest

Changes
^^^^^^^

- AEtest

  - Enhanced the logger to auto escape invalid XML character in logged message
    before transmitting to AEReport over XMLRPC.


Nov 7, 2017
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v3.3.8


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

- Easypy

  - Fixed a bug where archive top-level directory was still being created when
    ``-no_archive`` option is provided.
