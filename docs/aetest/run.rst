.. _running_aetest_script:

Running TestScripts
===================

.. sidebar:: Helpful Reading

    - `__main__`_
    - `PYTHONPATH`_
    - `Shell Scripts`_

.. _`__main__`: https://docs.python.org/3.4/library/__main__.html
.. _Shell Scripts: http://linuxcommand.org/lc3_writing_shell_scripts.php
.. _PYTHONPATH: https://docs.python.org/3.4/using/cmdline.html#envvar-PYTHONPATH

There are two primary methods of running ``aetest`` testscripts directly.

Standalone
    running the testscript directly through Linux command-line, within a
    pyats instance. This allows independent execution of ``aetest``
    scripts, with all logging outputs defaulted to screen printing only.

    *Best suited for rapid, lightweight script development & iteration cycles
    without the need to create log archives, etc.*

Through Easypy
    running the testscript as a task through Easypy :ref:`easypy_jobfile`. This
    method requires the use of :ref:`easypy`, leverages all of the benefits it
    has to offer, and produces log & archives.

    *Best suited for sanity/regression (official) executions where standard
    environments, reporting & log archiving is required, and when post-mortem
    debugging is necessary.*

.. _aetest_argument_propagation:

Argument Propagation
--------------------

Before heading into execution modes, we need to first expand on how ``aetest``
parses and propagates command-line arguments. ``aetest`` uses Python standard
module `argparse`_ to parse command-line arguments stored in `sys.argv`_.
This process can be summarized into the following rules of thumb:

    - all known arguments (:ref:`aetest_standard_arguments`) are parsed by
      ``aetest``, and removed from ``sys.argv`` list.

    - all unknown arguments (arguments that aren't part of the standard argument
      list) are kept in ``sys.argv`` as they were and untouched.


.. _sys.argv: https://docs.python.org/3.4/library/sys.html#sys.argv
.. _argparse: https://docs.python.org/3.4/library/argparse.html

For example, when ``aetest`` is started, and ``sys.argv`` contains the following
command line arguments:

.. code-block:: python

    sys.argv = ['python script.py', '-loglevel=INFO', '-my_arg=1', '-your_arg=2']

``aetest`` takes away ``-loglevel=INFO``, and leave the rest in
``sys.argv``.

This argument propagation scheme allows users to pass additional arguments to
the testscript from the command line, and create their own parsers (eg, within
a ``subsection``) to make use of that additional information.

.. tip::

    when writing your own parsers using `argparse`_, use ``parse_known_args()``
    to parse arguments. This ensures the continuity of this argument
    propgation scheme, and avoids unknown argument exceptions when additional
    arguments are encountered.

.. _aetest_standalone_execution:

Standalone Execution
--------------------

Script executions are considered *standalone* when they are run via one of the
following mechanisms:

    - directly calling ``aetest.main()`` function within a user script/area, or,

    - indirectly calling ``aetest.main()`` function by invoking Python's
      `__main__`_ mechanism

.. _-m: https://docs.python.org/3/using/cmdline.html?highlight=#cmdoption-m
.. _Shebang: http://en.wikipedia.org/wiki/Shebang_%28Unix%29

In other words, user has the absolute control of the execution environment, and
``aetest`` is simply running as the **standalone** execution infrastructure. Do
not confuse this concept with dependencies: ``aetest`` is still dependent on the
current given *environment*, such as log settings, etc.

The following is a description of default script behaviors during standalone
execution. Keep in mind that these can be modified if necessary, as environment
control is entirely at the hands of the user.

    - Limited to a single script per invocation.

    - Runtime folder is the present working directory ``pwd``.

    - All logging is redirected to ``STDOUT`` and ``STDERR``.

    - No :ref:`tasklog`, result report and archive generation.

    - Uses the :ref:`aetest_standalone_reporter` which tracks result and prints
      summary to ``STDOUT``.

Because of the quick and easy nature of this execution mode, it is mostly used
during script development, where quick turn-arounds are key to success.

Generally speaking, to run your testscript under standalone mode, run the script
by invoking ``aetest.main()`` mechanism yourself. For example, the following
enables running your script directly through Linux command line.

.. code-block:: python

    # Example
    # -------
    #
    #   enabling standalone execution

    import logging
    from pyats import aetest

    # your testscript sections, testscases & etc
    # ...
    #

    # add the following as the absolute last block in your testscript
    if __name__ == '__main__':

        # control the environment
        # eg, change some log levels for debugging
        logging.getLogger(__name__).setLevel(logging.DEBUG)
        logging.getLogger('pyats.aetest').setLevel(logging.DEBUG)

        # aetest.main() api starts the testscript execution.
        # defaults to aetest.main(testable = '__main__')
        aetest.main()

.. note::

    you may also add a `Shebang`_ to your script and make it a direct executable
    under Linux. This is a Linux prerequisite skillset, and is not covered as
    part of this document.

This enables your script to be executed using ``python`` executable:

.. code-block:: bash

    # Example
    # -------
    #
    #   running an aetest script standalone using python executable
    #   (output timestamp removed for legibility purpose)

    (pyats) [tony@jarvis:pyats]$ python /path/to/your/script.py

        +------------------------------------------------------------------------------+
        |                            Starting common setup                             |
        +------------------------------------------------------------------------------+
        +------------------------------------------------------------------------------+
        |                      Starting subsection subsection_one                      |
        +------------------------------------------------------------------------------+
        The result of subsection subsection_one is => PASSED
        +------------------------------------------------------------------------------+
        |                      Starting subsection subsection_two                      |
        +------------------------------------------------------------------------------+
        The result of subsection subsection_two is => PASSED
        The result of common setup is => PASSED
        +------------------------------------------------------------------------------+
        |                          Starting testcase Testcase                          |
        +------------------------------------------------------------------------------+
        +------------------------------------------------------------------------------+
        |                          Starting section test_one                           |
        +------------------------------------------------------------------------------+
        The result of section test_one is => PASSED
        +------------------------------------------------------------------------------+
        |                          Starting section test_two                           |
        +------------------------------------------------------------------------------+
        The result of section test_two is => PASSED
        +------------------------------------------------------------------------------+
        |                         Starting section test_three                          |
        +------------------------------------------------------------------------------+
        The result of section test_three is => PASSED
        The result of testcase Testcase is => PASSED
        +------------------------------------------------------------------------------+
        |                               Detailed Results                               |
        +------------------------------------------------------------------------------+
         SECTIONS/TESTCASES                                                    RESULT
        --------------------------------------------------------------------------------
         .
         |-- CommonSetup                                                       PASSED
         |   |-- subsection_one                                                PASSED
         |   `-- subsection_two                                                PASSED
         `-- Testcase                                                          PASSED
             |-- test_one                                                      PASSED
             |-- test_two                                                      PASSED
             `-- test_three                                                    PASSED
        +------------------------------------------------------------------------------+
        |                                   Summary                                    |
        +------------------------------------------------------------------------------+
         Number of ABORTED                                                            0
         Number of BLOCKED                                                            0
         Number of ERRORED                                                            0
         Number of FAILED                                                             0
         Number of PASSED                                                             2
         Number of PASSX                                                              0
         Number of SKIPPED                                                            0
        --------------------------------------------------------------------------------

In essence, the ``main()`` function is what actually starts up the ``aetest``
script execution under standalone mode. It is the primary entry point to
``aetest``, and accepts the following optional arguments:

    - ``testable``, the :ref:`aetest_testable` to be loaded and tested. Defaults
      to ``'__main__'``.

    - any ``aetest`` :ref:`aetest_standard_arguments` as keyword arguments.

    - and all other additional ``**kwargs`` keyword arguments are used as
      :ref:`script_args` parameters during this execution.

If your scripts require any input arguments from the command line (eg, script
arguments), you will need to write your own argument parser, and provide that
parsed information as ``**kwargs`` to ``aetest.main()`` so that they become
:ref:`test_parameters`.

.. code-block:: python

    # Example
    # -------
    #
    #   parsing script arguments in standalone mode

    from pyats import aetest

    class Testcase(aetest.Testcase):

        # defining a test that prints out the current parameters
        # in order to demonstrate argument passing to parameters
        @aetest.test
        def test(self):
            print('Parameters = ', self.parameters)

    # do the parsing within the __main__ block,
    # and pass the parsed arguments to aetest.main()
    if __name__ == '__main__':

        # local imports under __main__ section
        # this is done here because we don't want to pollute the namespace
        # when the script isn't run under standalone
        import sys
        import argparse
        from pyats import topology

        # creating our own parser to parse script arguments
        parser = argparse.ArgumentParser(description = "standalone parser")
        parser.add_argument('--testbed', dest = 'testbed',
                            type = topology.loader.load)
        parser.add_argument('--vlan', dest = 'vlan', type = int)

        # do the parsing
        # always use parse_known_args, as aetest needs to parse any
        # remainder arguments that this parser does not understand
        args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

        # and pass all arguments to aetest.main() as kwargs
        aetest.main(testbed = args.testbed, vlan = args.vlan)


    # Let's run this script with the following command
    #   example_script.py --testbed /path/to/my/testbed.yaml --vlan 50

    # output of the script:
    #
    #   +------------------------------------------------------------------------------+
    #   |                          Starting testcase Testcase                          |
    #   +------------------------------------------------------------------------------+
    #   +------------------------------------------------------------------------------+
    #   |                            Starting section test                             |
    #   +------------------------------------------------------------------------------+
    #   Parameters = {'testbed': <Testbed object at 0xf717578c>, 'vlan': 50})
    #   The result of section test is => PASSED
    #   The result of testcase Testcase is => PASSED

.. tip::

    when writing standalone argument parsers, try to only parse known arguments
    using ``parse_known_args()``. This allows all remaining ``aetest`` only
    arguments to propagate upstream, adhering to ``aetest``
    :ref:`aetest_argument_propagation` scheme.

There are many other possible use cases of ``aetest.main()`` under standalone
execution. This mechanism provides maximum flexibility & debuggability to the
end user, and simply runs ``aetest`` test infrastructure as is. For example,
it can also be called directly in a python interactive shell, as long as you
provide it the right arguments.

.. code-block:: shell

    # Example
    # -------
    #
    #   demonstrating the usages of aetest.main()
    #   (this is a python interpreter demo)

    # launch the python interpreter
    # and call main() by providing the script to be run as testable

    (pyats) [tony@jarvis:pyats]$ python
    Python 3.4.1 (default, Nov 12 2014, 13:34:48)
    [GCC 4.4.6 20120305 (Red Hat 4.4.6-4)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from pyats.aetest import main
    >>> main(testable = '/path/to/your/script.py')
    ... execution output ...
    >>>

.. tip::

    If you want the test script's bash exit code to reflect the outcome of the
    tests in your test scrip, then save the result of ``aetest.main()`` and pass
    it into ``aetest.exit_cli_code()`` like this:

    .. code-block:: python

        result = aetest.main()
        aetest.exit_cli_code(result)

    ``aetest.exit_cli_code`` will cause the script to exit and returns 0 or 1 to
    the environment as the exit code. 0 is returned if all tests in the script
    pass and 1 is returned if one or more tests fail (or if all tests are
    skipped).


.. _aetest_jobfile_execution:

Easypy Execution
----------------

Scripts executed with :ref:`easypy` is called *Easypy Execution*. In this mode,
all environment handling and control is set by the Easypy launcher. For example, the
following features are available:

    - multiple ``aetest`` test scripts can be executed together, aggregated
      within a :ref:`job file<easypy_jobfile>`.

    - initial logging configuration is done by :ref:`easypy`, with user
      customizations within the job file.

    - :ref:`tasklog`, result report and archives are generated.

    - uses :ref:`reporter` for reporting & result tracking,
      generating result YAML file and result details and summary XML files.

Easypy execution is the typical way of running ``aetest`` scripts for production
testing purposes such as sanity/regression testing. It offers a standard,
managed & replicable test environment for script execution; and most
importantly, creates an archive file containing log outputs & environment
information for post-mortem debugging.

.. note::

    this section only expands on ``aetest`` behaviors when executed through
    Easypy. :ref:`easypy` understanding is a prerequisite.

Each ``aetest`` script ran within a job file is called a *task*. Here's an
example of a simple job file with a single task.

.. code-block:: python

    # Example
    # -------
    #
    #   pyats job file example, integrating aetest scripts

    from pyats.easypy import run

    # job file needs to have a main() definition
    # which is the primary entry point for starting job files
    def main():

        # run a testscript
        # ----------------
        # easypy.run() api defaults to using aetest as the test infrastructure
        # to execute the testscript. Eg, this is the exact same as doing:
        #   run(testscript='/path/to/your/script.py',
        #       testinfra = 'pyats.aetest')
        run(testscript='/path/to/your/script.py')

In essence, during Easypy execution, each job file's ``run()`` api invokes
``aetest`` infrastructure independently and runs the provided testscript. The
following behaviors are observed:

    - all ``aetest`` :ref:`aetest_standard_arguments` are accepted as keyword
      arguments.

    - all ``**kwargs`` keyword arguments to ``run()`` api propagate to
      the testscript as :ref:`script_args`.

    - in addition, if ``pyats run job`` was launched with a testbed file (through
      ``--testbed-file`` or ``--logical-testbed-file`` arguments,
      see :ref:`easypy_arguments`), the corresponding testbed object
      propagates to the testscript as argument ``testbed``.

    - If neither ``--testbed-file`` nor ``--logical-testbed-file`` was
      provided to ``pyats run job``, then the argument
      ``testbed`` is set to `None`.


.. code-block:: python

    # Example
    # -------
    #
    #   pyats job file example, with script arguments

    from pyats.easypy import run

    def main():

        # providing a couple custom script arguments as **kwargs
        run(testscript='/path/to/your/script.py',
            pyats_is_awesome = True,
            aetest_is_legendary = True)

    # if this job file was run with the following command:
    #   pyats run job example_job.py --testbed-file /path/to/my/testbed.yaml
    #
    # and the script had one testcase that prints out the script's parameters,
    # the output of the script ought to be:
    #
    #   starting test execution for testscript 'a.py'
    #   +------------------------------------------------------------------------------+
    #   |                          Starting testcase Testcase                          |
    #   +------------------------------------------------------------------------------+
    #   +------------------------------------------------------------------------------+
    #   |                            Starting section test                             |
    #   +------------------------------------------------------------------------------+
    #   Parameters = {'testbed': <Testbed object at 0xf742f74c>,
    #                 'pyats_is_awesome': True,
    #                 'aetest_is_legendary': True}
    #   The result of section test is => PASSED
    #   The result of testcase Testcase is => PASSED


.. _aetest_standard_arguments:

Standard Arguments
------------------

``aetest`` accepts a number of standard arguments that can be used to influence
and/or change script execution behaviors. They can be provided either as command
line arguments when running directly under Linux shell, or used as keyword
arguments to ``aetest.main()`` and ``easypy.run()``.

.. csv-table:: AETest Standard Arguments
    :header: "Keyword", "Command Line", "Description"

    "n/a", ``-help``, "display help information"
    ``uids``, ``-uids``, "specify the list of section uids to run (logic
    expression)"
    ``groups``, ``-groups``, "specify the list of testcase groups to run (logic
    expression)"
    ``datafile``, ``-datafile``, "input datafile/value for this script"
    ``random``, ``-random``, "flag to enable testcase randomization"
    ``random_seed``, ``-random_seed``, "testcase randomization seed"
    ``max_failures``, ``-max_failures``, "max acceptable number of failures"
    ``pdb``, ``-pdb``, "start interactive debugger on failure"
    ``step_debug``, ``-step_debug``, "step debug input file"
    ``pause_on``, ``-pause_on``, "pause on phrase input string/file"
    ``loglevel``, ``-loglevel``, "``aetest`` logging level"
    ``submitter``, ``-submitter``, "submitter of this script (defaults to
    current user)"

.. code-block:: text

    Table Legend
    ------------

    Keyword: keyword argument name
    Command Line: command-line argument name


``-help``
    used under command-line to provide help information w.r.t. available command
    line arguments and how to use them.

    .. code-block:: bash

        bash$ python /path/to/my/script.py -help
        bash$ python -m pyats.aetest -help

``uids``, ``-uids``
    specify the list of section uids to be executed using a callable expression.
    This argument takes in a ``callable`` that returns True or False for each
    section uid input, controlling whether the section is run or not. (Docs @
    :ref:`aetest_uids`)

    When using this argument in command line, the input is required to be of
    valid python syntax, evaluatable by :ref:`logic_from_str`.

    .. code-block:: bash

        bash$ python testscript.py -uids "And('pattern_1', 'pattern_2')"

    .. code-block:: python

        # aetest.main() example using datastructure logic
        from pyats.datastructures.logic import Or
        aetest.main('testscript.py', uids = Or('common_setup',
                                               '^test_.*',
                                               'common_cleanup'))

        # easypy.run() example (job file snippet) using lambda
        run(testscript = 'testscript.py', uids = lambda tc, section=None: tc in ['common_setup', 'test_one'])

``groups``, ``-groups``
    expression specifying the group(s) of testcases to execute. This argument
    accepts a ``callable`` evaluating to True/False, where each testcase's
    groups field is supplied as input, to test whether that
    testcase should run or not (Docs @ :ref:`aetest_groups`)

    When using this argument in command line, the input is required to be of
    valid python syntax, evaluatable by :ref:`logic_from_str`.

    .. code-block:: bash

        bash$ python testscript.py -groups="And(Or('group1','group2'), 'group3')"

    .. code-block:: python

        # aetest.main() example using datastructure logic
        from pyats.datastructures.logic import Or, And
        aetest.main('testscript.py', groups = And(Or('group1','group2'), 'group3'))

        # easypy.run() example (job file snippet) using datastructure logic
        from pyats.datastructures.logic import Or, And
        run(testscript = 'testscript.py', groups = And(Or('group1','group2'), 'group3'))

``datafile``, ``-datafile``
    full name and path or URL to the script input datafile file in YAML format. 
    For full detail on use cases and examples, refer to :ref:`aetest_datafile`.

    .. code-block:: bash

        bash$ python testscript.py -datafile="/path/to/datafile.yaml"
        bash$ python testscript.py -datafile="http://<url>/datafile.yaml"

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', datafile = "/path/to/datafile.yaml")

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', datafile = "/path/to/datafile.yaml")


``random``, ``-random``
    flag to enable testcase randomization, allowing a script's testcase orders
    to be randomly shuffled before execution. To learn more about testcase
    randomization, refer to :ref:`aetest_testcase_randomization`.

    .. code-block:: bash

        bash$ python testscript.py -random

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', random = True)

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', random = True)

``random_seed``, ``-random_seed``
    randomization seed integer, used to fix the randomizer and re-generate the
    same testcase sequence, useful for debugging purposes. Requires testcase
    randomization to be turned on first. To learn more about it, refer to
    :ref:`aetest_testcase_randomization`.

    .. code-block:: bash

        bash$ python testscript.py -random -random_seed 42

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', random = True, random_seed = 42)

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', random = True, random_seed = 42)

``max_failures``, ``-max_failures``
    integer specifying the maximum number of failures allowed before the script
    auto-aborts. Refer to :ref:`aetest_max_failures` for details.

    .. code-block:: bash

        bash$ python testscript.py -max_failures 13

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', max_failures = 13)

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', max_failures = 13)

``pdb``, ``-pdb``
    flag, allowing AEtest to automatically invoke the python interactive
    debugger ``pdb`` on failure/errors. Refer to :ref:`aetest_pdb` for details.

    .. code-block:: bash

        bash$ python testscript.py -pdb

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', pdb = True)

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', pdb = True)

``step_debug``, ``-step_debug``
    full name and path to step debug file, containing debug commands to run at
    each testcase steps. To learn more about steps, refer to :ref:`aetest_steps`
    documentation.

    .. code-block:: bash

        bash$ python testscript.py -step_debug="/path/to/my/stepdebugfile"

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', step_debug = "/path/to/my/stepdebugfile")

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', step_debug = "/path/to/my/stepdebugfile")

``pause_on``, ``-pause_on``
    full name and path to pause on phrase file, its dictionary content in
    string format, or a plain string. For full detail on use cases and examples,
    refer to :ref:`aetest_pause_on_phase` documentation.

    .. code-block:: bash

        bash$ python testscript.py -pause_on="some string to pause"

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', pause_on = "/path/to/my/pause_on_file")

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', pause_on = "/path/to/my/pause_on_file")

``loglevel``, ``-loglevel``:
    changes the ``pyats.aetest`` logger loglevel. Defaults to ``logging.INFO``.

    .. code-block:: bash

        bash$ python testscript.py -loglevel=DEBUG

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', loglevel="DEBUG")

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', loglevel="WARNING")

``submitter``, ``-submitter``:
    changes the submitter user id. Defaults to current Linux shell user.

    .. code-block:: bash

        bash$ python testscript.py -submitter="tonystark"

    .. code-block:: python

        # aetest.main() example
        aetest.main('testscript.py', submitter="blackwidow")

        # easypy.run() example (job file snippet)
        run(testscript = 'testscript.py', submitter="warmachine68")


.. _aetest_testable:

Testable
--------

The definition of a *testable* in ``aetest`` is any object that can be loaded
by ``aetest.loader`` module into a ``TestScript`` class instance and executed
as a testscript without throwing errors.

.. code-block:: python

    # Example
    # -------
    #
    #   aetest loader

    from pyats.aetest import loader

    # load a testscript file directly into an object
    # and check the object type.
    obj = loader.load(testable = '/path/to/testScript.py')
    obj
    # <class 'TestScript' uid='pyats.aetest.testscript'>

The following are acceptable as **testables**:

    - full path/name to a python file ending with ``.py``

      .. code-block:: python

          aetest.main(testable = '/paty/to/your/test/script/file.py')

    - any module name that is part of current `PYTHONPATH`_

      .. code-block:: python

          aetest.main(testable = 'regression.bgp.traffic_suite')

    - any non built-in module objects (instances of ``types.ModuleType``)

      .. code-block:: python

          from regression.bgp import traffic_suite

          aetest.main(testable = traffic_suite)

Do not confuse **testables** with *testscripts that generate meaningful testing
and results*. Because of python's specific **inspect & run** mechanism, it is
possible to pass meaningless modules (such as ``urllib``) to ``aetest``, and
generate 0 results because even-though it passes as a testable, it contains no
actual tests.

    *Just because you can run it as a testscript doesn't mean it performs any
    consequential testing.*
