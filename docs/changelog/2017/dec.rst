December 2017
=============


Dec 4, 2017
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v3.3.10


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

- fixed a bug with easypy integration & Jenkins, where if ``-xunit`` argument
  is enabled with pyATS Jenkins plugin, an exception is thrown regarding TRADe
  log url
