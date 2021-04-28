
April 2021
==========

April 27, 2021
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.4
    ``pyats.aereport``, v21.4
    ``pyats.aetest``, v21.4
    ``pyats.async``, v21.4
    ``pyats.cisco``, v21.4
    ``pyats.connections``, v21.4
    ``pyats.datastructures``, v21.4
    ``pyats.easypy``, v21.4
    ``pyats.kleenex``, v21.4
    ``pyats.log``, v21.4
    ``pyats.reporter``, v21.4
    ``pyats.results``, v21.4
    ``pyats.robot``, v21.4
    ``pyats.tcl``, v21.4
    ``pyats.topology``, v21.4
    ``pyats.utils``, v21.4

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Feature List
^^^^^^^^^^^^

.. list-table::
    :header-rows: 1

    * - Feature
      - Docs
      - Whats New

    * - pyATS Manifest
      - :ref:`Docs <manifest>`
      - | The pyATS Manifest uses a file with YAML syntax (the "manifest" file)
        | to capture the runtime requirements, script arguments and
        | execution profile for test scripts.
        .. code-block:: text

            $ cat jobfile.tem
            version: 1

            type: easypy

            arguments:
                configuration: easypy_config.yaml
                mail-html: True

            $ pyats run manifest jobfile.tem
            %EASYPY-INFO: Executing: pyats run job jobfile.py  --configuration "easypy_config.yaml" --mail-html
            ...
            %EASYPY-INFO: Sending report email...
            %EASYPY-INFO: Done!


Other Changes
^^^^^^^^^^^^^

* log
    * Modified LiveView
        * Fix for liveview to handle improved memory model from reporter

* reporter
    * added get_section_ctx() to get section context

* log
    * fixed log liveview ui bug
    * added fullid in liveview
    * fixed log viewing key bindings for page up / down getting stuck
    * fixed files list scroll issue when the list goes beyond the page
    * removed "No log to display” when it should not display that
    * enhanced files list search

* pyats
    * Modified configuration:
      * Added new --pyats-configuration argument to specify an additional
        configuration file to be loaded

