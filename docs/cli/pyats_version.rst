pyats version
=============

Command with subcommands that displays and manipulates the currently installed
pyATS and sub-package versions.

.. code-block:: text

  Usage:
    pyats version <subcommand> [options]

  Subcommands:
      check               display currently installed pyATS version
      update              update current pyATS installation to another version

  General Options:
    -h, --help            Show help
    -v, --verbose         Give more output, additive up to 3 times.
    -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                          and CRITICAL logging levels

pyats version check
-------------------

This subcommand displays the currently installed pyATS version (within this
virtual environment), and gives you the ability to check whether there are
any available package updates.

Options
^^^^^^^

``--outdated``
    checks PyPI for any available package upgrades, and displays the appropriate
    upgrade api.

    .. note::

        this requires connecting to PyPI server and getting package metadata,
        a somewhat slow process. Be patient while it computes.

``--include [...]``
    list of other packages to display/check for in the displayed version table.
    Useful if you want to check for possible upgrades for some of your other
    installed packages.


Example
^^^^^^^

.. code-block:: text

    # Example
    # -------
    #
    #   check for outdated package versions, including genie

    bash$ pyats version check --outdated
    You are currently running pyATS version: 19.12

    Checking for outdated packages...

      Package                      Version Latest
      ---------------------------- ------- ------
      pyats                        19.12   20.1
      pyats.aereport               19.12   20.1
      pyats.aetest                 19.12   20.1
      pyats.async                  19.12   20.1
      pyats.connections            19.12   20.1
      pyats.datastructures         19.12   20.1
      pyats.easypy                 19.12   20.1
      pyats.examples               19.12   20.1
      pyats.kleenex                19.12   20.1
      pyats.log                    19.12   20.1
      pyats.results                19.12   20.1
      pyats.robot                  19.12   20.1
      pyats.tcl                    19.12   20.1
      pyats.templates              19.12   20.1
      pyats.topology               19.12   20.1
      pyats.utils                  19.12   20.1
      genie                        19.12   20.1
      genie.abstract               19.12   20.1
      genie.conf                   19.12   20.1
      genie.examples               19.12   20.1
      genie.harness                19.12   20.1
      genie.libs.conf              19.12   20.1
      genie.libs.filetransferutils 19.12   20.1
      genie.libs.ops               19.12   20.1
      genie.libs.parser            19.12   20.1
      genie.libs.robot             19.12   20.1
      genie.libs.sdk               19.12   20.1
      genie.libs.telemetry         19.12   20.1
      genie.metaparser             19.12   20.1
      genie.ops                    19.12   20.1
      genie.parsergen              19.12   20.1
      genie.predcore               19.12   20.1
      genie.telemetry              19.12   20.1
      genie.utils                  19.12   20.1

    Note - you can upgrade outdated packages with:
        pip install --upgrade pyats.easypy pyats.kleenex pyats.utils
        pip install --upgrade genie.conf genie.examples genie.harness
        pip install --upgrade genie.libs.parser genie.libs.telemetry genie.ops
        pip install --upgrade genie.parsergen genie.predcore genie.telemetry
        pip install --upgrade genie.utils


pyats version update
--------------------

This subcommand performs a one-click update of all your pyATS and its dependency
packages. The intent is to simplify common upgrade/downgrade process, eliminate
the need to fiddle with `pip` command, and maintain a seamless user experience
through packaging refactor/changes.

It performs the following actions in sequence:

1. check whether your environment has package mismatches

2. removes all current pyATS packages

3. installs the newly specified versions.

Options
^^^^^^^

``version``
    update your pyATS packages to this version. If not provided, defaults to
    current latest version

``--yes``
    skip the prompt that confirms wehether you want to do the environment
    update, and auto-providing consent.


.. tip::

    this command is perfect for restoring an out-of-shape, out-of-date and/or
    corrupted environment back in order.
