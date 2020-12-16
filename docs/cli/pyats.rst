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
        validate            utlities that helps to validate input files
        version             display currently installed pyATS version

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
