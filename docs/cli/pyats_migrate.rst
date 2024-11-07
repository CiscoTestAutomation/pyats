pyats migrate
=============

Command to identify and inform a user of required upcoming changes to their
environment.

.. code-block:: text

    Usage:
      pyats migrate <subcommand> [options]

    Subcommands:
        abstract            Discover what changes must be made to existing test environments to conform
                            to the new token discovery.


pyats migrate abstract
---------------------

The mechanism for `Genie Abstract`_ and the organization of `Unicon Supported Platforms`_
are being updated for better consistency and utility. This subcommand will
examine your environment and inform you of any potential changes that may be
required. The usage of ``os``, ``model``, ``platform`` will be strictly defined within
Unicon in the `PID tokens`_ file and may require updates to testbeds and scripts to correctly reflect
these definitions.

.. _Genie Abstract: https://pubhub.devnetcloud.com/media/genie-docs/docs/abstract/index.html
.. _Unicon Supported Platforms: https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/supported_platforms.html
.. _PID tokens: https://github.com/CiscoTestAutomation/unicon.plugins/blob/master/src/unicon/plugins/pid_tokens.csv

.. code-block:: text

    Usage:
      pyats migrate abstract [options]

    Description:
      Discover what changes must be made to existing test environments to conform to the new token discovery.

    Abstract Options:
      path                  Path to start searching for files
      --init                Only process __init__.py files
      --python              Only process Python files
      --yaml                Only process YAML files
      --threads THREADS     Max number of threads to run while processing files (default 100)
