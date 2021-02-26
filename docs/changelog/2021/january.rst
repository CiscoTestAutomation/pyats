January 2021
============

January 27, 2021
----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.1
    ``pyats.aereport``, v21.1
    ``pyats.aetest``, v21.1
    ``pyats.async``, v21.1
    ``pyats.cisco``, v21.1
    ``pyats.connections``, v21.1
    ``pyats.datastructures``, v21.1
    ``pyats.easypy``, v21.1
    ``pyats.kleenex``, v21.1
    ``pyats.log``, v21.1
    ``pyats.reporter``, v21.1
    ``pyats.results``, v21.1
    ``pyats.robot``, v21.1
    ``pyats.tcl``, v21.1
    ``pyats.topology``, v21.1
    ``pyats.utils``, v21.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Other Changes
^^^^^^^^^^^^^
Topology/Utils
  - Enhanced testbed and clean YAML file validation for Xpresso
    (environment-independent validation)

Utils
  - Enable markup references in YAML to be used in callable
    %CALLABLE{func(%{path1},%{path2})}
  - Fixed %INCLUDE{} markup in YAML breaking references

Reporter
  - Possible socket path length incresed to 120

Log
  - Fixed logviewer/liveview to show results detail page instead of overview
    page by default
  - Command ```pyats logs view abc.zip``` now opens abc.zip directly instead of
    result list page
  - Faster loading of result list page - UI now requests for correct number of
    results instead of parsing 100 results at once


