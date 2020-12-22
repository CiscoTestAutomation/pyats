pyats create
============

Create command, offering subcommands that allows you to craft using templates.

.. note::

  this commands requires optional dependencies. To install
  these optional dependency, do: ``pip install pyats[template]``.

.. code-block:: text

    Usage:
      pyats create <subcommand> [options]

    Description:
      Creates script and library components using cookiecutter templates.

      All subcommands equires the following dependencies to be installed:
          pip install pyats[template]

    Subcommands:
        project             create a new pyATS project from template

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels


pyats create project
--------------------

The command assists in the creation of new pyATS scripts from template:

- creates a new folder for your project

- create the basic project job file and script file

- creates testcases using the names you provide

All you have to do from there is to initialize the new folder into a git 
repository using ``git init``, and focus on your test automation content.

This subcommand uses cookiecutter to generate a new pyATS project/script.
The code for the cookiecutter used can be found at: https://github.com/CiscoTestAutomation/pyATS-project-template

.. code-block:: text

    Usage:
      pyats create project [options]

    Description:
      create a pyATS script from cookiecutter template, located at:
          https://github.com/CiscoTestAutomation/pyATS-project-template

    Project Options:
      --name                name of new pyATS project
      --testcases [ [ ...]]
                            names of testcases to be generated
      --datafile            flag to indicate usage of datafiles
      --no-datafile         disable the usage of datafiles

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels

By default, the command will prompt you for information it needs to generate
the project from template. These prompts can be automated if you provide the
corresponding command line arguments.

Example
^^^^^^^

.. code-block:: text

    # Example
    # -------
    #
    #   creating a pyats project by entering everything through the prompts

    bash$ pyats create project
    Project Name: test_project
    Testcase names [enter to finish]:
      1. testcase_one
      2. testcase_two
      3.
    Will you be using testcase datafiles [Y/n]: y
    Generating your project...

    # this will create a new folder with your provided project name, containing
    # the template files

    bash $ tree test_project/
    test_project/
    |--  test_project.py
    |--  test_project_data.yaml
    `--  test_project_job.py


.. code-block:: text

    # Example
    # -------
    #
    #   creating a pyats project by adding some options and arguments in the command line and the rest through prompts
    #   notes:
    #   - the arguments that were specified through the CLI command will not be prompted
    #   - the arguments that were not specified through the CLI command will be prompted
    #   - the order of the arguments does not matter

    bash$ pyats create project --project_name my-project --testbed_name my-testbed
    Checking if cookiecutter is installed...
    include_datafile: yes
    datafile_name: my-datafile
    number_of_test_cases: 2
    Generating your project...
    my-project has been generated in your current directory
