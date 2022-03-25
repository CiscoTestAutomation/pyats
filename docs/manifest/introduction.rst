Introduction
============

The pyATS Manifest is a file with YAML syntax describing how and where to execute a script.
It is intended to formally describe the execution of a single script, the runtime environment,
script arguments and profile which includes the test topology and related parameters.

A script can be executed via the manifest using the `pyats run manifest` command. Manifest
files use the file extension ``.tem`` which stands for Test Execution Manifest.

Command line execution examples:

.. code-block:: shell

    $ pyats run manifest job.tem
    $ pyats run manifest job.tem --profile sanity

Command line manifest validation:

.. code-block:: shell

    $ pyats validate manifest job.tem

The manifest defines the script execution arguments, runtime environment and the profile(s)
that define environment specific settings and arguments. Profiles allow the same script
to be run against multiple environments or run with different input parameters, e.g.
local testbed, orchestrated testbed, production environment, different scaling numbers,
or purposes like regression runs. Each profile can have its own specific script arguments
and runtime specific settings.

.. warning::

    Passing the job filename as an argument is not supported. See note below.

.. note::

    The associated script file that the manifest refers to is inferred based on the
    manifest filename with the extension `.py`. E.g. the script filename for a manifest
    with filename of ``job.tem`` is ``job.py`` in the same directory as the manifest file.



Script types
~~~~~~~~~~~~

The manifest defines a ``type`` for the script that is associated with
the manifest. Currently, the supported types for the manifest are:

    * easypy

Only suported script types have an execution runtime that allows
the manifest to execute the script.


Script arguments
~~~~~~~~~~~~~~~~

One of the primary definitions in the manifest is the ``arguments`` key in the manifest.

The arguments are defined as a set of key value pairs to be used as execution options.
These arguments are translated to shell command arguments for script execution.

Arguments defined for the script can be superseded by arguments defined in a profile.
Any arguments specified on the command line will override arguments defined in the profile.

Arguments are transformed into a command line argument string by combining the script arguments,
profile arguments and command line arguments and translating those using below rules.

The transformation of arguments is done in steps:

    * Arguments are translated from command line, manifest script arguments and profile arguments
      into internal argument structures
    * Internal argument structures are combined using the priority: command line > profile > script.
    * Internal argument structure is translated to the command line argument string

The internal argument structure is translated to the command line argument string using the following rules:

    * Arguments that do not start with `-` are assumed to be double dash arguments and `--` will
      be prepended to the key in the command line argument string.
    * Arguments may explicitly define dash syntax, e.g `"-key": value`
    * Argument values are quoted using double quotes, e.g. `val1` will translate to `"val1"`
    * Arguments specified as a list will translate to `--key "val1" "val2"`
    * If the value is `*N`, repeat the argument key N number of times
    * If the value is a boolean, leave out the value and only add
      the key to the argument string, e.g. `flag: True` translates to `--flag`.
    * If the boolean needs to be explicitly added to the argument string, the value
      must be explicitly specified as a string, e.g. `key: "True"`

For example, the script arguments defined in the manifest could look like this:

.. code-block:: yaml

    arguments:
        mail-html: True
        configuration: easypy_config.yaml

    profile:
        local:
            arguments:
                testbed-file: testbed.yaml

The arguments will be combined from the profile arguments and script arguments and translated
to command arguments for execution. Adding command line arguments will add or override
these.

For example running the manifest execution with the above arguments and adding the
`testbed-file` argument on the command line will override the profile argument.

.. code-block:: shell

    $ pyats validate manifest job.tem --profile local --testbed-file testbed2.yaml


runtimes
~~~~~~~~

The manifest can define zero or more runtime environments that can be used to execute the script.
Runtimes are defined as named entries under the ``runtimes`` key in the manifest.

A runtime environment is used to execute the script and provides the shell environment and related
libraries to be able to execute the script. If no runtime environment is defined, it is assumed
the script is intended to run in the 'current' system environment.

The supported runtime types are:

    * system
    * virtualenv


profiles
~~~~~~~~

The manifest can define zero or more profiles that contain environment specific settings and arguments.
Profiles are defined as named entries under the ``profiles`` key in the manifest.

The arguments defined in the profile override the arguments specified for the script. Profiles specify
a runtime to be used to execute the script and any additional settings relevant for that specific
environment and runtime combination.


Examples
========

Minimal manifest to run a easypy job script using the 'system' runtime.

.. code:: yaml

    version: 1

    type: easypy

    arguments:
        configuration: easypy_config.yaml
        mail-html: True


Manifest with runtime and profile.

.. code:: yaml

    version: 1

    type: easypy

    runtimes:
        venv:
            type: virtualenv
            source:
                - /var/pyenv/venv/bin/activate
            environment:
                PYTHONPATH: /var/pyenv/libs
                TEST: "%ENV{VARNAME}"

    arguments:
        configuration: easypy_config.yaml
        mail-html: True
        devices:
        - rtr1
        - rtr2

    profiles:
        local:
            description: |
                Local run using virtual environment, send plain text email
            runtime: venv
            arguments:
                mail-html: False
                testbed-file: testbed.yaml
