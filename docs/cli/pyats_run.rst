pyats run
=========

Execution command, offering subcommands that runs jobs and scripts defined in
pyATS.

.. code-block:: text

    Usage:
      pyats run <subcommand> [options]

    Subcommands:
       job                 runs the provided pyATS job file
       robot               runs the provided RobotFramework script

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels


pyats run job
-------------

This subcommand launches an :ref:`Easypy Job<easypy_jobfile>` for execution,
creating a standard Easypy runtime environment, running each tasks defined in
the job file, returing the overall results, and emailing you the report.

.. tip::

    ``pyats run job`` replaces the legacy ``easypy`` cli command with new POSIX
    style arguments.

.. code-block:: text

    Usage:
      pyats run job [file] [options]

    Example
    -------
      pyats run job /path/to/jobfile.py
      pyats run job /path/to/jobfile.py --testbed-file /path/to/testbed.yaml

    Description:
      Runs a pyATS job file with the provided arguments, generating & report result.

    Configuration:
      -C, --configuration FILE
                            easypy configuration yaml file for plugins

    Job Information:
      JOBFILE               target jobfile to be launched
      --job-uid             Unique ID identifiying this job run

    Mailing:
      --no-mail             disable report email notifications
      --mail-to             list of report email recipients
      --mail-subject        report email subject header
      --mail-html           enable html format report email

    Reporting:
      --submitter           Specify the current submitter user id
      --image               Specify the image under test
      --release             Specify the release being tested
      --xunit [DIR]         Generate xunit report in the provided location. If used as a flag, generates
                            xunit reports runtime directory

    HTML Logging:
      --html-logs [DIR]     Experimental feature. Directory to generates HTML logs in addition to any
                            existing log files. Note - will increase archive size due to log
                            duplication.

    TIMS:
      --tims-post           Enable posting results to tims
      --tims-user           TIMS user. If not specified, the userstarting the run is used
      --tims-dns            TIMS project dns name
      --tims-options        A string in the form of -key value sequence. (Add a space at the beginning
                            of the string to work around python parser bug. e.g. -a 1
      --tims-folder         A TIMS 3.x ID, a Logical ID or a complete, fully-qualified path
      --tims-custom-attrs   A str of dashed key/value pairs e.g. -key1 val1 -key2 val2. The key value
                            pairs are fed to TIMS as global custom attributes
      --tims-config-id      TIMS config_id, maps to Configuration ID, Related Config or logical
                            identifier

    Runinfo:
      --no-archive          disable archive creation
      --runinfo-dir         specify alternate runinfo directory
      --archive-dir         specify alternate archive directory
      --no-upload           Disable uploading archive to TRADe
      --bg-upload           Upload to TRADe in background

    Liveview:
      --liveview            Starts a liveview server in a separate process
      --liveview-host HOST  Specify host for liveview server. Default is localhost
      --liveview-port PORT  Specify port for liveview server. Default is 8080
      --liveview-keepalive  Keep log viewer server alive after the run finishes.
      
    Testbed:
      -t, --testbed-file    Specify testbed file location

    Clean:
      --clean-file FILE     Specify clean file location
      --clean-devices [ [ ...]]
                            Specify list of devices to clean, separated by spaces. To clean groups of
                            devices sequentially, specify as "[[dev1, dev2], dev3]".
      --clean-scope {job,task}
                            Specify whether clean runs before job or per task
      --invoke-clean        Clean is only invoked if this parameter is specified.

    Bringup:
      --logical-testbed-file
                            Specify logical testbed file location

    Rerun:
      --rerun-file FILE     rerun.results file that contains the information of tasks and testcases
      --rerun-condition  [ ...]
                            Results type list for the condition of rerun plugin.

    General Options:
      -h, --help            Show help information
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels

.. note::

    the arguments show in the ``pyats run job`` command may vary, depending on
    your current :ref:`plugin<easypy_plugin>` configuration.

For examples and the the list of all options standard to this command, see
:ref:`Easypy Usages<easypy_usage>`.


pyats run robot
---------------

    *Shortcut to running Robot scripts within Easypy environment*

Runs a provided RobotFramework script directly within a pyATS standard Easypy
runtime environment, operating as-if an :ref:`Easypy Job<easypy_jobfile>` was
provided.

This is identical to ``pyats run job`` in its behaviour - other than requiring
a Robot script instead of a job file to run. See :ref:`robot_easypy` for
details.

.. code-block:: text

    Usage:
      pyats run robot [file] [options]

    Example
    -------
      pyats run robot /path/to/my_robot_script.robot
      pyats run robot /path/to/my_robot_script.robot --testbed-file /path/to/testbed.yaml

    Description:
      Runs a RobotFramework script with the provided arguments, generating & report
      result.

    Configuration:
      -C, --configuration FILE
                            easypy configuration yaml file for plugins

    Robot Script Info:
      FILE                  target RobotFramework script to be run
      --job-uid             Unique ID identifiying this job run

    Mailing:
      --no-mail             disable report email notifications
      --mail-to             list of report email recipients
      --mail-subject        report email subject header
      --mail-html           enable html format report email

    Reporting:
      --submitter           Specify the current submitter user id
      --image               Specify the image under test
      --release             Specify the release being tested
      --xunit [DIR]         Generate xunit report in the provided location. If used as a flag, generates
                            xunit reports runtime directory

    HTML Logging:
      --html-logs [DIR]     Experimental feature. Directory to generates HTML logs in addition to any
                            existing log files. Note - will increase archive size due to log
                            duplication.

    TIMS:
      --tims-post           Enable posting results to tims
      --tims-user           TIMS user. If not specified, the userstarting the run is used
      --tims-dns            TIMS project dns name
      --tims-options        A string in the form of -key value sequence. (Add a space at the beginning
                            of the string to work around python parser bug. e.g. -a 1
      --tims-folder         A TIMS 3.x ID, a Logical ID or a complete, fully-qualified path
      --tims-custom-attrs   A str of dashed key/value pairs e.g. -key1 val1 -key2 val2. The key value
                            pairs are fed to TIMS as global custom attributes
      --tims-config-id      TIMS config_id, maps to Configuration ID, Related Config or logical
                            identifier

    Runinfo:
      --no-archive          disable archive creation
      --runinfo-dir         specify alternate runinfo directory
      --archive-dir         specify alternate archive directory
      --no-upload           Disable uploading archive to TRADe
      --bg-upload           Upload to TRADe in background

    Liveview:
      --liveview            Starts a liveview server in a separate process
      --liveview-host HOST  Specify host for liveview server. Default is localhost
      --liveview-port PORT  Specify port for liveview server. Default is 8080
  
    Testbed:
      -t, --testbed-file    Specify testbed file location

    Clean:
      --clean-file FILE     Specify clean file location
      --clean-devices [ [ ...]]
                            Specify list of devices to clean, separated by spaces. To clean groups of
                            devices sequentially, specify as "[[dev1, dev2], dev3]".
      --clean-scope {job,task}
                            Specify whether clean runs before job or per task
      --invoke-clean        Clean is only invoked if this parameter is specified.

    Bringup:
      --logical-testbed-file
                            Specify logical testbed file location

    Rerun:
      --rerun-file FILE     rerun.results file that contains the information of tasks and testcases
      --rerun-condition  [ ...]
                            Results type list for the condition of rerun plugin.

    General Options:
      -h, --help            Show help information
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels
