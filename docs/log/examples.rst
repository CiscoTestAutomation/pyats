Examples
========

The following provides some examples on how to do logging in your code.


Typical Usage
-------------

In typical test script and libraries, use ``logging`` directly and create your
loggers using your ``__name__`` module name as the logger name. Log messages 
would naturally just propagate to the pyATS configured ``root`` logger.

.. code-block:: python

    # typical test script
    # -------------------
    #
    #   assuming that you are running in an EasyPy environment where
    #   root handlers are configured

    import logging

    # create a logger for this module
    logger = logging.getLogger(__name__)

    # informational messages
    logger.info('info messages')

    # critical messages
    logger.critical('critical messages')

    # debug messages
    logger.debug('debug messages')

    # warning messages
    logger.warning('warning messages')

    # error messages
    logger.error('error messages')

    try:
        # i am raising an error here so the except statement catches it
        raise Exception('just raising for demo purposes')
    except:
        # exception automatically included in error message
        logger.exception('caught error above')


Advanced Usage
--------------

This is only needed if your code has a need to manipulate the current TaskLog
log file and/or managed handlers. Most users would not need to know this.

.. code-block:: python

    # controlling tasklog
    # -------------------
    #
    #   assuming that you are running in an EasyPy environment where
    #   root handlers are configured

    import logging
    from pyats.log import managed_handers

    # create a logger for this module
    logger = logging.getLogger(__name__)

    # now your log calls should work
    logger.info('info messages')
    logger.critical('critical messages')
    logger.debug('debug messages')
    logger.warning('warning messages')
    logger.error('error messages')

    # to change the current TaskLog file:
    managed_handlers['tasklog'].changeFile('/path/to/new/logfile.txt')
    
    # new log messages go to new file
    logger.info('new info messages')
    logger.critical('new critical messages')
    logger.debug('new debug messages')
    logger.warning('new warning messages')
    logger.error('new error messages')

    # removing handlers from root
    logging.root.removeHandler(managed_handlers['tasklog'])
    logging.root.removeHandler(managed_handlers['screen'])

    # adding handlers back to root
    logging.root.addHandler(managed_handlers['tasklog'])
    logging.root.addHandler(managed_handlers['screen'])


Configuring Your Own
--------------------

Here we'll cover how to configure ``logging`` from scratch, in case your script
is being run standalone in a foreign environment, or you are simply using the
``log`` package in your environment. 

.. code-block:: python
    
    # configuring your own logging using log handlers
    # -----------------------------------------------

    import logging

    from pyats.log import ScreenHandler, TaskLogHandler

    # create a logger
    logger = logging.getLogger(__name__)

    # creating a handler
    screen_handler = ScreenHandler()
    tasklog_handler = TaskLogHandler('/path/to/logfile.txt')

    # attach to your logger
    logger.addHandler(screen_handler)
    logger.addHandler(tasklog_handler)

    # set log level to show everything
    logger.setLevel(logging.DEBUG)


    # configuring your own logging using just the formatters
    # ------------------------------------------------------

    import sys
    import logging

    from pyats.log import ScreenFormatter, TaskLogFormatter

    # create a logger
    logger = logging.getLogger(__name__)

    # creating handlers using logging standard handlers
    screen_handler = logging.StreamHandler(stream = sys.stdout)
    tasklog_handler = logging.FileHandler('/path/to/logfile.txt')

    # set handler to use ats format and screen format
    screen_handler.setFormatter(ScreenFormatter())
    tasklog_handler.setFormatter(TaskLogFormatter())

    # attach to your logger
    logger.addHandler(screen_handler)
    logger.addHandler(tasklog_handler)

    # set log level to show everything
    logger.setLevel(logging.DEBUG)

    # voila!
