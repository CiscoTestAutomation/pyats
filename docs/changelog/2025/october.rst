October 2025
==========

October 28 - Pyats v25.10
------------------------



.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v25.10
    ``pyats.aereport``, v25.10
    ``pyats.aetest``, v25.10
    ``pyats.async``, v25.10
    ``pyats.cisco``, v25.10
    ``pyats.connections``, v25.10
    ``pyats.datastructures``, v25.10
    ``pyats.easypy``, v25.10
    ``pyats.kleenex``, v25.10
    ``pyats.log``, v25.10
    ``pyats.reporter``, v25.10
    ``pyats.results``, v25.10
    ``pyats.robot``, v25.10
    ``pyats.tcl``, v25.10
    ``pyats.topology``, v25.10
    ``pyats.utils``, v25.10




Changelogs
^^^^^^^^^^
--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* yaml.markup
    * Added support for multiple callables in a single line
    * Added support for callable with attribute, e.g. `%CALLABLE{datetime.datetime.now().year}`

* kleenex-pkg
    * Moved the logic of merging jit clean to _update_device_cleaning_info_using_template

* pyats
    * Removed all usage of deprecated pkg_resources module in favor of importlib.metadata where possible.


