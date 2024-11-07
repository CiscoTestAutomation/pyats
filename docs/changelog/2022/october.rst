October 2022
==========

October 25 - Pyats v22.10
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v22.10
    ``pyats.aereport``, v22.10
    ``pyats.aetest``, v22.10
    ``pyats.async``, v22.10
    ``pyats.cisco``, v22.10
    ``pyats.connections``, v22.10
    ``pyats.datastructures``, v22.10
    ``pyats.easypy``, v22.10
    ``pyats.kleenex``, v22.10
    ``pyats.log``, v22.10
    ``pyats.reporter``, v22.10
    ``pyats.results``, v22.10
    ``pyats.robot``, v22.10
    ``pyats.tcl``, v22.10
    ``pyats.topology``, v22.10
    ``pyats.utils``, v22.10

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

* pyats.utils
    * Updated markup processer to support keys() as target
    * Support %EXTEND_LIST markup to extend one or more lists as a value
    * Modified recursive dict update to support hierarchical use of EXTEND_LIST markup

* log
    * Modified archive.py
        * Added await to fix the bug where exposed API calls for results does not return file contents.

* reporter
    * Added Schema
        * schema for results.json
    * Modified commands.py
        * added pyats validate results <filename>


