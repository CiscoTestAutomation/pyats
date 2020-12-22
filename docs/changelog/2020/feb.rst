February 2020
=============

Feb 27, 2020
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.2.1
    ``pyats.reporter``, v20.2.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats
    bash$ pip install --upgrade pyats.reporter

    # Cisco Internal Developers
    bash$ pip install --upgrade ats
    bash$ pip install --upgrade ats.reporter

Changes
^^^^^^^

CLI
  - Adjusted command load order to prevent unwanted version mismatch exception

Reporter
  - Fix dumping arbitrary object to YAML with immutable dict


Feb 25, 2020
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.2
    ``pyats.aereport``, v20.2
    ``pyats.aetest``, v20.2
    ``pyats.async``, v20.2
    ``pyats.cisco``, v20.2
    ``pyats.connections``, v20.2
    ``pyats.datastructures``, v20.2
    ``pyats.easypy``, v20.2
    ``pyats.kleenex``, v20.2
    ``pyats.log``, v20.2
    ``pyats.reporter``, v20.2
    ``pyats.results``, v20.2
    ``pyats.robot``, v20.2
    ``pyats.tcl``, v20.2
    ``pyats.topology``, v20.2
    ``pyats.utils``, v20.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats

Changes
^^^^^^^

Easypy
  - New --no-archive-subdir and --archive-name cli options

  - Fixed an issue with unicode displays in ``--html-logs`` feature.

  - Removed some unused code in runinfo for legacy s3 and kafka support

Log
  - Fixed logviewer for parsing robot result, when missing some keys in
    result.yaml

Topology
  - Now allowing integer password to be specified in credential block.

Utils
  - Supporting the case when the copied file has no group "Fileutils"

Reporter
  - Prevent tag creation on dumping arbitrary types to results.yaml

AEtest
  - Steps now capture exception tracebacks in result data

  - Better exception message when trying to start child steps under a finished
    step

  - Fix the affix functions of the various skip processors

Kleenex
  - Introducing python 3.8 support to Kleenex/Bringup.


Feb 6, 2020
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.topology``, v20.1.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.topology

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.topology

Changes
^^^^^^^

- Any testbed YAML credential member whose name contains "password" is now
  loaded as a secret string.  This allows for other kinds of passwords to be
  specified under a credential.


Feb 5, 2020
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.1
    ``pyats.aereport``, v20.1
    ``pyats.aetest``, v20.1
    ``pyats.async``, v20.1
    ``pyats.cisco``, v20.1
    ``pyats.connections``, v20.1
    ``pyats.datastructures``, v20.1
    ``pyats.easypy``, v20.1
    ``pyats.kleenex``, v20.1
    ``pyats.log``, v20.1
    ``pyats.reporter``, v20.1
    ``pyats.results``, v20.1
    ``pyats.robot``, v20.1
    ``pyats.tcl``, v20.1
    ``pyats.topology``, v20.1
    ``pyats.utils``, v20.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats

Changes
^^^^^^^

- now guesses the closest option when user provides a bad choice with
  ``pyats`` CLI command.

- ``testbed.connect()`` now supports passing additional ``kwargs`` to each
  connection it establishes.

- `pyats version` command now updated to `pyats version check`.

- added `pyats version update` command to allow seamless update of pyATS
  versions from one release to another without using `pip`

- added quiet mode for scp and sftp in FileUtils to suppress printing and logging copy progress

- fixed a bug in TRADe upload (internal Cisco only) where when processing took
  too long and timed-out, the exception wasn't raised properly
