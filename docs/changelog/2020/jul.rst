July 2020
=========

July 28, 2020
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.7
    ``pyats.aereport``, v20.7
    ``pyats.aetest``, v20.7
    ``pyats.async``, v20.7
    ``pyats.cisco``, v20.7
    ``pyats.connections``, v20.7
    ``pyats.datastructures``, v20.7
    ``pyats.easypy``, v20.7
    ``pyats.kleenex``, v20.7
    ``pyats.log``, v20.7
    ``pyats.reporter``, v20.7
    ``pyats.results``, v20.7
    ``pyats.robot``, v20.7
    ``pyats.tcl``, v20.7
    ``pyats.topology``, v20.7
    ``pyats.utils``, v20.7

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats


Changes
^^^^^^^

- Kleenex standalone Liveview support
- Additional fixes and improvements


July 12, 2020
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats.easypy``, v20.6.1
    ``pyats.log``, v20.6.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy pyats.log

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy ats.log

Changes
^^^^^^^

Logs/Easypy
  - added ``--liveview-callback-url`` and ``--liveview-callback-token``
    option to support running liveview on xpresso for jenkins run.


July 7, 2020
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.6
    ``pyats.aereport``, v20.6
    ``pyats.aetest``, v20.6
    ``pyats.async``, v20.6
    ``pyats.cisco``, v20.6
    ``pyats.connections``, v20.6
    ``pyats.datastructures``, v20.6
    ``pyats.easypy``, v20.6
    ``pyats.kleenex``, v20.6
    ``pyats.log``, v20.6
    ``pyats.reporter``, v20.6
    ``pyats.results``, v20.6
    ``pyats.robot``, v20.6
    ``pyats.tcl``, v20.6
    ``pyats.topology``, v20.6
    ``pyats.utils``, v20.6

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

    * - Processor Reporting Decorator
      - :ref:`Docs <aetest_processors>`
      - | Processors are no longer reported by default. To enable reporting on a
        | processor, the `@aetest.processors.report` decorator has been added.
        .. code-block:: python

            @aetest.processors.report
            def my_processor(section):
                ...

            @aetest.processors.pre(my_processor)
            class MyTestcase(aetest.Testcase):
                ...

    * - Kleenex Arguments
      - :ref:`Docs <kleenex_standard_args>`
      - | Added additional Kleenex arguments.
        .. code-block:: text

            --clean-image  [ ...]
                                Image files for each device
            --clean-platform  [ ...]
                                Image files for each platform
            --clean-separator     Separator between device/platform & image file in arguments clean-image and
                                clean-platform

    * - Liveview Keepalive
      - :ref:`Docs <easypy_usage>`
      - | New `--liveview-keepalive` option to keep the liveview process running
        | after a job has completed.
        .. code-block:: text

            pyats run job myjob.py --liveview --liveview-host 0.0.0.0 --liveview-keepalive

    * - | *pyats.contrib*
        | WebEx Teams Notification Plugin
      - `Readme <https://github.com/CiscoTestAutomation/pyats.contrib/blob/master/src/pyats/contrib/plugins/README.md>`_
      - | A new plugin in the pyats.contrib package which can send notifications
        | when a pyATS job finishes execution. `pip install pyats.contrib` and
        | add the appropriate configuration or arguments to enable.
        .. code-block:: text

            pyats run job myjob.py --webex-token <WEBEX_BOT_TOKEN> --webex-email <MY_EMAIL>


Other Changes
^^^^^^^^^^^^^

Utils
  - Merged schemaengine functionality from metaparser
  - Added ListOf schema class

Reporter
  - Fixed issue with sending reporter messages >4GB

Cisco
  - Fix for `--tims-user` argument being ignored