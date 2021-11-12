.. _easypy_usage:

Using Easypy
============

Easypy comes with its own command line entrypoint: ``pyats run job``.
It is part of the overall :ref:`pyATS Command Line Interface<pyats_cli>`
that gets installed into your pyATS instance automatically.

.. note::

    prior to pyATS v5.1, the CLI command for Easypy was actually ``easypy``, and
    used single dash ``-`` arguments instead.

    Starting pyATS v5.1 forward, it has been replaced by ``pyats run job``
    command in favor of POSIX-style arguments. The old command is deprecated,
    but not removed for backwards compatbility purposes.

.. code-block:: bash

    # activate your pyats instance, eg:
    [tony@jarvis:~]$ cd /ws/tony-stark/pyats
    [tony@jarvis:pyats]$ source env.sh

    Activating the pyATS instance @ /ws/tony-stark/pyats
    --------------------------------------------------------------------
    PYTHONPATH=/ws/tony-stark/pyats:
    LD_LIBRARY_PATH=/usr/X11R6/lib
    --------------------------------------------------------------------

    # easypy is now part of your path
    (pyats) [tony@jarvis:pyats]$ which pyats
    /ws/tony-stark/pyats/bin/pyats

``pyats run job`` comes natively with built-in help information:

.. code-block:: text

    [tony@jarvis:~]$ pyats run job --help
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
      --clean-image-json          dictionary of clean images in JSON string (supports base64 encoded strings)

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


.. _easypy_arguments:

Standard Arguments
------------------

``pyats run job`` accepts a number of standard arguments that can be used to
influence and/or change jobfile execution behaviors. All arguments are
constructed and processed using python `argparse`_ module.  Please also see
:ref:`easypy_return_codes`.


.. _argparse: https://docs.python.org/3/library/argparse.html

.. csv-table:: Easypy Standard Arguments
    :header: Argument, Description
    :widths: 30, 70

    ``jobfile``, "positional argument, full path/name of :ref:`easypy_jobfile`
    to run."
    ``--configuration``, "configuration yaml file for plugins"
    ``--pyats-configuration``, "additional pyats configuration for execution"
    ``--job-uid``, "unique id from upper systems identifying this run"
    ``--testbed-file``, "full path/URL for YAML testbed file"
    ``--clean-file``, "file path/URL to file containing :ref:`clean_file` information"
    ``--clean-devices``, "a list of devices to :ref:`clean<kleenex_index>`"
    ``--clean-scope``, "whether to perform :ref:`clean/bringup<kleenex_index>` at job or task level"
    ``--invoke-clean``, ":ref:`Clean<kleenex_cleaners>` is only invoked when this parameter is specified."
    ``--clean-device-image``, "space separated images per device with format device:/path/to/image.bin"
    ``--clean-os-image``, "space separated images per OS with format os:/path/to/image.bin"
    ``--clean-group-image``, "space separated images per group with format group:/path/to/image.bin"
    ``--clean-platform-image``, "space separated images per platform with format platform:/path/to/image.bin"
    ``--clean-image-json``, "dictionary of clean images in JSON string. Can be base64 encoded."
    ``--submitter``, "specify a run submitter (defaults to current user)"
    ``--html-logs``, "enable generating HTML logs"
    ``--image``, "specify the current test image information"
    ``--release``, "specify the current release string information"
    ``--branch``, "specify the current branch information"
    ``--meta``, "A JSON dict of additional user information about this execution. Can be base64 encoded."
    ``--archive-name``, "specify a different name for the generated archive file."
    ``--no-archive``, "flag, disables the creation of a log archive"
    ``--no-archive-subdir``, "flag, disables the creation of date-specific archive subdirectory."
    ``--no-mail``, "flag, disables email notification at the end of run"
    ``--mailto``, "specify the list of email notification recipients."
    ``--mail-subject``, "email notification subject line."
    ``--mail-html``, "flag, enables HTML format email notification."
    ``--runinfo-dir``, "specify alternative runtime info directory location"
    ``--archive-dir``, "specify alternative archive storage directory location"
    ``--xunit``, "flag, enables x-unit style report generation"
    ``--verbose/--quiet``, "generate more or less log output"


.. important::

    ``jobfile`` is a positional argument, and must be provided first before
    all other arguments.

.. tip::

    ``pyats run job`` standardizes on `POSIX Style`_ CLI arguments.

.. _POSIX Style: https://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html


``-h, --help``
    Prints help information and how to use each arguments.

    .. code-block:: bash

        bash$ pyats run job --help

``jobfile``
    Mandatory positional argument. Specifies the full path/name to the
    :ref:`easypy_jobfile` to run.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py

``-C, --configuration``
    optional argument, used to provide the YAML plugin configuration file. Use
    this if you want to configure your Easypy to run certain plugins in custom
    orders for this particular run. Can be a file path or URL.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --configuration /path/to/config.yaml
        bash$ pyats run job /path/to/jobfile.py --configuration "http://<url>/config.yaml"

``--job-uid``
    optional argument. Allows upstream executor (eg, Jenkins) to pass down
    a unique identifier string to be stored in report.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --job-uid "this_is_an_example"

``--pyats-configuration``
    optional argument. Additional file to add to :ref:`pyats_configuration`.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --pyats-configuration /path/to/my/pyats.conf

``--testbed-file``
    Specifies the full path/name or URL of YAML topology 
    :ref:`topology_testbed_file` to be loaded as part of this run. When used, 
    Easypy automatically loads the testbed yaml file into a topology 
    :ref:`topology_objects`, and passes it to each task inside the jobfiles as 
    its ``testbed`` parameter. Refer to :ref:`easypy_testbed` for more details.

    Alternatively, you can specify a source to be loaded with the testbed
    creator package. To do so, append 'source:' in front of the desired loader
    name and specify any required arguments in CLI form. Refer to
    `pyats.contrib <https://github.com/CiscoTestAutomation/pyats.contrib>`_ for
    more details.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --testbed-file /path/to/mytestbed.yaml
        bash$ pyats run job /path/to/jobfile.py --testbed-file source:netbox
                                                --netbox-token=token
                                                --netbox-url=url
        bash$ pyats run job /path/to/jobfile.py --testbed-file "http://<url>/testbed.yaml"

``--clean-file``
    Full path or URL to the clean file. This enables testbed cleaning using
    the :ref:`kleenex<kleenex_index>` module.  This option is only useable if
    testbed information is provided using ``--testbed-file`` argument.

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/mytestbed.yaml\
                                       --clean-file /path/to/clean.yaml
                                       --invoke-clean
        bash$ pyats run job jobfile.py --testbed-file "http://<url>/testbed.yaml"\
                                       --clean-file "http://<url>/clean.yaml"
                                       --invoke-clean

``--clean-devices``
    Specifies the list of devices to :ref:`clean<kleenex_easypy_integration>`.
    If not specified, defaults to cleaning all devices specified in the clean
    file that are also present in the testbed file.

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --clean-devices device_a device_b device_c\
                                       --invoke-clean

    Groups of devices to be sequentially cleaned may be specified via
    nested list format.
    In the following example, device_a, device_b and device_c are
    cleaned in parallel, and only once complete are device_d and device_e
    cleaned in parallel.

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --clean-devices "[[device_a, device_b, device_c], [device_d, device_e]]"\
                                       --invoke-clean

.. _kleenex_cli_image_format:

``--clean-device-image``
    specifies images to be used for clean per device.

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --invoke-clean\
                                       --clean-device-image PE1:/path/to/clean_image.bin

    This is equivalent to the following in YAML

    .. code-block:: yaml

        devices:
          PE1:
            images:
            - /path/to/clean_image.bin

    To provide a list of images:

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --invoke-clean\
                                       --clean-device-image PE1:/path/to/controller_image.bin\
                                       PE1:/path/to/switch_image.bin

    This is equivalent to the following in YAML:

    .. code-block:: yaml

        devices:
          PE1:
            images:
            - /path/to/controller_image.bin
            - /path/to/switch_image.bin

    To provide images with a key structure:

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --invoke-clean\
                                       --clean-device-image PE1:image:/path/to/image.bin\
                                       PE1:packages:/path/to/optional_package1\
                                       PE1:packages:/path/to/optional_package2

    This is equivalent to the following in YAML:

    .. code-block:: yaml

        devices:
          PE1:
            images:
              image:
              - /path/to/image.bin
              packages:
              - /path/to/optional_package1
              - /path/to/optional_package2

    You may also specify an image which resides at a URL:

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --invoke-clean\
                                       --clean-device-image PE1:http://<url>/path/to/image.bin

    This is equivalent to the following in YAML:

    .. code-block:: yaml

        devices:
          PE1:
            images:
            - http://<url>/path/to/image.bin

    .. note::
        `--clean-device-image` can be used in combination with `--clean-os-image`,
        `--clean-group-image` and `--clean-platform-image`. Conflicts are resolved
        according to the following order: `device > group > platform > os`.

``--clean-os-image``
    specifies images to be used for clean per OS. Uses same format as `--clean-device-image`.

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --invoke-clean\
                                       --clean-os-image iosxe:/path/to/clean_image.bin

``--clean-group-image``
    specifies images to be used for clean per group. Uses same format as `--clean-device-image`.

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --invoke-clean\
                                       --clean-group-image group1:/path/to/clean_image.bin

``--clean-platform-image``
    specifies images to be used for clean per platform. Uses same format as `--clean-device-image`.

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --invoke-clean\
                                       --clean-platform-image n9k:/path/to/clean_image.bin

``--clean-image-json``
    JSON string with images for clean. The string can be base64 encoded. The two examples below are equivalent:

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --clean-image-json '{"os":{"iosxe":["test.bin"]}}'
        bash$ pyats run job /path/to/jobfile.py --clean-image-json eyJvcyI6eyJpb3N4ZSI6WyJ0ZXN0LmJpbiJdfX0=

    The schema for the JSON string is as follows:

    .. code-block:: json

        {
            "device": {
                "DEVICE_NAME": [
                    "URL_TO_IMAGE"
                ]
            },
            "os": {
                "OS_NAME": [
                    "URL_TO_IMAGE"
                ]
            },
            "group": {
                "GROUP_NAME": [
                    "URL_TO_IMAGE"
                ]
            },
            "platform": {
                "PLATFORM_NAME": [
                    "URL_TO_IMAGE"
                ]
            }
        }

    The clean image json will override any other image arguments as it will be applied after
    the standard arguments of device image, os image, group image and platform image.

    E.g. using the following argument combination:

    .. code-block:: bash

        --clean-device-image R1:test.bin --clean-image-json '{"os":{"iosxe":["test_new.bin"]}}'

    will use test_new.bin if the device `R1` is an IOSXE device.

``--clean-scope``
    specifies whether :ref:`clean<kleenex_easypy_integration>`
    is to be done at the :ref:`job<easypy_jobfile>` level
    or the :ref:`task<easypy_tasks>` level.
    If specified as "job", clean is done only once
    per job.
    If specified as "task", clean is done before each task
    starts.
    If not specified, defaults to "job".

    .. code-block:: bash

        bash$ pyats run job jobfile.py --testbed-file /path/to/my/testbed.yaml\
                                       --clean-file /path/to/my/clean.yaml\
                                       --clean-scope task
                                       --invoke-clean

``--invoke-clean``
    Clean is only invoked when this parameter is specified.

    .. note::

        Whether or not ``--invoke-clean`` is specified, :ref:`clean_file`
        content is still parsed and made available.


``-v, --verbose, -q, --quiet``
    Controls the logging level for Easypy. Use ``-v`` to increase and ``-q`` to
    decrease the verbosity of log output. Additive - use up to three to achieve
    more effect.

    .. code-block:: bash

        # quieter output
        bash$ pyats run job /path/to/jobfile.py -q

        # extre verbosity
        bash$ pyats run job /path/to/jobfile.py -vvv


``--submitter``
    Specifies an alternate userid to be displayed in the submitter field.
    (default: current user).

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --submitter chambers

``--html-logs``
    generates an HTML formatted, user-friendly log file ``TaskLog.html`` in
    addition to existing text-based log file. Optionally, provide the location
    where you want the HTML files to be generated to.

    .. code-block:: bash

        # use as a flag to generate HTML in the runtime archive
        bash$ pyats run job /path/to/jobfile.py --html-logs

        # use as an argument with directory where HTML logs should be put to
        bash$ pyats run job /path/to/jobfile.py --html-logs /path/to/directory/

    .. note::

        Experimental feature. Enabling this flag will double the size of your
        result archive due to log duplications.

``--image``/``--release``/``--branch``
    Specifies the image path/file and release/branch string information of used
    for result reporting purposes.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --image /path/to/image --release zn7

``--meta``
    User specified JSON dictionary of information to be added for reporting
    purposes. Can be a base64 encoded string of this JSON dictionary. The two
    examples below are equivalent:

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --meta "{\"key\":\"value\"}"
        bash$ pyats run job /path/to/jobfile.py --meta eyJrZXkiOiJ2YWx1ZSJ9

    URLs to JSON files, paths to JSON files, and individual key/value pairs can 
    also be supplied. These data sources can be freely combined and the `--meta` 
    argument can be used multiple times per command. Individual key/value pairs 
    must use an equals sign (`=`) to separate the key and the value. Being able 
    to combine different sources of information for the JSON meta dictionary 
    means that extra info can be added quickly and easily on a per-job basis. 
    See examples below:

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --meta https://<url>/jsonfile.json
        bash$ pyats run job /path/to/jobfile.py --meta /path/to/jsonfile.json
        bash$ pyats run job /path/to/jobfile.py --meta key=value
        bash$ pyats run job /path/to/jobfile.py --meta https://<url>/jsonfile.json --meta /path/to/jsonfile.json
        bash$ pyats run job /path/to/jobfile.py --meta key=value --meta another_key=another_value
        bash$ pyats run job /path/to/jobfile.py --meta /path/to/jsonfile.json --meta extra_key=value

``--archive-name``
    Specifies an alternative name for the archive file other than <jobuid>.zip.

``--no-archive``
    Flag. When used, disables the creation of archive zip file containing the
    current run information/logs, and preserves the job runinfo directory (as
    opposed to removing it after archive creation). Using this option also
    disables log uploading, as log uploading requires an archive zip file to be
    created and uploaded.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --no-archive

``--no-archive-subdir``
    Flag. Archive files are added to a subdirectory in the archive dir that
    specifies the month and day that the job was executed. When this flag is
    used, no such subdirectory is specified and archive files are added to the
    archive dir directly.

    .. code-block:: bash

        # Creates archive in <archive_dir>/ instead of <archive_dir>/<month>/
        bash$ pyats run job /path/to/jobfile.py --no-archive-subdir

``--no-mail``
    Flag, disables email notification at the end of execution.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --no-mail

``--mailto``
    Provides a list of recipients that receive email notification at the
    end of the run. Supports using either white-space, comma or semi-colon as
    the delimiter, and supports either user ids or full email addresses.
    (default: current user)

    .. code-block:: bash

        bash$ pyats run job jobfile.py --mailto "john, joe, jack@domain.com"

``--mail-subject``
    When specified, replaces the default email notification subject line.
    (default: ``pyATS Report - job: <name> by: <uid> - Total: # (P:#, PX:#,
    F:# ...)``)

    .. code-block:: bash

        bash$ pyats run job jobfile.py --mail-subject "legen -wait-for-it- dary. Legendary!"

``--mail-html``
    Flag, generates an html email notification report at the end of execution.
    You are able to attach custom report information in the html report, please
    refer to :ref:`easypy_report_customization`.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --mail-html

``--runinfo-dir``
    Specifies an alternative location for execution ``runinfo`` directory.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --runinfo-dir /my/runinfo/directory

``--archive-dir``
    Specifies an alternative location for storing archive zip files.

    .. code-block:: bash

        bash$ pyats run job /path/to/jobfile.py --archive-dir /my/archive/directory

``--xunit``
    Flag, enables the generation of an extra x-unit/j-unit result report XML.
    Can also be optionally used to provide the alternate location to generate
    xunit report to

    .. code-block:: bash

        # enable generation
        bash$ pyats run job /path/to/job/file.py --xunit

        # enable and also copy report to specified location
        bash$ pyats run job /path/to/job/file.py --xunit /path/to/dir


.. _easypy_argument_propagation:

Argument Propagation
--------------------

Easypy uses Python standard module argparse_ to parse command line arguments
stored in ``sys.argv``. In an effort to allow Easypy plugins to parse their own
arguments, and as well to allow users to provide custom arguments from the
command line and process them using their own parser code, a set of argument
propagation and processing rules were created:

- all arguments shall follow GNU POSIX CLI argument style

- parsers shall not feature positional arguments (except the Easypy ``jobfile``
  argument)

- parsers shall parse directly from ``sys.argv``

- parsers shall always leave ``sys.argv[0]`` untouched.

- parsers shall always use ``ArgumentParser.parse_known_args()`` to parse only
  their own arguments.

- all parsed/recognized arguments shall be removed from ``sys.argv``

- all other remaining/unknown arguments shall be placed back into ``sys.argv``

In other words, parsers only take what they know, and leave behind what
they don't know for the next parser to continue parsing. This allows parsing to
occur in sequential stages, wherever needed. The following is a list of typical
parser location/stages in Easypy environment, in their respective parsing order:

#. Easypy main program

#. Easypy plugins: core plugins first, then user's custom plugins.

#. User's jobfile

#. Test-harness ``aetest`` main program

#. User's script file

.. code-block:: python

    # Visualizing Argument Propagation
    # --------------------------------
    #
    #   assuming that easypy is invoked with the following arguments
    #   bash$ pyats run job jobfile.py --testbed-file tb.yaml \
    #                                  --no-archive --pdb --random --custom-arg "123"

    # breaking down the arguments into stages
    # ---------------------------------------
    #
    #   easypy arguments:       --no-archive             -> disable archive
    #
    #   plugin arguments:       --testbed-file tb.yaml   -> load testbed file
    #
    #   aetest arguments:       --pdb                    -> pdb on failure
    #                           --random                 -> randomize testcases
    #
    #   custom arguments:       --custom-args "123"      -> user custom


    # 0. at the first beginning
    # -------------------------
    sys.argv = ['pyats run job', '--testbed-file', 'tb.yaml',
                '--no-archive', '--pdb', '--random', '--custom-arg', '123']

    # 1. easypy argument parser
    # -------------------------
    # easypy takes away its known argument --no-archive
    #
    sys.argv = ['pyats run job', '--testbed-file', 'tb.yaml', '--pdb', '--random',
                '--custom-arg', '123']

    # 2. plugin argument parser
    # -------------------------
    # testbed plugin takes away its known argument --testbed-file
    #
    sys.argv = ['pyats run job', '--pdb', '--random', '--custom-arg', '123']

    # 3. jobfile custom argument parser
    # ---------------------------------
    # assume that the user wrote a custom parser in their jobfile, looking for
    # argument --custom-arg. While the jobfile is being run (before Tasks are)
    # started, this argument is also taken away
    #
    sys.argv = ['pyats run job', '--pdb', '--random']

    # 4. aetest argument parser
    # -------------------------
    # aetest finally takes away its known argument --pdb and --random
    #
    sys.argv = ['pyats run job']

This argument propagation scheme essentially allows users to provide any
additional custom arguments from the command line to be processed by the job
and/or script file, allowing for more dynamic & data-driven testing.

.. tip::

    because argument propagation only parses known arguments, any typos
    would be treated as an unknown argument and propagated further.

    *Steve Jobs once said, "you're holding it wrong"*.
