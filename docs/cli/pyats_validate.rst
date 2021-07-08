pyats validate
==============

Helper command, offering subcommands that focuses on validating various pyATS
related input files, formats, and content.

.. code-block:: text

    Usage:
      pyats validate <subcommand> [options]

    Subcommands:
        datafile            validate your YAML-based datafile syntax
        testbed             validate your testbed file yaml syntax

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels


pyats validate testbed
----------------------

This subcommand validates the content of your :ref:`topology_testbed_file`. It
gives developers an opportunity to check if the file is written following 
valid YAML syntax, and adheres to the :ref:`schema`. 

.. code-block:: text

    Usage:
      pyats validate testbed [file] [options]

    Description:
      Validates the provided testbed YAML file for syntax and content completeness.

    Testbed Options:
      [file]                Testbed YAML file to validate
      --connect             Test each device's connections
      --no-lint             Do not lint the testbed YAML file


Options
^^^^^^^

``[file]``
    the input testbed yaml file. Can be a file path or a URL to a YAML file

``--connect``
    best-effort attempt to connect to each testbed device using
    ``device.connect()``. Consider this as a rudimentary method of ensuring
    your devices's connection block is well defined/formed.

``--no-lint``
    skips the linting of your testbed YAML file for syntax errors and warnings.

Example
^^^^^^^


.. code-block:: text

    # Example
    # -------
    #
    #   validating a testbed input file

    bash$ pyats validate testbed N7K-EZ-HW-7-SSR.yaml
    Loading testbed file: N7K-EZ-HW-7-SSR.yaml
    --------------------------------------------------------------------------------

    Testbed Name:
        N7K-EZ-HW-7-SSR

    Testbed Devices:
    .
    |-- P1 [router/nxos]
    |   `-- Ethernet3/9 ----------> link-1
    `-- PE1 [router/nxos]
        `-- Ethernet3/9 ----------> link-1

    Warning Messages
    ----------------
     - Device 'P1' missing 'platform' definition
     - Device 'PE1' missing 'platform' definition



pyats validate datafile
-----------------------

This subcommand validates the content any pyATS YAML datafile, including 
:ref:`aetest_datafile`. It understands the various YAML datafile syntaxes 
introduced as part of pyATS's extended YAML loader, and gives developers an 
opportunity to check:

1. what the expanded data looks like
2. if correct YAML syntax is followed

Returns the loaded, validated datafile, with ``extends:`` block expanded.

.. code-block:: text

    Usage:
      pyats validate datafile [file] [options]

    Description:
      Validates the provided YAML datafile for syntax and content completeness.

      Note:
        This command also understands the pyATS datafile 'extends:' syntax, and
        returns the complete, full data content with extensions fulfilled.

    Datafile Options:
      [file]                Datafile to validate
      --schema              Schema to validate datafile structure
      --json                Output in JSON format
      --no-lint             Do not lint the YAML datafile

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels

Options
^^^^^^^

``[file]``
    the input datafile. Can be a file path or a URL to a YAML file

``--schema``
    Python module.object to the schema to validate the provided datafile against

``--json``
    return output in JSON format instead of YAML. 
    (cannot be used when ``--schema`` is provided)

``--no-lint``
    skips the linting of your datafile file for syntax errors and warnings.

Example
^^^^^^^

.. code-block:: text

    # Example
    # -------
    #
    #   validating an AEtest datafile

    bash$ pyats validate datafile $VIRTUAL_ENV/examples/comprehensive/data/base_datafile.yaml
    Loading datafile: examples/comprehensive/data/base_datafile.yaml
    --------------------------------------------------------------------------------
    parameters:
      parameter_A: datafile value A
      parameter_B: datafile value B
    testcases:
      ExampleTestcase:
        uid: ExampleTestcaseDatafileID
        description: 'block of text describing what this testcase does

          '
        groups:
        - group_A
        - group_B
        - group_C
        - group_D
        parameters:
          local_A: datafile value A
          local_B: datafile value B
        data_A: attribute data A
        data_B: attribute data B
      LoopedTestcase:
        groups: []
      TestcaseWithSteps:
        uid: TestcaseWithStepsDatafileID


    YAML Lint Messages
    ------------------
      5:75      error    trailing spaces  (trailing-spaces)
      19:42     error    trailing spaces  (trailing-spaces)
      53:1      error    trailing spaces  (trailing-spaces)
      72:41     error    no new line character at the end of file  (new-line-at-end-of-file)


.. code-block:: text

    # Example
    # -------
    #
    #   validating an AEtest datafile against schema
    #   (eg, datafile schema is available as:
    #    from pyats.aetest.datafile.schema import datafile_schema)

    bash$ pyats validate datafile examples/comprehensive/data/base_datafile.yaml --schema pyats.aetest.datafile.schema.datafile_schema
    Loading datafile: examples/comprehensive/data/base_datafile.yaml
    --------------------------------------------------------------------------------
    {'parameters': {'parameter_A': 'datafile value A',
                    'parameter_B': 'datafile value B'},
    'testcases': {'ExampleTestcase': {'data_A': 'attribute data A',
                                      'data_B': 'attribute data B',
                                      'description': 'block of text describing '
                                                      'what this testcase does\n',
                                      'groups': ['group_A',
                                                  'group_B',
                                                  'group_C',
                                                  'group_D'],
                                      'parameters': {'local_A': 'datafile value A',
                                                      'local_B': 'datafile value '
                                                                'B'},
                                      'uid': 'ExampleTestcaseDatafileID'},
                  'LoopedTestcase': {'groups': []},
                  'TestcaseWithSteps': {'uid': 'TestcaseWithStepsDatafileID'}}}

    YAML Lint Messages
    ------------------
      5:75      error    trailing spaces  (trailing-spaces)
      19:42     error    trailing spaces  (trailing-spaces)
      53:1      error    trailing spaces  (trailing-spaces)
      72:41     error    no new line character at the end of file  (new-line-at-end-of-file)


.. tip::

    use ``-q`` to quiet pretty information such as "----" sections and headers.