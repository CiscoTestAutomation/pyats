June 2021
========

June 29, 2021
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.6
    ``pyats.aereport``, v21.6
    ``pyats.aetest``, v21.6
    ``pyats.async``, v21.6
    ``pyats.cisco``, v21.6
    ``pyats.connections``, v21.6
    ``pyats.datastructures``, v21.6
    ``pyats.easypy``, v21.6
    ``pyats.kleenex``, v21.6
    ``pyats.log``, v21.6
    ``pyats.reporter``, v21.6
    ``pyats.results``, v21.6
    ``pyats.robot``, v21.6
    ``pyats.tcl``, v21.6
    ``pyats.topology``, v21.6
    ``pyats.utils``, v21.6

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Feature List
^^^^^^^^^^^^

--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* fileutils
    * Added check server name to prevent showing unneeded warnings

* pyats
    * Updated manifest schema
    * pyats manifest run will use 'default' arguments if no profile is specified
    * Updated manifest implementation to fix usage of easypy command

* log
    * change socketio and engineio version requirements to

* pyats.filetransferutils
    * Updated FileUtilsBase.from_device method
        * Added `protocol` parameter for protocol sub-plugins

* reporter
    * Modified Explorer
        * Added __bool__ to check for when no sections exist in reporter
    * Added health_result and health_summary in results.json
    * Modified ReporterServer
        * When getting a section wait for log lines to be counted first

* kleenex
    * Update url clean-image CLI handling to allow url style syntax for files
    * Fixed loading of multiple clean files with a mixture of alias and real device names
    * Fix log handlers to avoid duplicate output on terminal

* cisco (internal)
    * Removed PackagesDiscoveryPlugin
        * removed PackagesDiscoveryPlugin class.
    * Modified UploadSubcommand
        * Changed help message to inform that logs are uploaded to TaaS Logviewer
        * Added Link to Logviewer when archive was sucessfully uploaded

* logs
    * Update logviewer to check archive and runinfo location set in pyats.conf,

* connection manager
    * Use 'cli' as default alias for xrUT
    * Modified logic for single connection 'via' to be compatible with xrUT

* markup processor
    * Allow string replacement with %CALLABLE markup for non-string return values

* testbed loader
    * Updated to use genie.testbed.load instead of genie.conf.utils.converter

--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* topology
    * added testbed methods to execute against devices in parallel
    * The following methods are available
        * testbed.connect
        * testbed.disconnect
        * testbed.destroy
        * testbed.execute
        * testbed.configure
        * testbed.parse


