
Manifest Schema
===============

.. code-block:: yaml

    version: 1 # <integer> schema version for manifest
               # required

    type:  # type of script: easypy
           # required

    arguments:  # arguments for the script (optional)

        <key>: <value>

        key:
        - val1
        - val2

        "--key": value
        "-k": value

        <key>: "*N"

        <key>: true|false

        <key>: "True"

    description: |
        # This is the description for this script
        (optional)

    note: |
        # Note about this script, e.g. instructions or known issues
        (optional)

    tags:
    -  # string with tag keyword
    (optional)

    command:  # command to execute script, e.g. pyats run job
              # (optional)
              # by default, the command is inferred from the 'type'
              # e.g. easypy command: pyats run job

    # definition of runtimes for the related script
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
                <key>: <value>

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
                # (optional)

            arguments:   # arguments that override the global script arguments
                         # (optional)
                <key>: <value>
