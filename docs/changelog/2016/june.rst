June 2016
=========

June 6, 2016
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.kleenex``, v3.0.6,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex

Changes
^^^^^^^

  - `US58609 <https://rally1.rallydev.com/#/22527801475d/detail/userstory/47470635305>`_

    - Fixed a failing unit test from the previously released version.


June 3, 2016
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions", "Comments"

    ``ats.easypy``, v3.0.3,
    ``ats.kleenex``, v3.0.5,
    ``ats.utils``, v3.0.1,

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex ats.utils ats.easypy

Changes
^^^^^^^

  - `US58609 <https://rally1.rallydev.com/#/22527801475d/detail/userstory/47470635305>`_

    - Now allowing both uppercase and lowercase for ``-loglevel`` arguments to
      kleenex and easypy tools, and also for the ``-bringup_log_level`` argument.

