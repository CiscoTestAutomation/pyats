September 2020
==============

September 30, 2020
------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``pyats.aetest``, v20.9.1
    ``pyats.kleenex``, v20.9.1
    ``pyats.results``, v20.9.1
    ``pyats.log``, v20.9.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.aetest pyats.kleenex pyats.results pyats.log

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.aetest ats.kleenex ats.results ats.log

Changes
^^^^^^^
  - Various fixes for liveview and import paths


September 29, 2020
------------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v20.9
    ``pyats.aereport``, v20.9
    ``pyats.aetest``, v20.9
    ``pyats.async``, v20.9
    ``pyats.cisco``, v20.9
    ``pyats.connections``, v20.9
    ``pyats.datastructures``, v20.9
    ``pyats.easypy``, v20.9
    ``pyats.kleenex``, v20.9
    ``pyats.log``, v20.9
    ``pyats.reporter``, v20.9
    ``pyats.results``, v20.9
    ``pyats.robot``, v20.9
    ``pyats.tcl``, v20.9
    ``pyats.topology``, v20.9
    ``pyats.utils``, v20.9

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

    * - Processor Parameters and Result APIs
      - :ref:`Docs <aetest_processors>`
      - | Processors now have :ref:`parameters <test_parameters>` which can be
        | passed by adding a correctly named argument to the processor.
        | Processors support :ref:`steps <aetest_steps>` by adding a `steps`
        | argument. Processors have their own result APIs, which can be accessed
        | from the `processor` argument.
        .. code-block:: python

            from pyats import aetest

            def my_processor(section, processor, testbed, steps, param_a):
                if not param_a:
                    processor.failed('param_a is False')

            class MyTestcase(aetest.Testcase):
                @aetest.processors.post(my_processor)
                @aetest.test
                def test_method(self):
                    self.parameters['param_a'] = False


Other Changes
^^^^^^^^^^^^^

Kleenex
  - Added `-archive_dir` argument in kleenex to generate zip archive file for
    clean results
  - Added the extended clean yaml to the log archive
  - Added the cli command 'pyats clean' which replaces `kleenex` cli command

Commands
  - Changed default behavior of `pyats secret encode` command.
    - New default is to input password by prompt
    - plaintext password can be still given via `--string` option

Aetest
  - Section uid chaining to accurately represent where each test occurs in the
    hierarchy with `uid.list`

Reporter/Easypy
  - Generate results file in JSON format instead of YAML format
  - Plugin summary in results file in addition to regular tests summary

