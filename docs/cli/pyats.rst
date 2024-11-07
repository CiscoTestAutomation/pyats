pyats
=====

Top-level command-line entry point for pyATS. All other functions
are loaded as subcommands of this command.


Synopsis
--------

.. code-block:: bash

    Usage:
      pyats <command> [options]

    Commands:
        clean               runs the provided clean file
        create              create scripts and libraries from template
        diff                Command to diff two snapshots saved to file or directory
        learn               Command to learn device features and save to file
        logs                command enabling log archive viewing in local browser
        migrate             utilities for migrating to future versions of pyATS
        parse               Command to parse show commands
        run                 runs the provided script and output corresponding results.
        secret              utilities for working with secret strings.
        shell               enter Python shell, loading a pyATS testbed file and/or pickled data
        validate            utilities that help to validate input files
        version             commands related to version display and manipulation

    General Options:
      -h, --help            Show help

    Run 'pyats <command> --help' for more information on a command.


.. tip::

    the number of subcommands homed under top-level ``pyats`` command may vary
    depending on your pyATS version, packages installed, and other variables.

Common Options
--------------

Optional arguments built into the core ``pyats`` command, that can be added to
any level/subcommands.

``-h``, ``--help``
    display help for the given command and/or subcommand

``-v``, ``--verbose``
    increase the verbosity of display output

``-q``, ``--quiet``
    decrease the verbosity of displayed output
