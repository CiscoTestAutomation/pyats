Introduction
------------

The pyATS Manifest is a file with YAML syntax describing how and where to execute a script.
It is intended to formally describe the execution of a single script, the runtime environment,
script arguments and profile which includes the test topology and related parameters.

A script can be executed via the manifest using the `pyats run manifest` command. Manifest
files typically use the file extension ``.tem`` which stands for Test Execution Manifest.

Command line execution examples:

.. code-block:: shell

    $ pyats run manifest job.tem
    $ pyats run manifest job.tem --profile sanity

Command line manifest validation:

.. code-block:: shell

    $ pyats validate manifest job.tem

The manifest defines the script execution arguments, runtime environment and the profile(s)
to define environment specific settings and arguments. The profiles are intended to allow
the same script to be run against mulitple environments, e.g. local testbed, orchestrated
testbed or production environment. Each profile can have its own specific script arguments
and runtime specific settings.

Script arguments
~~~~~~~~~~~~~~~~

One of the primary definitions in the manifest is the ``arguments`` key in the manifest.

The arguments are defined as a set of key value pairs to be used as execution options.
These arguments are translated to shell command arguments for script execution.

Arguments defined for the script can be superseded by arguments defined in a profile.
Any arguments specified on the command line will override arguments defined in the profile.

The priority of arguments is: command line > profile > script.

For example, the script arguments defined in the manifest could look like this:

.. code-block:: yaml

    arguments:
        mail-html: True
        configuration: easypy_config.yaml

    profile:
        local:
            arguments:
                testbed-file: testbed.yaml

The arguments will be combined from the profile and top level arguments key and translated
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

