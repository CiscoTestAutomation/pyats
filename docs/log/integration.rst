Integration with Easypy
=======================

Because of the specific ``log`` concept implementation, it is pretty much
automatically integrated with the execution environment (Easypy), where users 
should not need to concern themselves with the logging facility, and only focus
on standard usage. 

The following describes the points of automated integration with ``easypy``, 
``tcl`` and ``aetest`` in case you are interested.


Managed Handlers
----------------

Following the Python logger hierarchy, by default, all ``LogRecord`` objects
propagate to the ``root`` logger. This allows the simple concept of ``TaskLog``
to work: if we only configure the ``root`` logger with a ``TaskLogHandler``, 
then all log messages would be processed and stored to the given TaskLog file.

However, since each logger is able to have multiple handlers, there is a need
to track which handler is the current active TaskLog. Ergo the concept of
managed handlers:
    
    instead of creating new handler instances on the fly, a "globally" managed 
    instance of ``ScreenHandler`` and ``TaskLogHandler`` is automatically
    created and stored in the ``log`` module. 

.. code-block:: python
    
    # code snippet
    # ------------
    # 
    #   log/__init__.py

    # global managed handlers instances
    managed_handlers = {
                        'tasklog': TaskLogHandler(None),
                        'screen' : ScreenHandler(),
                        }

These managed handlers are intended to be attached to the ``root`` logger so 
that wherever within the code, we can always refer back to current TaskLog
handler. Consider this as the same concept as how ``logging`` always creates
the ``root`` logger as ``logging.root`` internally.


One TaskLog
-----------

In pyATS typical usage, there is only one TaskLog per process. This is achieved 
through the usage of managed handlers, tracking which handler instance is the 
current active TaskLog. It is required because of the following:

* TaskLogs needs to be closed after a test script finishes running in a job,
  and new TaskLog file need to be assigned to the next script

* Need to maintain the ability to change the current active TaskLog file with
  a simple API call.

Therefore for all practical purposes and usages, the ``managed_handlers`` should
be the only active instances of those handler classes when executing in pyATS.


.. note::

    the system is designed to be flexible. If you are familiar with how Python
    logging works and want to apply additional TaskLogs, filters, handlers 
    and more, it is absolutely possible to do so. It won't break the above
    conditions, except that pyATS is designed around the above: everything else
    is at your discretion/control, and you are responsible in configuring and
    tracking them.

.. _log_multiprocessing:

TaskLog & Multiprocessing
-------------------------

By default, Python ``logging`` module is not process-aware: users are expected
to modify/re-configure log handlers manually at the start of each process. In an
effort to make pyATS & the test ecosystem more user-friendly, this mundane work
is automatically handled by the infrastructure.

When running through :ref:`easypy`, ``TaskLogHandler`` is automatically attached
to ``root`` logger by the infrastructure to handle each testscript's TaskLog. In
addition, Easypy also auto-enables ``TaskLogHandler.enableForked()`` method to
make the handler process aware, so that all future forked child processes
automatically logs to new log files.

.. code-block:: python
    
    # Example
    # -------
    #
    #   demonstrating tasklog & multiprocessing

    import logging
    import multiprocessing

    from pyats import log

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # attach managed_handler to logger
    logger.addHandler(log.managed_handlers.tasklog)

    # change tasklog to a meaninful file & enable forking behavior
    log.managed_handlers.tasklog.changeFile('/tmp/logfile.txt')

    # now all log messages go into /tmp/logfile.txt
    logging.info('this is an informational message')

    # now let's define a function to be called in a child process
    # and print some log messages
    def func():
        logger.info('this is a message in child process')

    # turn on enableForked()
    log.managed_handlers.tasklog.enableForked()

    # call the function using multiprocessing fork
    multiprocessing.Process(target = func).start()

    # if you run the above code, here is the resulting logfiles & content:
    #
    # /tmp/logfile.txt
    # ----------------
    # 1: jarvis-lnx: 2015-09-13T22:39:06: %ROOT-6-INFO: %[pname=MainProcess][pid=9323][tid=MainThread]: this is an informational message
    # 2: jarvis-lnx: 2015-09-13T22:39:07: %LOG-6-INFO: %[pname=Process-1][pid=9324][tid=MainThread]: Forked process 9324 started, log: /tmp/logfile.txt:pid-9324
    #
    # /tmp/logfile.txt:pid-9324 
    # -------------------------
    # 3: jarvis-lnx: 2015-09-13T22:39:07: %ROOT-6-INFO: %[pname=Process-1][pid=9324][tid=MainThread]: this is a message in child process

Notice above that a new logfile was created by the child-process automatically
after forking, inheriting all of its parent's configuration and logging to a new
file with ``pid-<pid>`` post-fixed to the original logfile name. 

This beahvior can be disabled by calling ``disableForked()`` on the managed
``TaskLogHandler``.

Various Package Behaviors
-------------------------

EasyPy
    on startup, the managed handlers are added to the root logger as default
    handlers. If print-to-screen is disabled, then the screen handler is removed
    from the root logger (but not removed/closed from managed handlers dict).
    When a test script is run in the job file, a new TaskLog is created by using
    the managed tasklog handler's ``changeFile`` API.

AEtest
    when running in stand-alone mode, AEtest adds the managed screen handler to
    root logger in order to allow print-to-screen. Otherwise, AEtest does not
    touch logging configurations.

