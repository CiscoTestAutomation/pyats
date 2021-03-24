July 2019
=========

July 30, 2019 - pyATS v19.7
---------------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.7
    ``pyats.aereport``, v19.7
    ``pyats.aetest``, v19.7
    ``pyats.async``, v19.7
    ``pyats.cisco``, v19.7
    ``pyats.connections``, v19.7
    ``pyats.datastructures``, v19.7
    ``pyats.easypy``, v19.7
    ``pyats.kleenex``, v19.7
    ``pyats.log``, v19.7
    ``pyats.results``, v19.7
    ``pyats.robot``, v19.7
    ``pyats.tcl``, v19.7
    ``pyats.topology``, v19.7
    ``pyats.utils``, v19.7

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats

Deprecation Notice
^^^^^^^^^^^^^^^^^^

- ``pyats.templates`` and ``pyats.examples`` packages are completely removed
  as packages, and are replaced with alternate functionality:

  - Templating is now done through ``pyats create`` command.

  - Examples is now moved to GitHub: https://github.com/CiscoTestAutomation/examples

Changes
^^^^^^^

- updated pyATS packaging and now allows for optional package installations:

  - ``pip install pyats``
  - ``pip install pyats[library]``
  - ``pip install pyats[template]``
  - ``pip install pyats[robot]``
  - ``pip install pyats[full]``

- fixed a bug in ``utils.yaml.Loader()`` where ``extends:`` key did not properly
  resolve markup syntax before loading the extension YAML file.

- YAML loading (including topology yaml loader) now supports loading using
  ``~`` in path (eg, from user home)

- Kleenex and easypy are now copying the clean YAML into the archive prior to
  attempting to load it, to improve support/debug following clean load
  failures.

- fixed a bug with ``pcall`` wasting time

- added ``pyats validate datafile`` command

- added ``pyats create project`` command, creating a pyATS project from
  cookiecutter template

- new ``Testbed.connect()`` convenience api, allowing asynchronous connection
  establishment to multiple devices in the testbed.

- ConnectionPool can now start directly based on YAML file ``pool_size`` if
  ``connect(via=<name>)`` is used (eg, a via is provided, and the connection
  block for that via defines a ``pool_size``)

- fixed a bug in ``ConnectionPool`` where worker allocation wait-delay-backoff
  algorithm was too aggressive and wasted time

- deprecated ``ConnectionManager.instantiate_pool()`` and ``.start_pool()``
  api: harmonized into ``.connect()`` and ``.instantiate()``

- ConnectionPool now starts and stops using threads at supercharged speeds

- TaskLog will now contain thread id and name if there are more than one thread
  currently running

- added the ability to change job name in job file using
  ``runtime.job.name = x``

- Added support for credential password encryption via secret string feature.
  This includes a new ``pyats secret`` CLI command.
  Passwords may now be specified in the testbed YAML in encrypted form.

- added credential lookup fallback to ``default`` credential if it exists.

- added manual input of credential passwords defined as ``ASK()``.

- added ``-skip_teardown`` command-line argument that ensures any brought-up
  topology is not torn down (making it the user's responsibility to do so).

- env.txt now encodes as secret strings those environment variables that
  match the pyats configuration ``[secrets] env.hide_pattern``.

- File transfer utils fixes:

  - Fixed issue with remote ftp directory listings seen on some servers.

  - Added option to not strip leading file/path name, which is needed by
    some servers.

  - Server auth is first taken from the credential named after the selected
    protocol, or ``default`` if not available.

- added new WebInteraction API for tests that rely upon human interation to
  decide result.

- added configuration options for alternative topology classes.
