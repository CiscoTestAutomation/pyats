April 2020
==========

April 29, 2020
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.easypy``, v20.4.1
    ``pyats.log``, v20.4.3

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.log

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.log

Changes
^^^^^^^

- Fixed a `pyats logs view` live viewing bug, circumventing https://github.com/cython/cython/issues/2273

- Fixed issue with multiprocessing on Mac, circumventing https://bugs.python.org/issue33725s

- More regular Liveview UI refresh


April 28, 2020
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.4
    ``pyats.aereport``, v20.4
    ``pyats.aetest``, v20.4
    ``pyats.async``, v20.4
    ``pyats.cisco``, v20.4
    ``pyats.connections``, v20.4
    ``pyats.datastructures``, v20.4
    ``pyats.easypy``, v20.4
    ``pyats.kleenex``, v20.4
    ``pyats.log``, v20.4
    ``pyats.reporter``, v20.4.1
    ``pyats.results``, v20.4
    ``pyats.robot``, v20.4
    ``pyats.tcl``, v20.4
    ``pyats.topology``, v20.4
    ``pyats.utils``, v20.4


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
 - Testbed files that fail to be loaded are now included in archive

 - Easypy and pyats configurations are now written to the archive

Reporter
 - Reporter client can now subscribe to the server to receive live updates with
   asyncio

 - Reporter Unix file socket will be made in runinfo directory as reporter.sock
   if the path is not too long, otherwise made in a temporary location and
   symlinked to the runinfo directory

 - Add line counts in report for logs associated with a test section

 - Reporting for sections defined within plugins

 - Kleenex to use the pyATS Reporter as a plugin instead of a Kleenex-specific
   reporter

 - Kleenex no longer generates cleanresults files during clean

 - Kleenex will now report a device as `Failed` as long as a test section inside
   clean reports a failure.

Liveview
 - Liveview server plugin for displaying live test progression data to xpresso

 - A new UI supports both static logviewer and liveview

 - User can either use 'pyats run job job.py --liveview' to enable liveview when
   starting a job, or use command 'pyats logs view --liveview' anytime when a
   job is running

 - Support viewing genie clean result, display processors and plugins as well

pyATS Contribution Package
 - New package `pyats.contrib` which is a collection of open-source extensions
   for the pyATS framework

 - Installs as a part of `pip install pyats[full]`