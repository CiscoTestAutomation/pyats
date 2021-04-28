Logging Concept
===============

Python's logging system is highly complex. For example:

* each module/package can have its own `Logger`_.

* each `Logger`_ could be equipped with multiple `Handler`_.

* each `Handler`_ could have its own `Formatter`_ and `Filter`_.

* log message propagate through its parent logger chain for processing.

To put it simply, Python logging is like rocket science, running pure steroids 
as fuel, with Tony Stark at the controls...

.. figure:: tonystark.jpg
    :align: center

.. tip::
    
    hence why it is highly beneficial for everyone to read & understand 
    ``logging`` fully.

In an effort to preserve this behavior, as well as minimizing usage complexity, 
pyATS logging was engineered to provide just enough for logs to be backwards 
compatible to existing tools & infrastructure (using CiscoLog format), offer the 
same ease of use, whilst maintaining the full flexibility and power of native
python ``logging``.


Behavior
--------

The overall pyATS logging behavior (applicable to the infrastructure, end-user
libraries and scripts) can be conceptually summarized as follows:

#. Logging is always done through using Python ``logging`` module.

#. `Logger`_ should always be named the same as the current module name (using
   magic variable ``__name__``), following the logger hierarchy.

   .. code-block:: python

    # Example
    # -------
    # 
    #   creating a logger object

    import logging

    logger = logging.getLogger(__name__)

#. ``log`` module features `Formatter`_ and `Handler`_ class that implements
   CiscoLog compatible log message format & storage behavior, and should be 
   used to configure Python ``logging``.

#. Under most circumstances, the pyATS test infrastructure configures logging
   for the user (in ``easypy`` and ``aetest``). However, when needed, the user
   scripts/modules/libraries is also able to configure their own logging 
   behavior/format (such as when used in another peer, non-pyATS infra)

#. Unless otherwise configured, there is only one active :ref:`tasklog` per 
   process where, by default, all log messages propagate to. If any additional
   handlers are processing log messages, the initiator is responsible for
   tracking/handling/closing them.

Adhering to this concept enables the following benefits:

* Logging hierarchy is preserved; ``root`` logger by default handles the logging 
  to :ref:`tasklog`.

* Scripts and libraries do not care about how log outputs are configured, and 
  their only requirement is to use Python ``logging`` module and its 
  functionalities.

* If needed, scripts can configure their own logging handlers and formatters for
  additional log files/output.

.. _Logger: https://docs.python.org/3.4/library/logging.html#logger-objects

.. _Formatter: https://docs.python.org/3.4/library/logging.html#formatter-objects

.. _Handler: https://docs.python.org/3.4/library/logging.html#handler-objects

.. _Filter: https://docs.python.org/3.4/library/logging.html#filter-objects

.. _tasklog:

TaskLog
-------

The log file storing script-run log messages in pyATS is called the *TaskLog*. 
This file is only generated when executing pyATS testscripts through ``easypy``, 
or when ``logging`` is manually configured to use :ref:`tasklog-handler`. 

The TaskLog file is no different than any other python ``logging`` log files in
the sense that it is also a text-based file, containing log messages. It is
referred to as the *TaskLog* for the sake of name reference consistency, and to 
highlight the fact that its log messages adhere to the :ref:`cisco-log-format`.


Logging Levels
--------------

Python ``logging`` natively offers 5 logging levels: 

    - critical

    - error

    - warning

    - info

    - debug

At any time, logging level can be set using ``setLevel`` API:

.. code-block:: python
    
    # Example
    # -------
    # 
    #   setting logger level
    #
    #   available levels:
    #       logging.INFO
    #       logging.CRITICAL
    #       logging.ERROR
    #       logging.WARNING
    #       logging.DEBUG

    import logging

    logger = logging.getLogger(__name__)

    logger.setLevel(logging.INFO)


When configuring your Python logger, use the actual Python levels and follow 
the Pythonic logging concept where if a level's numeric value is bigger than 
the current set level, then it would be displayed. This should be 
self-intuitive.


``Logging`` provides a set of convenience functions for simple logging usage. 
These are ``critical()``, ``error()``, ``warning()``, ``info()``, ``debug()``
and ``exception()``. To determine when and which logging level API to use, 
refer to the table below:

+-----------------------------------+------------------------------------------+
| Task you want to perform          | Suggested API                            |
+===================================+==========================================+
| Report event that occurred during | ``logger.info()`` or ``logger.debug()``  |
|                                   |                                          |
| normal operation of a program     | debug for very detailed output for       |
|                                   |                                          |
| (e.g. for status monitoring or    | diagnostic purposes                      |
|                                   |                                          |
| fault investigation)              |                                          |
+-----------------------------------+------------------------------------------+
| Issue a warning regarding a       | ``logger.warning()``                     |
|                                   |                                          |
| particular runtime event.         | - In library code if the issue is        |
|                                   |                                          |
| Script/program continues.         |   avoidable and the client application   |
|                                   |                                          |
|                                   |   should be modified to eliminate the    |
|                                   |                                          |
|                                   |   warning.                               |
|                                   |                                          |
|                                   | - If there is nothing the client         |
|                                   |                                          |
|                                   |   application can do the situation,      |
|                                   |                                          |
|                                   |   but the event should still be noted.   |
|                                   |                                          |
|                                   | - In user script, abnormal situation     |
|                                   |                                          |
|                                   |   happens, but don't want the script     |
|                                   |                                          |
|                                   |   to quit.                               |
+-----------------------------------+------------------------------------------+
| Report suppression of an error    | ``logger.error()``                       |
|                                   |                                          |
| particular runtime event          | do not raise an exception                |
+-----------------------------------+------------------------------------------+
| Report an error regarding a       | ``logger.critical()`` or                 |
|                                   |                                          |
| particular runtime even.          | ``logger.error()``                       |
|                                   |                                          |
| Raising an exception and          | Raise an exception                       |
|                                   |                                          |
| terminate the program.            |                                          |
+-----------------------------------+------------------------------------------+
| Report an error with exception    | ``logger.exception()``                   |
|                                   |                                          |
| information/stack added           | This can only be called from an exception|
|                                   |                                          |
| automatically to the messages     | handler.                                 |
+-----------------------------------+------------------------------------------+

For more information on Python ``logging``, refer to its documentation_ and 
tutorial_.

.. _documentation: https://docs.python.org/3.4/library/logging.html

.. _tutorial: https://docs.python.org/3.4/howto/logging.html#logging-basic-tutorial

