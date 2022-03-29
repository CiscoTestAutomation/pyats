March 2022
==========

March 29 - Pyats v22.3 
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.3 
    ``pyats.aereport``, v22.3 
    ``pyats.aetest``, v22.3 
    ``pyats.async``, v22.3 
    ``pyats.cisco``, v22.3 
    ``pyats.connections``, v22.3 
    ``pyats.datastructures``, v22.3 
    ``pyats.easypy``, v22.3 
    ``pyats.kleenex``, v22.3 
    ``pyats.log``, v22.3 
    ``pyats.reporter``, v22.3 
    ``pyats.results``, v22.3 
    ``pyats.robot``, v22.3 
    ``pyats.tcl``, v22.3 
    ``pyats.topology``, v22.3 
    ``pyats.utils``, v22.3 

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
                                      Fix                                       
--------------------------------------------------------------------------------

* alpine builder
    * Update alpine builder container to alpine3.15

* pyats.aetest
    * Fix datafile loading

* kleenex
    * Kleenex_main.py
        * Fixed the bug for email report when the Taas log is not uploaded.

* reporter
    * Modified ReporterServer
        * reporter.log only generated when running in verbose mode with -v


--------------------------------------------------------------------------------
                                    Updated                                     
--------------------------------------------------------------------------------

* aetest
    * Fixed step result handling inside a processor


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* aetest
    * Fixed -v handling
        * debug logging appears in Aetest by -v option


