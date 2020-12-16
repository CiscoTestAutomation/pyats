May 2020
========

May 26, 2020
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.5
    ``pyats.aereport``, v20.5
    ``pyats.aetest``, v20.5
    ``pyats.async``, v20.5
    ``pyats.cisco``, v20.5
    ``pyats.connections``, v20.5
    ``pyats.datastructures``, v20.5
    ``pyats.easypy``, v20.5
    ``pyats.kleenex``, v20.5
    ``pyats.log``, v20.5
    ``pyats.reporter``, v20.5
    ``pyats.results``, v20.5
    ``pyats.robot``, v20.5
    ``pyats.tcl``, v20.5
    ``pyats.topology``, v20.5
    ``pyats.utils``, v20.5


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats

Changes
^^^^^^^
 - CEL 8 Support

 - RobotFramework logs now written to a directory named after task to prevent conflict
   when using same script multiple times.

 - The message from each RobotFramework test is now set as the reason for each
   result in the pyATS report.

 - More consistent reporting on the parameters for all parts of a testscript.
   (testscript, testcase, test sections)

 - Handling for creating unix sockets when the runinfo dir is in a symlinked
   path

.. note::
    For Cisco internal users:

    The May 2020 release also includes an updated installer. You must `set up a
    Bitbucket access token
    <https://confluence.atlassian.com/bitbucketserver/personal-access-tokens-939515499.html>`_
    to enable secure cloning in the future.


May 13, 2020
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.log``, v20.4.4

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.log

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.log

Changes
^^^^^^^

- Fixed issue with Log Viewer parsing result for processor


May 7, 2020
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.datastructures``, v20.4.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.datastructures

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.datastructures

Changes
^^^^^^^

- Fixed issue with listdict.reconstruct() handling tuples
