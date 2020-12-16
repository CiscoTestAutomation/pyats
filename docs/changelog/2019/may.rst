May 2019
========

May 28, 2019 - pyATS v19.5
--------------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.5
    ``pyats.aereport``, v19.5
    ``pyats.aetest``, v19.5
    ``pyats.async``, v19.5
    ``pyats.cisco``, v19.5
    ``pyats.connections``, v19.5
    ``pyats.datastructures``, v19.5
    ``pyats.easypy``, v19.5
    ``pyats.examples``, v19.5
    ``pyats.kleenex``, v19.5
    ``pyats.log``, v19.5
    ``pyats.results``, v19.5
    ``pyats.robot``, v19.5
    ``pyats.tcl``, v19.5
    ``pyats.templates``, v19.5
    ``pyats.topology``, v19.5
    ``pyats.utils``, v19.5

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Changes
^^^^^^^

- ``pyats.utils.fileutils`` now allows case-insensitive server name
  lookups in the testbed server block.

- Topology YAML file now supports a new ``credentials block``. This will be 
  used in the near future for new credential (eg, username password) storage.
  Stay tuned for more updates

- Kleenex fix to allow proper merging of content from logical
  to actual testbed when multiple interfaces share a common link.

- ``Unicon`` is now a standard requirement for connections module

- Now defaults to ``~/.pyats/archive`` and ``~/.pyats/runinfo`` folder for 
  standard log/archive output (unless Cisco internal ``cisco`` module is 
  installed, where it reverts back to current behavior)

- Moved per-user pyATS configuration file location to ``~/.pyats/pyats.conf``

- Added support to specify default archive/directory location in pyATS 
  configuration file

- Fixed a bug where AEtest does not return ``Errored`` when it crashes and burns 
  hard outside of design intention

- Easypy now handles a corner condition where if a Task failed to generate
  meaningful results (or inconsistent results), it raises a flag in the report,
  and returns error code 1 in the command line

- removed ``dd`` usage from logging utils

- fixed a bug in AEReport where the current hostname had to be resolvable by
  DNS or by local ``hosts`` file. AEReport server now starts strictly on
  ``127.0.0.1`` serving localhost instead.

- Kleenex loader no longer raises an exception if no images are present
  but -invoke_clean has not been specified in `pyats run job`.

