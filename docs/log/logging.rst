.. _log-module:

Log Module
==========

The pyATS ``log`` module features `Formatter`_ and `Handler`_ classes that 
implements CiscoLog compatible message format & storage behavior.

Cisco logging standard can be summarized as:

- the log file is called a :ref:`tasklog`. There is only ever one active TaskLog
  per script execution process (eg, logging is not duplicated to multiple 
  files).

- log messages within the :ref:`tasklog` must be of :ref:`cisco-log-format`.

- :ref:`tasklog` can be changed on the fly within each testscript.

.. _Formatter: https://docs.python.org/3.4/library/logging.html#formatter-objects

.. _Handler: https://docs.python.org/3.4/library/logging.html#handler-objects

.. _cisco-log-format:

Cisco Log Format
----------------

Cisco log format is a per-line logging format for all Cisco related log outputs
& messages, standardized since the IOS days. It enables all routers & scripts to 
log in a common manner, and enables other infras to
filter and build tooling around it. This format can be summarized as the
following:

.. code-block:: text

    # the format itself, in Python logging formatter style
    # ----------------------------------------------------

    {seqnum}: {hostname}: {time}: %{appname}-{severity}-{msgname}: {tags}: {message}%

    seqnum      - message sequence number, starts with 0 for each process
    hostname    - current host name
    time        - timestamp in yyyy-mm-ddThh:mm:ss format
    appname     - the application generating this message
    severity    - message severity, range 1-7
    msgname     - name of the message
    tags        - optional tags associated with this message
    message     - message given by the user

    # Example
    # -------

    70: my-server: 2014-08-06T11:21:30: %AETEST-6-INFO: %[pname=python][pid=11295][tid=MainThread]: a log message
    71: my-server: 2014-08-06T11:21:30: %AETEST-6-INFO: %[pname=python][pid=11295][tid=MainThread]: another log message


Message Severity
----------------

The Cisco message severity equivalents are only displayed as part of the log
header. When logger outputs the final log message to file, the conversion to its 
equivalent severity number is automatically done. 

Following Table provides the Python logging level as described in
Python ``logging`` documentation and its severity's equivalent numerical value. 

+------------+-------------------+----------------------+
| LEVEL      | ``logging`` level | Cisco Msg Severity   |
+============+===================+======================+
| CRITICAL   | 50                | 2                    |
+------------+-------------------+----------------------+
| ERROR      | 40                | 3                    |
+------------+-------------------+----------------------+
| WARNING    | 30                | 4                    |
+------------+-------------------+----------------------+
| INFO       | 20                | 6                    |
+------------+-------------------+----------------------+
| DEBUG      | 10                | 7                    |
+------------+-------------------+----------------------+

.. note::

    the Python native logging levels are sufficient for all script/library 
    developments, and thus the following Cisco message severities are no-longer 
    supported in pyATS:

        - emergency

        - alert

        - notice

.. note::
    
    Cisco message severity and Python numeric levels are conceptually reversed.
    In Cisco message severity, if a level is lower, it's more important, 
    whereas in Python, if a level is higher, it's more important. Do not confuse
    the two - use the Python logic as described in the ``logging`` 
    documentation.


Installation and Updates
------------------------

The ``log`` module is installed by default as part of ``pyATS`` installation. 
The package is also featured in the PyPI server, and can be installed 
separately. ``log`` module is part of the ``pyats`` namespace, and therefore 
users should always refer to the full namespace when installing & using:

.. code-block:: bash

    pip install pyats.log

To upgrade an existing installation of log package in your environment, do: 

.. code-block:: bash

    pip install pyats.log --upgrade
