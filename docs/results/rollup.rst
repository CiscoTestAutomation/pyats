.. _result_rollup:

Results Rollups
===============

Result roll-up is the act of combining one or more results together and yielding
a new, summary result. Rolling up results with ``results`` module objects is
as simple as adding them together using the Python ``+`` operator.

.. code-block:: python

    # Example
    # -------
    #
    #   rolling multiple results objects

    # import all result codes
    from pyats.results import (Passed, Failed, Aborted, Errored,
                             Skipped, Blocked, Passx)

    # roll up some results together
    Passed + Failed
    # Failed

    Passx + Errored
    # Errored

    # chaining multiples
    Passed + Aborted + Blocked
    # Blocked

    # assign a result to variable
    result = Passed

    # roll up that result against another
    result += Failed


Roll-up Rules
-------------

When results are rolled-up together, their final summary result are calculated
by referencing the chart below:

.. list-table:: Result Roll-up Table
    :header-rows: 1
    :stub-columns: 1

    * - Results
      - ``Failed``
      - ``Passed``
      - ``Aborted``
      - ``Blocked``
      - ``Skipped``
      - ``Errored``
      - ``Passx``

    * - ``Failed``
      - ``Failed``
      - ``Failed``
      - ``Aborted``
      - ``Failed``
      - ``Failed``
      - ``Errored``
      - ``Failed``

    * - ``Passed``
      - ``Failed``
      - ``Passed``
      - ``Aborted``
      - ``Blocked``
      - ``Passed``
      - ``Errored``
      - ``Passx``

    * - ``Aborted``
      - ``Aborted``
      - ``Aborted``
      - ``Aborted``
      - ``Aborted``
      - ``Aborted``
      - ``Aborted``
      - ``Aborted``

    * - ``Blocked``
      - ``Failed``
      - ``Blocked``
      - ``Aborted``
      - ``Blocked``
      - ``Blocked``
      - ``Errored``
      - ``Blocked``

    * - ``Skipped``
      - ``Failed``
      - ``Passed``
      - ``Aborted``
      - ``Blocked``
      - ``Skipped``
      - ``Errored``
      - ``Passx``

    * - ``Errored``
      - ``Errored``
      - ``Errored``
      - ``Aborted``
      - ``Errored``
      - ``Errored``
      - ``Errored``
      - ``Errored``

    * - ``Passx``
      - ``Failed``
      - ``Passx``
      - ``Aborted``
      - ``Blocked``
      - ``Passx``
      - ``Errored``
      - ``Passx``

.. note::
    To read the table, take the first row with the first column. Pick any
    result of the first row with any result of the first column, find the
    cross point, and this is the result you would get after roll up.

    Here is an example on how to read the table :
    ``Passed`` + ``Failed`` = ``Failed``

When multiple results are added together in a single line, consider that
operation to be the same as breaking it down to multiple intermediate two-item
roll-ups:

.. code-block:: python

    # Example
    # -------
    #
    #   performing multiple rollups

    # import all result codes
    from pyats.results import (Passed, Failed, Aborted, Errored,
                             Skipped, Blocked, Passx)

    # consider this
    Passed + Failed + Aborted + Errored

    # the same as performing
    result = Passed + Failed
    result = result + Aborted
    result = result + Errored

