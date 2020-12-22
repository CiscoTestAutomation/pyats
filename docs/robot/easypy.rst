.. _robot_easypy:

Easypy Integration
==================

The use of this package enables users to integrate any RobotFramework script
(eg, files ending with ``.robot``) into :ref:`Easypy Runtime<easypy>`, where
Robot testcase results aggregates together into the final report the user
receives.

``run_robot`` API
-----------------

The ``run_robot`` API launches an :ref:`Easypy Task<easypy_tasks>` process,
running the provided RobotFramework script. It automatically convert and adapt
Robot outputs, logs, results etc into your Easypy runtime directory and report.

.. code-block:: python

    # Example
    # -------
    #
    #   job file running a robot script

    import os

    # import the run_robot api
    from pyats.robot.runner import run_robot

    # entry point
    def main(runtime):

        # run your robot script
        run_robot(robotscript = os.path.join('path', 'to', 'my_robo_script.robot'),
                  runtime = runtime)

and this job file can then be launched with:

.. code-block:: bash

    bash$ pyats run robot_job.py --testbed-file /path/to/tb.yaml

.. csv-table:: run_robot() Function Arguments
  :header: "Argument", "Description"

  ``robotscript``, "RobotFramework script to be run in this task"
  ``taskid``, "unique task id (defaults to ``Task-#`` where # is an
  incrementing number)"
  ``max_runtime``, "maximum tax runtime in seconds before termination"
  ``runtime``, "easypy runtime object"
  ``**options``, "any other RobotFramework options_ to be passed to Robot engine"

.. _options: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#all-command-line-options

.. note::

    The option for variables is passed as a list of formatted strings which
    reflects how they are specified on the command line.

    .. code-block:: python

        run_robot(..., variable = ['var1:value1',
                                   'var2:value2',
                                   ...])

Testbed File
^^^^^^^^^^^^

To facilitate the sharing of one testbed between each Tasks launched in Easypy,
when a testbed file is provided (eg, using ``--testbed-file`` argument to
``pyats run job``), the argument value (eg, path to file) is saved to
environment variable ``TESTBED``.

This facilitates the access of testbed files within RobotFramework scripts. Eg:

.. code-block:: robotframework

    *** Settings ***
    # load pyATS framework
    Library        ats.robot.pyATSRobot

    *** Variables ***
    # set testbed to use from env variable TESTBED
    ${testbed}     %{TESTBED}


Behaviours
^^^^^^^^^^

- each RobotFramework script run in Easypy should be called via an instance of
  ``run_robot()`` api

- the job file will wait for each Robot script to continue before proceeding to
  to the next line (eg, sequential execution)

- each test in Robot maps to a testcase in pyATS

- each keyword line in Robot maps to a test section in pyATS

- the name of the Robot file, minus the ``.robot`` postfix, is used as a the
  suite name

- all log outputs are written to TaskLog

- each Robot script gets its own output folder within Easypy runinfo directory


Example
^^^^^^^

Running the following ``hello_world.robot`` script in Easypy:

.. code-block:: robotframework

    *** Settings ***
    Library         hello_world.py

    *** Test Cases ***
    Should Pass
        Hello World

    Should Fail
        Raise Exception

    Logging Test
        Do Logging

    Check Testbed Provided
        Check Testbed

Easypy Output:

.. code-block:: text

    +------------------------------------------------------------------------------+
    |                             Task Result Summary                              |
    +------------------------------------------------------------------------------+
    Task-1: hello_world.Should Pass                                           PASSED
    Task-1: hello_world.Should Fail                                           FAILED
    Task-1: hello_world.Logging Test                                          PASSED
    Task-1: hello_world.Check Testbed Provided                                FAILED

    +------------------------------------------------------------------------------+
    |                             Task Result Details                              |
    +------------------------------------------------------------------------------+
    Task-1: hello_world
    |-- Should Pass                                                           PASSED
    |   `-- 1_Hello World                                                     PASSED
    |-- Should Fail                                                           FAILED
    |   `-- 1_Raise Exception                                                 FAILED
    |-- Logging Test                                                          PASSED
    |   `-- 1_Do Logging                                                      PASSED
    `-- Check Testbed Provided                                                FAILED
        `-- 1_Check Testbed                                                   FAILED


``pyats run robot`` CLI
-----------------------

In addition to being able to run RobotFramework scripts directly within your job
file, the ``pyats run robot`` command line also enables you to quickly run a
Robot script in an Easypy environment (eg, with generated archive and report),
without having to explicitly create a job file.

.. code-block:: bash

    # Example
    # -------
    #
    #   running a robot file directly in Easypy environment

    bash$ pyats run robot /path/to/my_robot_script.robot --testbed-file /path/to/tb.yaml

The arguments to ``pyats run robot`` is no different than that of typical
:ref:`Easypy Uage<easypy_usage>`, except that instead of an Easypy job file,
you are providing a RobotFramework script directly.

The command line code will automatically generate the required jobfile from a
template, copy it to your runtime directory, and run as if you provided that job
file instead.

All other behaviours are exactly the same as if using an explicit job file with
``run_robot()`` api.

.. note::

    Consider this as a *shortcut* way of running a RobotFramework script - it
    works only for a single file. For multiple files consolidated into the same
    job, you should still create your own job file.
