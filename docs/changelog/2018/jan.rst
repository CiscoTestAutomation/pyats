January 2018
============

Jan 8, 2018
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v3.3.4
    ``ats.tims``, v3.3.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.aetest
    bash$ pip install --upgrade ats.tims

Changes
^^^^^^^

    - Now detecting and truncating excessively long filenames when writing to
      runinfo/taskresults.  These files now contain the full name if truncation
      occurs.

    - Minor refactoring, provide warning and filter out unpicklable characters
      when attempting to generate TIMS results file.
