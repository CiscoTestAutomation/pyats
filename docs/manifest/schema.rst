
Manifest Schema
===============

.. code-block:: yaml

    version: 1 # <integer> schema version for manifest
               # required

    type:  # type of script: easypy
           # required

    arguments:  # arguments for the script (optional)

        # command line arguments may override the arguments provided here or in the profile

        <key>: <value>  # if the key does not start with "-", "--" will be prepended to the argument string, e.g. --key value

        # argparse 'nargs' using 'list'
        key:  # values may be specified as a list, this will translate to "--key val1 val2"
        - val1
        - val2

        "--key": value  # arguments can explicitly define dash syntax
        "-k": value

        <key>: "*N"  # if the value is "*N", repeat the argument N number of times

        <key>: true|false  # if the value is a boolean, leave out the value and only add the key to the argument string, e.g. --flag

        <key>: "True"  # if the boolean needs to be explicitly added to the argument as the value, explicitly specify a string


    # Note: Script file name is inferred from the manifest file name   file_name.tem -> file_name.py

    # description for the script related to this manifest
    description: |
        # This is the description for this script
        (optional)

    # Note about the script, e.g. instructions or known issues
    note: |
        # Note about this script
        (optional)

    # tags for searching
    tags:
    -  # string with tag keyword
    (optional)

    command:  # command to execute script, e.g. pyats run job
              # (optional)
              # by default, the command is inferred from the 'type'
              # e.g. easypy command: pyats run job

    # definition of runtime for the related script
    # (optional)
    runtimes:
        <name>:  # name of the runtime, e.g. venv

            type:  # supported types: virtualenv, system
                   # 'system' is the existing shell environment
                   # required

            source:  # list of environment files to source (optional)
            -  # path to file

            environment:  # dictionary of environment variables for the execution of the script
                          # (optional)
                key: value

            # list of files/paths that need to exist for succesfull execution (e.g. library files)
            # (optional)
            files:
                -  # path to file or directory

    # Profiles
    # (optional)
    profiles:

        <name>:  # name of the profile

            runtime:  # name of the runtime to use, if not specified, 'system' is assumed
                      # (optional)

            description: |
                # description of the profile

            arguments:   # arguments that override the global script arguments
                testbed-file: testbed.yaml
