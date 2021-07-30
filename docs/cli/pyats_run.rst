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
      --pyats-configuration
                            pyats configuration override file

    Mailing:
      --no-mail             disable report email notifications
      --mail-to             list of report email recipients
      --mail-subject        report email subject header
      --mail-html           enable html format report email

    Reporting:
      --submitter           Specify the current submitter user id
      --image               Specify the image under test
      --release             Specify the release being tested
      --branch              Specify the branch being tested
      --meta                Specify some meta information as a dict (supports base64 encoded strings)
      --no-xml-report       Disable generation of the XML Report

    Runinfo:
      --no-archive          disable archive creation
      --no-archive-subdir   disable archive subdirectory creation
      --runinfo-dir         specify alternate runinfo directory
      --archive-dir         specify alternate archive directory
      --archive-name        specify alternate archive file name

    Liveview:
      --liveview            Starts a liveview server in a separate process
      --liveview-host HOST  Specify host for liveview server. Default is localhost
      --liveview-port PORT  Specify port for liveview server.
      --liveview-hostname HOSTNAME
                            Displayed hostname for liveview.
      --liveview-displayed-url LIVEVIEW_DISPLAYED_URL
                            Displayed url for liveview, for example, http://<liveview_hostname>:<port>
      --liveview-keepalive  Keep log viewer server alive after the run finishes.
      --liveview-callback-url LIVEVIEW_CALLBACK_URL
                            Specify xpresso callback url for jenkins run.
      --liveview-callback-token LIVEVIEW_CALLBACK_TOKEN
                            Specify xpresso token for jenkins run.

    Testbed:
      -t, --testbed-file    Specify testbed file location

    Clean:
      --clean-file FILE [FILE ...]
                            Specify clean file location(s). Multiple clean files can be specified by
                            separating them with spaces.
      --clean-devices [ [ ...]]
                            Specify list of devices to clean, separated by spaces. To clean groups of
                            devices sequentially, specify as "[[dev1, dev2], dev3]".
      --clean-scope {job,task}
                            Specify whether clean runs before job or per task
      --invoke-clean        Clean is only invoked if this parameter is specified.
      --clean-device-image        space separated images per device with format device:/path/to/image.bin
      --clean-os-image            space separated images per OS with format os:/path/to/image.bin
      --clean-group-image         space separated images per group with format group:/path/to/image.bin
      --clean-platform-image      space separated images per platform with format platform:/path/to/image.bin

    Bringup:
      --logical-testbed-file
                            Specify logical testbed file location

    Rerun:
      --rerun-file FILE     rerun.results file that contains the information of tasks and testcases
      --rerun-task  [ ...]  TASKID TESTSCRIPT [TESTCASES...] Details to identify a specific Task to
                            rerun. Can be used multiple times for multiple tasks.
      --rerun-condition  [ ...]
                            Results type list for the condition of rerun plugin.

    xUnit:
      --xunit [DIR]         Generate xunit report in the provided location. If used as a flag, generates
                            xunit reports runtime directory

    HTML Logging:
      --html-logs [DIR]     Directory to generate HTML logs in addition to any existing log files. Note
                            - will increase archive size due to log duplication.

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
      --branch              Specify the branch being tested
      --meta                Specify some meta information as a dict (supports base64 encoded strings)
      --no-xml-report       Disable generation of the XML Report

    Runinfo:
      --no-archive          disable archive creation
      --no-archive-subdir   disable archive subdirectory creation
      --runinfo-dir         specify alternate runinfo directory
      --archive-dir         specify alternate archive directory
      --archive-name        specify alternate archive file name

    Liveview:
      --liveview            Starts a liveview server in a separate process
      --liveview-host HOST  Specify host for liveview server. Default is localhost
      --liveview-port PORT  Specify port for liveview server.
      --liveview-hostname HOSTNAME
                            Displayed hostname for liveview.
      --liveview-displayed-url LIVEVIEW_DISPLAYED_URL
                            Displayed url for liveview, for example, http://<liveview_hostname>:<port>
      --liveview-keepalive  Keep log viewer server alive after the run finishes.
      --liveview-callback-url LIVEVIEW_CALLBACK_URL
                            Specify xpresso callback url for jenkins run.
      --liveview-callback-token LIVEVIEW_CALLBACK_TOKEN
                            Specify xpresso token for jenkins run.

    Testbed:
      -t, --testbed-file    Specify testbed file location

    Clean:
      --clean-file FILE [FILE ...]
                            Specify clean file location(s). Multiple clean files can be specified by
                            separating them with spaces.
      --clean-devices [ [ ...]]
                            Specify list of devices to clean, separated by spaces. To clean groups of
                            devices sequentially, specify as "[[dev1, dev2], dev3]".
      --clean-scope {job,task}
                            Specify whether clean runs before job or per task
      --invoke-clean        Clean is only invoked if this parameter is specified.
      --clean-device-image        space separated images per device with format device:/path/to/image.bin
      --clean-os-image            space separated images per OS with format os:/path/to/image.bin
      --clean-group-image         space separated images per group with format group:/path/to/image.bin
      --clean-platform-image      space separated images per platform with format platform:/path/to/image.bin

    Bringup:
      --logical-testbed-file
                            Specify logical testbed file location

    Rerun:
      --rerun-file FILE     rerun.results file that contains the information of tasks and testcases
      --rerun-task  [ ...]  TASKID TESTSCRIPT [TESTCASES...] Details to identify a specific Task to
                            rerun. Can be used multiple times for multiple tasks.
      --rerun-condition  [ ...]
                            Results type list for the condition of rerun plugin.

    xUnit:
      --xunit [DIR]         Generate xunit report in the provided location. If used as a flag, generates
                            xunit reports runtime directory

    HTML Logging:
      --html-logs [DIR]     Directory to generate HTML logs in addition to any existing log files. Note
                            - will increase archive size due to log duplication.

    General Options:
      -h, --help            Show help information
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels



pyats run manifest
------------------

This subcommand uses the :ref:`Manifest<manifest>` for job execution. The filename specified
must the a ``.tem`` file with YAML syntax according to the :ref:`manifest_schema`.

.. code-block:: text

    Usage:
      pyats run manifest [options]

    Example
    -------
      pyats run manifest <filename>
      pyats run manifest <filename> --profile s2c
      pyats run manifest <filename> --profile local

    Description:
      Runs a test script by discovering the execution parameters and target environment from the manifest file.

    Manifest Options:
      FILENAME              manifest filename
      --profile PROFILE     execution profile
