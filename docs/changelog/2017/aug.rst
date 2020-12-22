August 2017
===========

Aug 31, 2017
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v3.3.3


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.utils

Changes
^^^^^^^

* Bug fix: find API matched wrong data where syntax is used in find requirements


Aug 14, 2017
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aereport``, v3.3.2
    ``ats.utils``, v3.3.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aereport
    bash$ pip install --upgrade ats.utils

Changes
^^^^^^^

* fixed a bug in AEreport where the testcase's name is not used as TIMS entry
  title.
* Added new parameters `filter_`, `index` and `all_keys` to find API, giving
  users more fine-grained control on matching results.