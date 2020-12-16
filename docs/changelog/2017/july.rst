July 2017
=========

July 14, 2017
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v3.3.5


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

* Reverted previous bug fix, as behavior was design intent.


July 10, 2017
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v3.3.4


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

* Bug fix : Users may now specify a nonexistent directory and expect
  it to be created when using ``-archive_dir`` or ``-runinfo_dir``.

July 3, 2017
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v3.3.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.utils

Changes
^^^^^^^

* Bug fix : The mpip command now works on CEL72 ADS machines.
