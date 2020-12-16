Implementation
==============


As previously established, ``log`` itself does not configure ``logging``. It
only offers the formatters & handlers necessary to adhere to CiscoLog standard.

Handlers
    Handlers handle each LogRecord_ by sending them to the appropriate
    destination. In pyATS ``log``, there are two common destinations for
    most users: the shell screen, and a runtime log (TaskLog). These two
    destinations are handled by two different handler classes.

Formatters
    Formatters are responsible for converting a LogRecord_ to a properly
    formatted string that can be interpreted by human or an external system,
    which, in pyATS, is either screen, or to log file. ``log`` module
    features two formatters.

.. _LogRecord: https://docs.python.org/3.4/library/logging.html#logging.LogRecord

ScreenHandler
-------------

Enables print-to-screen functionality for log messages. Outputs to STDOUT by
default, and when attached to a logger, prints log messages to screen. This
handler automatically sets ScreenFormatter_ as its formatter.

.. code-block:: python

    # Example
    # -------
    #
    #   attaching ScreenHandler to root logger, enabling all log messages to be
    #   printed to screen

    import sys
    import logging
    from pyats.log import ScreenHandler

    # get the root logger
    logger = logging.getLogger(__name__)

    # create handler (defaults to STDOUT)
    handler = ScreenHandler()
    # or, if you want to output to STDERR, use below instead
    handler = ScreenHandler(sys.stderr)

    # add handler to logger
    logger.addHandler(handler)

    # now try logging :)
    logger.critical('a critical message')

    # disable coloured output
    # (default to enabled)
    handler.coloured = False

.. _tasklog-handler:

TaskLogHandler
--------------

Enables saving log messages in standard CiscoLog format to log files. Also has
an API enabling easy changing of current active log file to a different file.
Automatically uses TaskLogFormatter_ as its formatter.

.. code-block:: python

    # Example
    # -------
    #
    #   attaching TaskLogHandler to root logger, enabling all log messages to be
    #   logged to a particular file, and then changing the file to log to

    import logging
    from pyats.log import TaskLogHandler

    # get the root logger
    logger = logging.getLogger(__name__)

    # create handler (with full path to log file)
    handler = TaskLogHandler('/path/to/my/TaskLog-A.log')

    # add handler to logger
    logger.addHandler(handler)

    # set logging level a bit lower to enable INFO
    logger.setLevel(logging.INFO)

    # now try logging
    logger.info('an info message')

    # get current log directory and file
    logdir = handler.logdir
    logfile = handler.logfile

    # change log file to a different file
    handler.changeFile('/path/to/my/TaskLog-B.log')

    # log again, it appears in second file
    logger.info('another info message')

    # enable/disable on-fork create new logfile
    # (this behavior is inherited in child processes)
    handler.enableForked()
    handler.disableForked()

    # enable coloured output
    # (default to disabled - enabling will cause ANSI colour codes to appear
    #  in your task log, which the log viewer may not support)
    handler.coloured = True

``TaskLogHandler`` file/folder handling behavior is described by the following:

* if no logfile is provided (eg, ``''`` or ``None``), log stream is set to
  ``/dev/null`` in order to keep stream functionality consistent.

* if full logfile path is provided, the current log directory is set to the
  directory where the log file is.

* if absolute file path is not provided on the creation of TaskLogHandler, the
  current working directory is used as log file directory.

* if absolute file path is not provided when calling ``changeFile`` method, the
  current known log directory is used.

* if ``enableForked()`` is called, ``TasklogHandler`` becomes process aware:
  when python ``multiprocessing`` is called to fork a new child processes, the
  child process's TaskLog is automatically redirected to a new file, and
  the parent TaskLog contains a message/link to the new child log.

.. code-block:: python

    # Example
    # -------
    #
    #   TaskLogHandler behavior example.
    #   no logger is used in this example. only showing how the handler works.

    from pyats.log import TaskLogHandler

    # create handler (with full path to log file)
    handler = TaskLogHandler('/path/to/my/logdir/TaskLog-A.log')

    # now the logging active directory is "/path/to/my/logdir/"
    # let's change the tasklog file:
    handler.changeFile('TaskLog-B.log')
    # following logging behavior, TaskLog-B.log is created under
    # "/path/to/my/logdir/TaskLog-B.log"

    # but if we provide an absolute path
    handler.changeFile('/path/to/newdir/TaskLog-C.log')
    # logging directory changes to "/path/to/newdir/

    # to use present-working-directory, create handler with logfile as None
    handler = TaskLogHandler(None)
    # note that if you only change current logfile to None, the last logdir
    # does not change


.. note::

    ``changeFile`` method is a method of the handler class, and not a
    functionality of logger class. Thus in order to change the output file for a
    TaskLogHandler, you need to beware of which handler you want to use and
    track it (eg, store the variable somewhere).


.. _ScreenFormatter:

ScreenFormatter
---------------

Formats log messages to be printed to screen. Screen formatter formats messages
by adding a basic time stamp and the module name from where the message came
from. Note that this is not the standard CiscoLog format.

Usually this class does not need to be used by the end user: it is automatically
used when using ScreenHandler_.

.. code-block:: text

    Format
    ------

    %(asctime)s: %%%(appname)s-%(msgname)s: %(message)s

    where:
        acstime     time when the log message was created
        appname     name of module where log message was called
        msgname     text logging level for the message (eg, INFO/DEBUG/WARNING)
        messages    the log message itself

    Example Message
    ---------------

    2014-12-02T10:10:45: %root-INFO: this is an informational message
    2014-12-02T10:11:00: %root-WARNING: this is a warning message


.. _TaskLogFormatter:

TaskLogFormatter
----------------

Formats log messages to standard CiscoLog format, ready to be saved to log
files, hence the name "TaskLog Formatter".

Usually this class does not need to be used by the end user: it is automatically
used when using TaskLogHandler_.

.. code-block:: text

    # the format itself, in Python logging formatter style
    # ----------------------------------------------------

    {seqnum}: {hostname}: {time}: %{appname}-{severity}-{msgname}: {tags}: {message}%

    seqnum      - message sequence number, starts with 1
    hostname    - current host name
    time        - timestamp in yyyy-mm-ddThh:mm:ss format
    appname     - name of module where log message was called
    severity    - message severity, range 1-7
    msgname     - text logging level for the message (eg, INFO/DEBUG/WARNING)
    tags        - optional tags associated with this message
    message     - message given by the user

    # default tags included per message
    # ---------------------------------
    pname       - process name
    pid         - process id
    part        - log message part number, if the message is multi-part/line

    # Example
    # -------

    70: my-server: 2014-08-06T11:21:30: %AETEST-6-INFO: %[pname=python][pid=11295][tid=MainThread]: a log message
    71: my-server: 2014-08-06T11:21:30: %AETEST-6-INFO: %[pname=python][pid=11295][tid=MainThread]: another log message


CiscoLogRecord
--------------

Extends basic ``logging.LogRecord`` class and adds support for more default
values such as ``seqnum``, ``hostname``, and ``tags``, and is backwards
compatible.

When either ``TaskLogFormatter`` or ``ScreenFormatter`` is enabled on a handler,
this class replaces the default ``logging.LogRecord`` factory class through
``logging.setLogRecordFactory`` api call.
