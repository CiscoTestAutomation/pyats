March 2019
==========

March 21, 2019
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.aetest``, v19.0.1
    ``pyats.easypy``, v19.0.1
    ``pyats.kleenex``, v19.0.1
    ``pyats.log``, v19.0.1
    ``pyats.robot``, v19.0.1
    ``pyats.utils``, v19.0.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.aetest pyats.easypy pyats.kleenex pyats.log pyats.robot pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.aetest ats.easypy ats.kleenex ats.log ats.robot ats.utils

Changes
^^^^^^^
    - Introduction of Kleenex reporting.

    - Added 'connect to device' keyword to ats.robot


Mar 4, 2019 - pyATS v19.0
-------------------------

    *Introducing the new calendar-year based version numbering scheme.*

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.0
    ``pyats.aereport``, v19.0
    ``pyats.aetest``, v19.0
    ``pyats.async``, v19.0
    ``pyats.cisco``, v19.0
    ``pyats.connections``, v19.0
    ``pyats.datastructures``, v19.0
    ``pyats.easypy``, v19.0
    ``pyats.examples``, v19.0
    ``pyats.kleenex``, v19.0
    ``pyats.log``, v19.0
    ``pyats.results``, v19.0
    ``pyats.tcl``, v19.0
    ``pyats.templates``, v19.0
    ``pyats.topology``, v19.0
    ``pyats.utils``, v19.0

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Changes
^^^^^^^

Release Format
    - changed to calendar year based versioning scheme

    - Format: ``YY.N(.M)``, where ``YY`` is the release year, ``N`` is the
      this year's minor release level, and ``M`` is the optional patchlevel.

      .. code-block:: text

          Example Versions
          ----------------
               19.0       - this release
               19.0.0     - exactly the same as 19.0
               19.0.1     - first patch/bug fix for this release

Python 3.7 Support
    - v19.0 now supports Python 3.7 release, and continues to seamlessly support
      older Python releases (Python 3.4/3.5/3.6)

    - ``pyats.async`` module had to be renamed to ``pyats.async_``,
      following PEP guidelines: in Python 3.7, ``async`` and ``await`` are now
      reserved keywords (https://docs.python.org/3/whatsnew/3.7.html)

      .. code-block:: python

          # anyone looking to port their source code from Python 34/35/36 to 37
          # should update their script imports:

          # eg, from this
          from pyats.async import pcall

          # to this
          from pyats.async_ import pcall

      Though the new pyATS release is backwards compatible, changing the above
      in your script/code makes it **NON-BACKWARDS COMPATIBLE** to older
      pyATS versions, as the ``pyats.async_`` module doesn't exist pre-v19.0.

      If you are looking to make your code forward AND backwards compatible,
      try the following:

      .. code-block:: python

          # try to import pyats.async
          # if it doesn't exist, try to import pyats.async_
          # note that you can't wrap 'from pyats.async import pcall' in a
          # try/except clause, because merely writing async inline as so
          # will cause the import machinery to reject the file.
          import importlib

          try:
              pcall = importlib.import_module('pyats.async').pcall
          except ImportError:
              from pyats.async_ import pcall

Command Line
    - introduced new ``pyats shell`` command, that saves the end user from
      having to load their own testbed yaml file every time they enter
      interactive shell.

ConnectionManager
    - introduced new ``instantiate()`` and ``instantiate_pool()`` api that
      allows the user to manipulate connection objects before establishing
      connection

Examples
    - all examples updated to use ``pyats run job`` command

Docker Optimizations
    - all pre-built images in Docker Hub (https://hub.docker.com/r/ciscotestautomation/pyats/)
      are now significantly smaller in size due to a new, optimized Dockerfile
