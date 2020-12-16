December 2019
=============

December 17, 2019
-----------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v19.12
    ``pyats.aereport``, v19.12
    ``pyats.aetest``, v19.12
    ``pyats.async``, v19.12
    ``pyats.cisco``, v19.12
    ``pyats.connections``, v19.12
    ``pyats.datastructures``, v19.12
    ``pyats.easypy``, v19.12
    ``pyats.kleenex``, v19.12
    ``pyats.log``, v19.12
    ``pyats.reporter``, v19.12
    ``pyats.results``, v19.12
    ``pyats.robot``, v19.12
    ``pyats.tcl``, v19.12
    ``pyats.topology``, v19.12
    ``pyats.utils``, v19.12

Changes
^^^^^^^

Topology
  - Added %ASK{user specified prompt} markup, deprecated ASK() for passwords.

  - Added %ENC{encoded string, optional alternate representer} markup,
    deprecated ENC() for passwords.

FileUtils
  - Added getspace method to FileUtils for getting available disk space info
    from remote server

AEtest
  - Added separate description for steps. The step description no longer
    defaults to the name if not specified.

Reporter
  - Change Results.yaml -> results.yaml

  - Results.yaml version 2.1  processors now divided into 'pre' and 'post'
    lists.

  - Including processors as sections in ResultsDetails.xml with configuration
    option to disable.

Kleenex
  - Added clean by platform by introducing the platforms: key to the Kleenex
    schema.

  - The cleaners block of the clean YAML is now autopopulated if not specified
    by the user.  All clean YAML devices (including those specified via platform
    and group) are assigned to a default cleaner as long as they also exist in
    the testbed content as well.

  - Accepts multiple clean files from cli

  - Markups are now processed in the logical testbed file if specified.
