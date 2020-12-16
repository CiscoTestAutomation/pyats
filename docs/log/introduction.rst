Introduction
============

A log is a log regardless of what kind of prefixes each log message contains and
what format it ended up as, as long as it is human readable and provides useful
information to the user. 

Python ``logging`` module's native ability to handle and process log messages is
more than sufficient for any logging needs, and has always been suggested as the
de-facto logging module to use. 
    
Therefore, for all intends and purposes, users of pyATS infrastructure should
always use just the native Python ``logging`` module as-is in their scripts and 
testcases.

.. code-block:: python

    # Example
    # -------
    #
    #   import the logging module at the top of your script
    #   setup the logger

    import logging

    # always use your module name as the logger name.
    # this enables logger hierarchy
    logger = logging.getLogger(__name__)

    # use logger:
    logger.info('an info message')
    logger.error('an error message')
    logger.debug('a debug message')

Users are expected to have a good understanding of how Python logging works. 
Documentation for Python ``logging`` module can be found at:

* https://docs.python.org/3.6/howto/logging.html#logging-advanced-tutorial

.. important::

    do not attempt to read and understand the rest of the logging documentation
    without first reading and learning how python logging works.


Delving Deeper
--------------

Why should everyone use the Python ``logging`` module as is? Simple: it is 
highly configurable. Behind the scenes, pyATS infrastructure configures the 
logging behavior for the end-user, so that all scripts & libraries output
logs in the exact same format: :ref:`cisco-log-format`.

The remainder of this logging documention digs deeper into the details of how
and where pyATS uses and configures python ``logging``, what the actual 
:ref:`log-module` offers, and how advanced power users can leverage them.

