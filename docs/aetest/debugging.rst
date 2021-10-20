Debugging Resources
===================


.. sidebar:: Helpful Reading

    - `The Python Debugger`_

    - :ref:`resources_debugging_python`

    - :ref:`testbench`

.. _The Python Debugger: https://docs.python.org/3/library/pdb.html

    *If only we wrote perfect code from the get-go...*

This section describes in detail AEtest built-in tools that may be useful during
your quest on zapping those pesty bugs. Keep in mind that there may be more
than one way to debug something: the following are supplements to any existing
public ways of debugging python code.

.. hint::

    there is **no magic**: the AEtest engine is **purely** developed in python.

.. _mutiprocess_pdb:

PDB & Multiprocessing
---------------------

Python's native interactive source code debugger ``pdb`` is quite powerful when
it comes to zapping bugs: setting breakpoints, stepping code, inspecting stack
frames & such. This documentation is not going to cover the use of it: for all
intents and purposes, read the official documentation: `The Python Debugger`_.

However, one thing to note is that ``pdb`` does not play well with python
`Multiprocessing`_ module. When ``multiprocessing`` forks a child process,
it closes the ``stdin`` as part of the default child process bootstrap. Thus,
as ``pdb`` relies on ``stdin`` to provide an interactive session, it crashes
with the following cryptic exception:

.. code-block:: text

    Traceback (most recent call last):
      File "/auto/pysw/cel63/python/3.4.1/lib/python3.4/multiprocessing/process.py", line 254, in _bootstrap
        self.run()
      File "/auto/pysw/cel63/python/3.4.1/lib/python3.4/multiprocessing/process.py", line 93, in run
        self._target(*self._args, **self._kwargs)
      File "<stdin>", line 2, in func
      File "/auto/pysw/cel63/python/3.4.1/lib/python3.4/bdb.py", line 52, in trace_dispatch
        return self.dispatch_return(frame, arg)
      File "/auto/pysw/cel63/python/3.4.1/lib/python3.4/bdb.py", line 96, in dispatch_return
        if self.quitting: raise BdbQuit
    bdb.BdbQuit

This error can be typically seen when trying to use ``pdb`` in your script while
it ran under :ref:`aetest_jobfile_execution` (as a Task/subprocess), forcing you
to *debug the debugger* for hours...

Luckily, there are a few known ways to workaround this problem:

1. Open ``/dev/stdin`` manually in child process before launching pdb, or use
   the following ``ForkedPdb`` class:

   .. code-block:: python

       import sys
       import pdb

       class ForkedPdb(pdb.Pdb):
           '''A Pdb subclass that may be used
           from a forked multiprocessing child
           '''

           def interaction(self, *args, **kwargs):
               _stdin = sys.stdin
               try:
                   sys.stdin = open('/dev/stdin')
                   pdb.Pdb.interaction(self, *args, **kwargs)
               finally:
                   sys.stdin = _stdin

       # to use:
       ForkedPdb().set_trace()

2. Use Easypy Task argument ``pdb = True``, which automatically opens
   ``/dev/stdin`` in the given task process, and also turning on
   :ref:`aetest_pdb`.

3. Use a multiprocesss-aware debugger like `Winpdb`_

4. Any other creative methods you may cook-up :-)

.. _Winpdb: http://manpages.ubuntu.com/manpages/bionic/man1/winpdb.1.html
.. _Multiprocessing: https://docs.python.org/3.4/library/multiprocessing.html

.. hint::

    **StackOverflow** is your friend: http://stackoverflow.com/questions/4716533

.. _aetest_pdb:

PDB on Failure
--------------

``pdb`` is golden, but putting ``pdb`` everywhere in your scripts and
libraries trying to catch a runaway bug is... not pretty. There are
times where you can't seem to figure out what, where, and why an exception is
raised, why your script is failing, and where to put
``import pdb; pdb.set_trace()``...

    *PDB on Failure to the rescue!*

When AEtest scripts are run with the flag ``pdb = True``, whenever an error,
failure, or exception is encountered during execution, the testing engine
pauses and starts an interactive `post_mortem`_ debugging session
at the stack frame of failure.


.. _post_mortem: https://docs.python.org/3.4/library/pdb.html#pdb.post_mortem

.. tip::

    Additionally to ``pdb = True``, pyATS debugging supports any debugger that 
    has post_mortem capabilities. Want to use ``pudb``? Set ``pdb = 'pudb'``.
    Want to use ``web-pdb``? Set ``pdb = 'web_pdb'``.

.. code-block:: python

    # Example
    # -------
    #
    # PDB on Failure demonstration

    from pyats import aetest

    class CommonSetup(aetest.CommonSetup):
        @aetest.subsection
        def subsection(self):
            pass

    class TestcaseOne(aetest.Testcase):

        @aetest.setup
        def setup(self):
            pass

        @aetest.test
        def test(self):
            # raise an exception by calling something that doesn't exist
            blablabla()

        @aetest.cleanup
        def cleanup(self):
            pass

    class CommonCleanup(aetest.CommonCleanup):
        @aetest.subsection
        def subsection(self):
            pass

    aetest.main(pdb = True)

    # output result:
    #
    # +------------------------------------------------------------------------------+
    # |                            Starting common setup                             |
    # +------------------------------------------------------------------------------+
    # +------------------------------------------------------------------------------+
    # |                        Starting subsection subsection                        |
    # +------------------------------------------------------------------------------+
    # The result of subsection subsection is => PASSED
    # The result of common setup is => PASSED
    # +------------------------------------------------------------------------------+
    # |                        Starting testcase TestcaseOne                         |
    # +------------------------------------------------------------------------------+
    # +------------------------------------------------------------------------------+
    # |                            Starting section setup                            |
    # +------------------------------------------------------------------------------+
    # The result of section setup is => PASSED
    # +------------------------------------------------------------------------------+
    # |                            Starting section test                             |
    # +------------------------------------------------------------------------------+
    # Caught exception during execution:
    # Traceback (most recent call last):
    #   File "a.py", line 16, in test
    #     blablabla()
    # NameError: name 'blablabla' is not defined
    # > example_pdb_on_failure.py(16)test()
    # > blablabla()
    # (Pdb)
    #

The interactive debugging session starts with ``(pdb)`` prompt, and waits for
user input. Refer to `Debugger Commands`_ for details on how to use the ``pdb``
debugger.

You can also use ``pdb`` from the command line by including ``--pdb``. This will
drop you into the default Python pdb debugger. If you have a third-party debugger
installed that supports post_mortem you can specify it like so ``--pdb <debugger>``.

Examples:

.. code-block::

    pyats run job job.py --pdb
    pyats run job job.py --pdb pudb
    pyats run job job.py --pdb web_pdb

.. tip::

    submitting a testscript to sanity/regression with ``pdb = True`` may be
    career-limiting.

.. _Debugger Commands: https://docs.python.org/3.4/library/pdb.html#debugger-commands


.. _aetest_pause_on_phase:

Pause on Phrase
---------------

``import pdb; pdb.set_trace()`` and :ref:`aetest_pdb` features both have its
limitations: the first requires editing the script, and the second only pauses
when an exception or non-passing result occurs. What about cases where you just
want to pause the testscript execution somewhere & check the current state
and/or configuration of your environment, logs, and testbed devices?

The **pause on phrase** feature allows you to pause on **any** log messages
generated by the current script run, without requiring any modifications to the
scripts and/or its libraries. When enabled, it actively filters all log messages
propagated to the ``logging.root`` logger, and pauses when a match is found.

Three distinct types of pause actions are supported:

``email``
    pauses, creates a *pause file* and notifies the user via email. Deleting
    this file (or after a set timeout value is reached) resumes the script
    execution.

``pdb``
    pauses and opens a Python `Pdb Debugger`_ at the caller stack.

``code``
    pauses and opens a Python `Interactive Shell`_ at the caller stack.

.. _Pdb Debugger: https://docs.python.org/3.4/library/pdb.html
.. _Interactive Shell: https://docs.python.org/3.4/tutorial/interpreter.html#interactive-mode

To enable this feature, provide the ``pause_on`` (see
:ref:`aetest_standard_arguments`) to your script run with one of the following
types of values:

    - full path & name to a YAML input file, satisfying the schema described
      below, **or**

    - the content of said YAML file, in corresponding dictionary format, **or**

    - a regex string for the engine to look and pause on.

The following schema describes the YAML pause file format:

.. code-block:: yaml

    # Pause On Phrase YAML Schema
    # ---------------------------

    timeout:    # timeout value in seconds (int)
                # specifies the max pause time before the script resumes
                # execution automatically. Set to 0 to wait indefinitely.
                # (only applies to email action)
                # (default: 0)
                # (optional)

    action:     # action to be performed on pause (email/pdb/code)
                # choose to either send user a notification email, provide a
                # pdb debugger, or an interactive code shell on pause.
                # (disables timeout value when action is pdb or code)
                # (default: email)
                # (optional)

    patterns:   # patterns to search & pause on (list)
                # each list item needs to follow a particular structure as below
                # (mandatory)

        - pattern:      # pattern to pause on (str)
                        # this is internally compiled into a regex pattern used
                        # to match log messages with
                        # (mandatory)

          section:      # section/uid to enable pattern searching (str)
                        # this is internally compiled into regex, used
                        # to match the current executing section uid
                        # note that you can use Testcase.setup to denote setup
                        # section of a testcase, etc.
                        # (if not provided, the pattern is used globally)
                        # (optional)

Normally, the default action is ``email``: when the script is paused after
matching a log phrase, it sends a notification email to the current
executing user, including with it the instructions on how to resume execution
(eg, remove the pause file).

.. note::

    If the execution is paused in ``email`` mode and the pause file is modified,
    timer will be disabled and execution will be paused until the pause file is
    deleted.

However, if the action is set to ``pdb`` or ``code``, the script pauses
and provides an interactive python debugger/shell to the user, allowing for
look-arounds, debugs & etc. *Be careful with what you do in these modes:*
modifications persist when the script continues.

.. hint::

    use ``Ctrl-D`` to resume from interactive shell, and ``c`` to resume from
    pdb.

.. warning::

    timeout counter is not active/disregarded in pdb/interactive mode.

Here's an example YAML pause file:

.. code-block:: yaml

    # Example
    # -------
    #
    #   yaml input pause file

    timeout: 600        # pause a maximum of 10 minutes

    patterns:
        - pattern: '.*pass.*'           # pause on all log messages including
                                        # .*pass.* in them globally

        - pattern: '.*state: down.*'    # pause whenever  'state: down' is found
          section: '^common_setup\..*$' # enable for all common_setup sections

        - pattern: '.*should pause.*'      # pause whenever 'should pause' is found
          section: '^TestcaseTwo\.setup$'  # pause on TestcaseTwo setup section

Keep in mind that the content of YAML seamlessly translates to Python ``dict``
types. Therefore, as a convenience feature, it is also possible to use the
content of a YAML file in its dict format as input to ``pause_on`` instead of
a file:

.. code-block:: python

    # Example
    # -------
    #
    #   dict format corresponding to the above

    pause_on = {'timeout': 600,
                'patterns': [{'pattern': '.*pass.*'},
                             {'pattern': '.*state: down.*',
                              'section': '^common_setup\..*$'},
                             {'pattern': '.*should pause.*',
                              'section': '^TestcaseTwo\.setup$'}]}

    # command-line call
    # -----------------
    #   python testscript.py -pause_on="{'timeout': 600,\
    #                                    'patterns': [{'pattern': '.*pass.*'},\
    #                                                 {'pattern': '.*state: down.*',\
    #                                                  'section': '^common_setup\..*$'},\
    #                                                 {'pattern': '.*should pause.*',\
    #                                                  'section': '^TestcaseTwo\.setup$'}]}"

.. hint::

    if your pause regex patterns are extremely generic, eg, ``.*``, it
    pauses ... a **lot**. However, if multiple regex matches to the same log
    message, the engine is pretty smart about only pausing once, and avoiding
    duplicated pauses on this same message.

In addition, as a convenience measure, it is also possible to simply provide a
*string* to the ``pause_on`` argument. This *simplified* input mode is mostly intended
for local debugging sessions, avoiding the need to use a properly formatted
dictionary or YAML file. As this is solely intended for interactive debugging,
the default action with simplified input mode is ``pdb``.

.. code-block:: text

    # Example
    # -------
    #
    #   using simple string regex inputs

    # pause on all instances of 'some phrase'
    bash$ python testscript.py -pause_on='.*some phrase.*'

Below are some examples of the pause on phrase feature in action:

.. code-block:: python

    # Example 1
    # ---------
    #
    #   pause on phrase with code action

    from pyats import aetest

    import logging

    logger = logging.getLogger()

    class CommonSetup(aetest.CommonSetup):
        @aetest.subsection
        def subsection(self):
            pass

    class tc_one(aetest.Testcase):

        @aetest.setup
        def setup(self):
            pass

        @aetest.test
        def test(self):
            logger.info('i should pause')

        @aetest.cleanup
        def cleanup(self):
            pass

    class CommonCleanup(aetest.CommonCleanup):
        @aetest.subsection
        def subsection(self):
            pass

    if __name__ == '__main__':
        logging.root.setLevel(logging.INFO)
        aetest.main(pause_on = dict(action = 'code',
                                    patterns = [{'pattern': 'i should pause'}]))
    # output of the script:
    #
    #    Starting common setup
    #    Starting subsection subsection
    #    The result of subsection subsection is => PASSED
    #    The result of common setup is => PASSED
    #    Starting testcase tc_one
    #    Starting section setup
    #    The result of section setup is => PASSED
    #    Starting section test
    #    i should pause
    #
    #    --------------------------------------------------------------------------------
    #    Pause On Phrase: Interactive Console
    #    -> /path/to/my/example/testscript.py[20] test()
    #    (press Ctrl-D to resume execution)
    #    >>>


    # Example 2
    # ---------
    #
    #   pause on phrase with from command line, simplified mode

    # output of the script:
    #   +------------------------------------------------------------------------------+
    #   |                            Starting common setup                             |
    #   +------------------------------------------------------------------------------+
    #   +------------------------------------------------------------------------------+
    #   |                        Starting subsection subsection                        |
    #   +------------------------------------------------------------------------------+
    #   The result of subsection subsection is => PASSED
    #   The result of common setup is => PASSED
    #   +------------------------------------------------------------------------------+
    #   |                           Starting testcase tc_one                           |
    #   +------------------------------------------------------------------------------+
    #   +------------------------------------------------------------------------------+
    #   |                            Starting section setup                            |
    #   +------------------------------------------------------------------------------+
    #   The result of section setup is => PASSED
    #   +------------------------------------------------------------------------------+
    #   |                            Starting section test                             |
    #   +------------------------------------------------------------------------------+
    #   i should pause
    #
    #   --------------------------------------------------------------------------------
    #   Pause On Phrase: Interactive Console
    #   -> /path/to/my/example/testscript.py[20] test()
    #   (press Ctrl-D to resume execution)
    #   >>>
