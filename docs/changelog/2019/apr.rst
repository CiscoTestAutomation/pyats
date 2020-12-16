April 2019
==========

Apr 30, 2019 - pyATS v19.4
--------------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.4
    ``pyats.aereport``, v19.4
    ``pyats.aetest``, v19.4
    ``pyats.async``, v19.4
    ``pyats.cisco``, v19.4.3
    ``pyats.connections``, v19.4
    ``pyats.datastructures``, v19.4
    ``pyats.easypy``, v19.4.2
    ``pyats.examples``, v19.4
    ``pyats.kleenex``, v19.4.1
    ``pyats.log``, v19.4
    ``pyats.results``, v19.4
    ``pyats.robot``, v19.4
    ``pyats.tcl``, v19.4
    ``pyats.templates``, v19.4
    ``pyats.topology``, v19.4
    ``pyats.utils``, v19.4.3

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Changes
^^^^^^^

- added new ``pyats.configuration`` module for central configuration support

- introducing new ``pyats.datastructures.Configuration`` class.

- introducing new ``pyats.datastructures.NestedAttrDict`` class.

- now supports sending emails using SMTP server through TLS/SSL.

- Kleenex now supports a virtual device type of ``routem``.

- Cisco-internal installer now uses https to access BitBucket and uses
  /router/bin/curl if it exists (otherwise, system default curl is used).

