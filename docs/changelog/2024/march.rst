March 2024
==========

 - Pyats v24.3 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v24.3 
    ``pyats.aereport``, v24.3 
    ``pyats.aetest``, v24.3 
    ``pyats.async``, v24.3 
    ``pyats.cisco``, v24.3 
    ``pyats.connections``, v24.3 
    ``pyats.datastructures``, v24.3 
    ``pyats.easypy``, v24.3 
    ``pyats.kleenex``, v24.3 
    ``pyats.log``, v24.3 
    ``pyats.reporter``, v24.3 
    ``pyats.results``, v24.3 
    ``pyats.robot``, v24.3 
    ``pyats.tcl``, v24.3 
    ``pyats.topology``, v24.3 
    ``pyats.utils``, v24.3 

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
                                      New                                       
--------------------------------------------------------------------------------

* easypy.plugins
    * rerun
        * Added ability to download archive/rerun file from a URL

* pyats.aetest
    * Modified PauseOnPhrase, added collect and custom options

* pyats.cli
    * Migrate abstract
        * Added functionality to the `pyats migrate abstract` command to modify the files in-place with the suggested changes

* easypy
    * plugins(kleenex)
        * add --clean-template-action cli argument to kleenex plugin.

* kleenex
    * loader
        * add logic for loading a template for cleaning the device


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* pyats.connection
    * Service Wrapper
        * Fixed an issue that caused a circular import when using the service wrapper with external connection packages
        * Changed `BaseServiceWrapper` to `ServiceWrapper`
        * Changed `ServiceWrapper` import from `from pyats.connections.bases import BaseServiceWrapper` to `from pyats.connections import ServiceWrapper`


