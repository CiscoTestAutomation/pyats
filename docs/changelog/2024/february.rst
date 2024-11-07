February 2024
==========

February 27 - Pyats v24.2 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.2 
    ``pyats.aereport``, v24.2 
    ``pyats.aetest``, v24.2 
    ``pyats.async``, v24.2 
    ``pyats.cisco``, v24.2 
    ``pyats.connections``, v24.2 
    ``pyats.datastructures``, v24.2 
    ``pyats.easypy``, v24.2 
    ``pyats.kleenex``, v24.2 
    ``pyats.log``, v24.2 
    ``pyats.reporter``, v24.2 
    ``pyats.results``, v24.2 
    ``pyats.robot``, v24.2 
    ``pyats.tcl``, v24.2 
    ``pyats.topology``, v24.2 
    ``pyats.utils``, v24.2 

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Add                                       
--------------------------------------------------------------------------------

* docker
    * Added aarch64 python 3.12 builder


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* makefile
    * Added aiohttp package

* easypy.plugins
    * kleenex.py
        * Added logic to update device recovery information to clean data.
    * kleenex.py
        * Added dyntopo entrypoints to take cli args from the workers.


--------------------------------------------------------------------------------
                                     Modify                                     
--------------------------------------------------------------------------------

* aetest-pkg
    * Removed unused and deprecated imports
    * Renamed the file to fix UT issue

* easypy-pkg
    * assertEquals is not support for 3.12 hence changed to assertEqual

* utils-pkg
    * updated import utils with exec_module instead of load_module


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* installer
    * Modified installer script to remove dependency on pypi.org (Cisco internal use only)

* pyats.connections
    * utils.py
        * Fixed bug with set_parameters and added unittest

* pyats.connections.bases
    * Move wrapper to before connection so that `connect` can be wrapped

* easypy.plugins
    * Modified XunitPlugin
        * Updated post_job method and separated xunit xml generation code
        * Added conditional xunit_include_logs parameter to generate xunit.xml


