Behavior & Flow
===============

This section covers native runtime behaviors of Easypy using ``pyats run job``:
the behavior and/or objects available while Easypy is running :ref:`easypy_jobfile`.

.. _easypy_return_codes:

Easypy Return Codes
-------------------

``pyats run job`` exits with Linux exit code ``0`` (Success) if all the
following conditions are met:

.. csv-table:: Easypy Successful Return Conditions
    :header: Condition, Description
    :widths: 20, 80

    "Some tests were ran", "At least one test script/testcase was run and reported"
    "Test results are available", "No exception seen while trying to access test results."
    "success rate is 100%", "Total # of tests with ``Passed``, ``Passx`` or ``Skipped`` results / total # of tests."
    "All pre-job plugins ran ok", "No exception seen in any pre-job plugin."
    "All pre-task plugins ran ok", "No exception seen in any pre-task plugin for all scripts in the jobfile."
    "All post-task plugins ran ok", "No exception seen in any post-task plugin for all scripts in the jobfile."
    "All post-job plugins ran ok", "No exception seen in any post-job plugin."


Otherwise, the following codes will be used:

.. csv-table:: Easypy Return Codes
    :header: Code, Description
    :widths: 10, 90

    ``1``, "Non-100% testcase success rate"
    ``2``, "Incorrect command-line arguments"
    ``3``, "Some errors/exceptions are seen while running plugins"
    ``4``, "All other exceptions unhandled by the infrastructure (unknown)"

Return codes give test runners such as Jenkins one way of determining if the
``pyats run job`` run was successful.

.. note::

    When a testscript fails to run, the success rate of the job is multiplied by
    the percentage of testscripts that successfully executed. This prevents the
    case where the success rate is 100% despite a testscript failing to run.

.. _easypy_graceful_termination:

Graceful Termination
--------------------

Easypy has the built-in capability to gracefully handle the exit signal ``SIGINT``
(``Ctrl-C``) from the user and its runtime Linux environment. Keep in mind that
Linux signals always propagate to the entire process group - and all processes
spawned by Easypy belong to the same process group.

    - When the first ``SIGINT`` is received, all child processes should begin
      aborting the current execution (quick-exit).

    - The main Easypy process continues to wait for all child processes and
      :ref:`easypy_tasks` to wrap-up execution. The email report, archive,
      upload logs etc still occur after everything finalizes.

    - If a second ``SIGINT`` is received, the main Easypy process is quickly
      aborted & crashed out. No subsequent handling of exceptions & erroneous
      states are processed. No email report, archive etc are performed.


.. _easypy_runtime:

runtime
-------

When a job is running, the runtime object allows users to query to current
Easypy states, objects and input argument information. To read and refer to
``runtime`` attributes, define your job file's main function with the special
runtime argument:

.. code-block:: python

    # Example
    # -------
    #
    #   querying runtime information inside jobfile

    from pyats import easypy

    # use special argument runtime in main() argument list
    # the engine automatically passes in the runtime object
    def main(runtime)

        # pass in runtime directory as an argument to testscript
        run('script.py', directory = runtime.directory)

The following attributes are currently accessible through ``runtime``:

``runtime.env``
    attribute dictionary of runtime environment information.

    .. code-block:: text

        # Runtime Environment Attributes
        # ------------------------------

        env.argv.all              command line arguments easypy was called with
        env.argv.custom           all user arguments not recognized by easypy
        env.prefix                pyATS virtual environment root path
        env.python.tag            python tag, eg, cpython-34
        env.python.name           python name, eg, cpython
        env.python.version        python version, eg, 3.4.1
        env.python.architecture   python build architecture, eg, 32bit/64bit
        env.env.user              user id (whoami)
        env.host.name             exec server hostname
        env.host.distro           exec server's Linux distribution
        env.host.kernel           exec server's Linux kernel version string
        env.host.architecture     exec server's system architecture

``runtime.directory``
    Location of :ref:`easypy_runinfo` directory.

``runtime.archive``
    Location of the archive zip file. Note that this is a "target" location.
    The actual zip file is not created until the jobfile finishes execution.
    Set to ``None`` when ``--no-archive`` option is used.

``runtime.testbed``
    current topology :ref:`topology_objects`, loaded through ``--testbed-file``
    argument.
    If no testbed file was provided, the testbed object is set to `None`.

``runtime.synchro``
    a built-in default multiprocessing Manager_ instance. This is used to
    synchronize data between various Easypy subprocesses, and allows users to
    leverage and create datastructures that can be shared between their job
    and script files.

``runtime.mail_report``
    proposed jobfile report ``TextEmailReport`` object instance. Refer to
    :ref:`easypy_email_notification` documentation for details.

``runtime.job.name``
    name of the current running jobfile.

``runtime.job.file``
    full path/name of the current running jobfile.

``runtime.job.uid``
    this job's unique string identifier, format: ``<name>.<'%Y%b%d_%H:%M:%S'``.

``runtime.job.image``, ``runtime.job.release``
    image name and release string information associated with this job run.
    By default, these values are provided by ``--image`` and ``--release``
    command line arguments.

.. warning::

    ``runtime`` shall be used solely as a **read-only** source of Easypy
    state information. Unless otherwise advised in this documentation, any and
    all write-access & monkey-patching of ``runtime`` objects and attributes is
    **strictly forbidden**. Doing so will void your warranty and support
    contracts.

.. _Manager: https://docs.python.org/3.4/library/multiprocessing.html#managers

.. _easypy_testbed:

testbed
-------

When a :ref:`Task<easypy_tasks>` executes a testscript, a ``testbed`` parameter is
always provided by default.

    *Testing is always done on a testbed.*

The provided ``testbed`` parameter value is the corresponding
:ref:`topology_objects` instance, loaded from ``--testbed-file``.
If a testbed file is not provided, the value is ``None``, and is nevertheless
still provided to the testscript for consistency, indicating that
"no testbed was provided".

This behavior can be overridden if ``testbed`` argument was explicitly provided
to ``run()`` method or ``Task()`` class constructor.

.. code-block:: python

    # Example
    # -------
    #
    #   a jobfile that runs a script on 3 separate testbeds in parallel
    #   (cannot be done with --testbed-file argument)

    from pyats.easypy import run

    # import topology module
    from pyats import topology

    # manually load your testbed files
    testbed_1 = topology.loader.load('/path/to/testbed_1.yaml')
    testbed_2 = topology.loader.load('/path/to/testbed_2.yaml')
    testbed_3 = topology.loader.load('/path/to/testbed_3.yaml')

    def main(runtime):

        # create the tasks and manually provide a testbed to run on.
        tasks_1 = Task(testscript = '/path/to/my/testscript.py',
                       runtime = runtime,
                       testbed = testbed_1)
        tasks_2 = Task(testscript = '/path/to/my/testscript.py',
                       runtime = runtime,
                       testbed = testbed_2)
        tasks_3 = Task(testscript = '/path/to/my/testscript.py',
                       runtime = runtime,
                       testbed = testbed_3)

        # now start all tasks in parallel
        task_1.start()
        task_2.start()
        task_3.start()


        # wait for all tasks to finish
        task_1.wait()
        task_2.wait()
        task_3.wait()

.. warning::

    the example above is intended to demonstrate the ability to provide custom
    and/or override the ``testbed`` parameter inside a job file.


Directories
-----------

By default, Easypy always creates a ``users/`` directory under the current
virtual environment. Each user of this pyATS instance gets their own ``<user>``
folder, where their :ref:`easypy_runinfo` and :ref:`easypy_archive` is located.

.. code-block:: text

    # Easypy Users Directory Strcture
    # -------------------------------

    <pyats_root>
    |
    |-- users
    .   |-- <userid>
        .   |-- runinfo              -> runtime/runinfo folder
            |-- archive              -> past run log archives
            |-- jobs                 -> user specific job file storage
            `-- etc                  -> anything else


``users/`` folder is always created with ``0o777`` permission in order to allow
sharing of a single pyATS instance by multiple users. Each user's own directory
is created with ``0o755`` to avoid other users from accidentally writing to it.

.. _easypy_runinfo:

runinfo
"""""""

During Easypy execution, ``runinfo`` folder contains all the logs, files &
etc generated by the running jobfile and tasks. Each job is assigned its own
unique ``runinfo`` directory, based on its name and the time of launch.

.. code-block:: text

    # Typical runinfo Structure
    # -------------------------
    #
    #   assuming the current job name is "example_job" and is running

    runinfo
    |-- example_job                           -> symlink to job runinfo
    |-- example_job.2015Sept14_10:05:13       -> job runinfo directory
    .   |-- JobLog.example_job                -> easypy jobfile log
        |-- TaskLog.Task-1                    -> Task-1 Tasklog & forked
        |-- TaskLog.Task-1:pid-31526             child process logs
        |-- TaskLog.Task-1:pid-31535
        |-- TaskLog.Task-1:pid-31536
        |-- taskresults                       -> folder holding current task
        |   |-- Task-1.common_setup.Passed      results as blank files, used
        |   |-- Task-1.testcase_1.Passed        for quickly identifing current
        |   `-- Task-1.testcase_2.Failed        testscript progress/results.
        |-- cleanresults                      -> folder holding current clean
        |   |-- Task-1.device_1.Passed          results as blank files, used
        |   |-- Task-1.device_2.Failed          for quickly identifing current
        |   `-- Task-1.device_3.Passed          clean progress/results.
        |-- reporter.log                      -> Reporter server log
        |-- env.txt                           -> environment debug information
        `-- example_job.py                    -> copy of the running jobfile

As the unique ``runinfo`` directory of each job run is quite tedious to type,
a symlink is provided using only the job name. This allows quick reference and
access of ``runinfo`` directory for debugging purposes. This symlink only exists
during runtime, and is removed after. Note that it should not be used as
a reliable method for automation purposes: in case two jobs of the same name
are running simultaneously, only one of them gets the symlink, depending on
whichever one ran last.

If a filename to be written to taskresults is too long, it is truncated and rather
than being blank, the resulting file is made to contain the original filename and
test result for tracking purposes.

.. _easypy_archive:

archive
"""""""

By default, at the end of Easypy execution, the contents of ``runinfo`` is
archived into a zip file, and the jobfile ``runinfo`` directory is deleted. This
behavior can be averted by using ``--no-archive`` option.

Archives are stored under each user's ``./users/<userid>/archive/YY-MM/``
directory, where ``YY-MM`` represents the current year and month in double
digits, providing some level of division/classification between jobs.


Files
-----

The following is a list of typical files generated by Easypy job runs, and their
corresponding descriptions:

<job-name>.py
    copy of the jobfile that ran.

<job-name>.report
    copy of the email notification sent to the submitter

TaskLog.<task-id>
    TaskLog: one per jobfile task, where all messages generated in a task is
    stored.

JobLog.<job-name>
    overall ``pyats.easypy`` module log

testbed.static.yaml
    Contents of the ``--testbed-file``, if specified by the user.

testbed.clean.yaml
    Contents of the ``--clean_file``, if specified by the user.

env.txt
    A dump of environment variables and cli args of this Easypy run

reporter.log
    Reporter server log file, contains a trace of XML-RPC call sequences.

results.json
    JSON result summary file generated by Reporter.

xunit.xml,
    files containing xUnit-style result reports and information required by
    Jenkins. These files are only generated if ``--xunit`` argument is provided
    to Easypy.

ResultsSummary.xml
    XML result summary file generated by Reporter

ResultsDetails.xml
    XML result details file generated by Reporter

CleanResultsDetails.yaml
    YAML clean result details file generated by Kleenex

Kleenex.<device-name>.log
    Job-scope clean details for this device.

Kleenex_<task-id>.<device-name>.log
    Task-scope clean details for this device.
