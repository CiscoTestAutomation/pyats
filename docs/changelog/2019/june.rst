June 2019
=========

June 25, 2019 - pyATS v19.6
---------------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.6
    ``pyats.aereport``, v19.6
    ``pyats.aetest``, v19.6
    ``pyats.async``, v19.6
    ``pyats.cisco``, v19.6
    ``pyats.connections``, v19.6
    ``pyats.datastructures``, v19.6
    ``pyats.easypy``, v19.6
    ``pyats.examples``, v19.6
    ``pyats.kleenex``, v19.6
    ``pyats.log``, v19.6
    ``pyats.results``, v19.6
    ``pyats.robot``, v19.6
    ``pyats.tcl``, v19.6
    ``pyats.templates``, v19.6
    ``pyats.topology``, v19.6
    ``pyats.utils``, v19.6

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Changes
^^^^^^^

- now prints deprecation warnings in pyats cli

- fixed a bug with regex for file listing match in FileUtils ftp plugin

- fixed a bug with Easypy job file loader where it does not add job directory
  to ``sys.path``.

- updated SMTP server customization documentation to reflect latest uses of
  pyATS configuration file

- [Cisco Internal only] fixed a bug in ``pyats.cisco`` TIMS uploading module 
  where ``archive_file`` is not uploaded as an attribute field