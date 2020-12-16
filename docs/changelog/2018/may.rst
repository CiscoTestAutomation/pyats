May 2018
========

May 24, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v4.1.4


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.utils

Changes
^^^^^^^

    - Fixed a bug in multiprotocol file transfer utilities, now URLs may be specified
      via the server alias, fully qualified server name or IP address.

May 17, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.5


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

    - added additional debug information to easypy generated ``env.txt``


May 15, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v4.1.3


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.aetest

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.aetest

Changes
^^^^^^^

    - fixed an issue where logs were creeping from one section to another in
      the final report


May 3rd, 2018
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.robot``, v4.1.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.robot

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.robot

Changes
^^^^^^^

    - fixed robot pkg install dependencies
