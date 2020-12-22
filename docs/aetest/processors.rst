.. _aetest_processors:

Section Processors
==================

.. sidebar:: Helpful Reading

    - `Preprocessors`_
    - `Decorators`_
    - :ref:`object_model`

.. _Decorators: https://wiki.python.org/moin/PythonDecorators
.. _Preprocessors: http://en.wikipedia.org/wiki/Preprocessor
.. _Exception: https://docs.python.org/3.4/library/exceptions.html

In ``aetest``, functions and methods scheduled to run immediately before and
after testscript sections are called **pre-processors**, **post-processors**,
**exception-processors**.
These programs possess the ability to *process* the given section based on its
id, parameters and results, dynamically and directly affecting the outcome of
testing.

Because of this unique inline execution trait, pre/post/exception processors may
also be used as means to perform common, routine checks before and after each
test section. Here are some possible use cases:

Pre-Processors
    - take snapshots of the current test environment information (eg, testbed
      configuration)

    - check the test environment and determine if the current section should
      run or not

Post-Processors
    - access/validate the result of the section that just finished execution

    - check current test environment against previous snapshots (eg, router
      health-checking)

    - execute debug commands, collect dump files & etc

Exception-Processors
    - take post exception snapshots of the current test environment information
      (eg, testbed configuration) when exception occurs

    - execute debug commands, collect dump files & etc when exception occurs

    - suppress a specified Exception_ and assign a result to the section.

The usage of pre/post/exception processor feature is entirely *optional*. They
can access the internals of ``aetest`` :ref:`object_model`, and can be extremely
powerful.

    *With great power, comes great responsibilities* - use them wisely.


Definition & Arguments
----------------------

Pre/post/exception processors are affixed to each script sections using
``@processors`` decorator, and providing it lists of objects for each condition.

.. code-block:: text

    Syntax
    ------

        @processors(pre = [list of pre-processor objects],
                    post = [list of post-processor objects],
                    exception = [list of exception-processor objects])

Processor functions support :ref:`parameter <test_parameters>` propagation the
same way that test sections do. Parameters from parent objects, or a
:ref:`datafile <aetest_datafile>` (eg. the testbed) can be passed to a processor
by simply declaring an argument of the same name. Some default parameters
available for all processors are:
    - `section` for the Testcase or Test Section the processor is being applied
      to
    - `processor` for the running processor itself, which has a `properties`
      attribute, as well as result APIs (eg. `processor.failed()`
    - `steps` for declaring :ref:`steps <aetest_steps>` within the processor

Exception processors also have default parameters of `exc_type`, `exc_value`,
and `exc_traceback` for the exception that occurs in the parent section.

.. code-block:: python

    # Example
    # -------
    #
    #   simple pre/post/exception processor example

    from pyats import aetest

    # define a function that prints the section's uid
    def print_uid(section):
        print('current section: ', section.uid)

    # define a function that prints the section result
    def print_result(section):
        print('section result: ', section.result)

    # define another function that prints the exception message and suppress the
    # exception
    def print_exception_message(section, exc_type, exc_value, exc_traceback):
        print('exception : ', exc_type, exc_value)
        return True

    # use the above functions as pre/post/exception processors to a Testcase
    #   pre-processor  : print_uid
    #   post-processor : print_result
    #   exception-processor : print_exception_message
    @aetest.processors(pre = [print_uid],
                       post = [print_result],
                       exception = [print_exception_message])
    class Testcase(aetest.Testcase):

        @aetest.test
        def test(self):
            print('running testcase test section')

        @aetest.test
        def testException(self):
            raise Exception('running testcase testException section')

    # define a function that fails when a section does not set a parameter, this
    # will propagate the failure to the parent section
    def fail_if_not_a(processor):
        a = processor.parameters.get('a')
        if not a:
            processor.failed('a was not set to True')

    class Testcase2(aetest.Testcase):
        # use fail_if_not_a as a post-processor on only this test section
        @aetest.processors.post(fail_if_not_a)
        @aetest.test
        def test(self):
            self.parameters['a'] = False

    # script output
    #   - notice that the processors ran immediately before and after the
    #     testcase execution.
    #
    #     +------------------------------------------------------------------------------+
    #     |                          Starting testcase Testcase                          |
    #     +------------------------------------------------------------------------------+
    #     +------------------------------------------------------------------------------+
    # ->  |                     Starting PreProcessor-1 'print_uid'                      |
    #     +------------------------------------------------------------------------------+
    # ->  current section:  Testcase
    #     +------------------------------------------------------------------------------+
    #     |                            Starting section test                             |
    #     +------------------------------------------------------------------------------+
    #     running testcase test section
    #     The result of section test is => PASSED
    #     +------------------------------------------------------------------------------+
    #     |                        Starting section testException                        |
    #     +------------------------------------------------------------------------------+
    #     +------------------------------------------------------------------------------+
    # ->  |           Starting ExceptionProcessor-1 'print_exception_message'            |
    #     +------------------------------------------------------------------------------+
    # ->  exception :  <class 'Exception'> running testcase testException section
    # ->  The result of section testException is => PASSED
    #     +------------------------------------------------------------------------------+
    # ->  |                   Starting PostProcessor-1 'print_result'                    |
    #     +------------------------------------------------------------------------------+
    # ->  section result:  passed
    #     The result of testcase Testcase is => PASSED
    #     +------------------------------------------------------------------------------+
    #     |                         Starting testcase Testcase2                          |
    #     +------------------------------------------------------------------------------+
    #     +------------------------------------------------------------------------------+
    #     |                            Starting section test                             |
    #     +------------------------------------------------------------------------------+
    #     +------------------------------------------------------------------------------+
    # ->  |                   Starting PostProcessor-1 'fail_if_not_a'                   |
    #     +------------------------------------------------------------------------------+
    #     The result of PostProcessor-1 'fail_if_not_a' is => FAILED
    #     The result of section test is => FAILED
    #     The result of testcase Testcase2 is => FAILED

Since parameters are only passed when there is an argument of the same name, any
functions & methods that require zero arguments to invoke are useable as
pre/post processors. However making use of the arguments to access parameters
provides many options. The `section` parameter can be passed as an argument,
which references the current running section object that the processor has been
applied to. This enables the processor function to access within the current
executing object, reference its :ref:`test_parameters` and act accordingly.
Refer to :ref:`object_model` for section object details.

Pre/post/exception processors can be applied independently towards both test
containers (``CommonSetup``, ``Testcase``, ``CommonCleanup``) and test sections
(``subsections``, ``setup``, ``test``, ``cleanup``). Each section may receive
an arbitrary number of processor functions, run in the order of appearance.

.. note::

    A section can have multiple processors all trying to set the result through
    APIs. The final result set for the section will be the 'rolled-up' result
    from all of the processors of that type. (see :ref:`object_model` for rules
    about roll-up).


.. note::

    If **pre-processors** block a section from executing, the
    **post-processors** will not be executed.


The decorator ``@processors`` can be used to define both **pre-processors**,
**post-processors** and **exception-processors** at the same time. The following
alternatives allows the definition of one specific type using ``*varargs`` style
input.

.. code-block:: text

    Alternative Syntax
    ------------------

        @processor.pre(*list of pre-processors)
        @processor.post(*list of post-processors)
        @processor.exception(*list of exception-processors)


.. code-block:: python

    # Example
    # -------
    #
    #   extended pre/post processor/exception examples

    from pyats import aetest

    # assuming we had a library full of readily defined processor functions
    # import all of them for the sake of this example
    from pre_processors import *
    from post_processors import *
    from exception_processors import *

    class common_setup(aetest.CommonSetup):

        # attach some pre-processors to subsection
        # using @aetest.processors.pre(x, y, z, ...) shortcut definition
        # this is equivalent to:
        #   @aetest.processors(pre = [x, y, z, ...])
        @aetest.processors.pre(collect_snapshot)
        @aetest.subsection
        def subsection(self):
            pass

    # attach multiple processors to testcase
    @aetest.processors(pre = [check_environment, collect_snapshot, check_uid],
                       post = [router_health_check, restore_snapshot],
                       exception = [unexpected_exception_snapshot])
    class Testcase(aetest.Testcase):

        # attach some post-processors to test section
        # using @aetest.processors.post(x, y, z, ...) shortcut definition
        # this is equivalent to:
        #   @aetest.processors(post = [x, y, z, ...])
        @aetest.processors.post(run_debug_commands, check_memory_leak)
        @aetest.test
        def test(self):
            pass


Results
-------

Processors also have a result, which can be set in multiple ways. The `section`
object and the `processor` object both have :ref:`result_apis` which act in
slightly different ways. Any result apis called from the `processor` object
behave as expected, setting a result for that processor before moving on with
execution. This result rolls up to the result of the parent section, so failing
a processor will also mark a Testcase as failed. Calling a result api from the
`section` object will apply that result to the section directly, instead of the
normal roll up behavior. For **pre-processors**, this will block the execution
of the section entirely, just setting the result instead. For
**post-processors**, this can override existing results occurring in that
section.

For example, result apis from either `processor` or `section` could declare a
section as failed with a **post-processor** even if it already passed.

.. code-block:: python

    def section_failed(section):
        section.failed()

    class Testcase(aetest.Testcase):

        @aetest.processors.post(section_failed)
        @aetest.test
        def test(self):
            pass
        # This test section would regularly pass, but the processor will cause
        # the result to be Failed

.. note::

    However, only the `section` apis could mark a failed section as passed,
    since this goes against :ref:`result_rollup`

There are some other ways to impact the section result with processors.
**Pre-processors** that return ``False``, will cause the section to be
``Skipped``, **pre-processors** that have an assertion failure will be
``Blocked``and **Exception-processors** that return ``True`` will suppress the
exception and prevent an ``Errored`` result.


Context Processors
------------------

Typical pre/post/exception-processors are just functions with a specific
purpose. **Context-processors**, on the other hand, are similar to Python's
`context managers`_ in the sense that they can handle the before, after, and
exceptions within a single class.

.. tip::

    think of a **context-processor** as pre + post + exception processor
    all-in-one

There are two methods of defining **context-processors**:

    1. by subclassing from ``aetest.processors.bases.BaseContextProcessor``

    2. using ``@aetest.processors.context`` decorator on a generator factory
       function.

.. code-block:: python

    # Example
    # -------
    #
    #   simple context processor example

    from pyats import aetest
    from pyats.aetest.processors.bases import BaseContextProcessor

    # define a context processor that:
    #   - print the section uid before testcase
    #   - prints the section result after testcase in normal conditions
    #   - prints the exception when an exception occurs

    class ContextProcessor(BaseContextProcessor):

        def __enter__(self):
            print('current section: ', self.section.uid)
            # can also access parameters
            testbed = self.parameters.get('testbed')

        def __exit__(self, type_, value, traceback):
            if type_:
                print('An exception occured!')
                print('exception : ', exc_type, exc_value)
            else:
                print('section result: ', self.section.result)

    # attach above context processor to a Testcase
    @aetest.processors(ContextProcessor)
    class Testcase(aetest.Testcase):

        @aetest.test
        def test(self):
            print('running testcase test section')

        @aetest.test
        def testException(self):
            raise Exception('running testcase testException section')

In essense, a basic, class-based **context-processor** is basically a Python
Context Manager, with its ``__enter__()`` called as the section
**pre-processor**, and ``__exit__()`` called as the
**post+exception-processor**. If an exception occurs, ``__exit__()`` is called
after the exception but before the section result is set, just like an
**exception-processor**. If no exception occurs, ``__exit__()`` is called later
after the exception is set, like a **post-processor**. Additionally, the result
apis are still available from the class itself. So a call of `self.failed()`
would be equivalent to `processor.failed()` in a **pre-processor**.

You can also opt to define generator-style **context-processors**, similar to
Python's ``contextlib.contextmanager`` functionality:

.. code-block:: python

    # Example
    # -------
    #
    #   simple context processor example using generator
    #   (same functionality as above)

    from pyats import aetest

    @aetest.processors.context
    def context_processor(section, processor):
        print('current section: ', section.uid)
        # accessing parameters
        testbed = processor.parameters.get('testbed')

        try:
            yield

        except Exception as e:
            print('An exception occurred!')
            print('exception : ', exc_type, exc_value)
            # we are not raising e, so it will be suppressed
        else:
            print('section result: ', section.result)


    # attach above context processor to a Testcase
    @aetest.processors(context_processor)
    class Testcase(aetest.Testcase):

        @aetest.test
        def test(self):
            print('running testcase test section')

        @aetest.test
        def testException(self):
            raise Exception('running testcase testException section')


.. tip::

    Generator-style **context-processors** do not return a boolean value to
    determine whether or not to suppress an exception. Instead, they suppress
    exceptions by default and must raise the same exception again in order to
    let it propagate.


.. _context managers: https://docs.python.org/3/library/stdtypes.html#typecontextmanager

.. _aetest_global_processors:

Global Processors
-----------------

In addition to the ability to attach processors to classes & sections, it is
also possible to define processors that run **globally**: before and after
each and every defined script section (common setup/cleanup, subsection,
testcases, setup/cleanup/tests), or on Exception_ occurance.

Global processors are no different than the ones affixed to each section using
the ``@processors`` decorator, except that they always run automatically. To
use global processors in your testscript, define a script-level dictionary named
``global_processors`` with ``pre``, ``post`` and ``exception`` as the keys, and
the values being a list of processor functions.

.. code-block:: text

    Global Processors Syntax
    ------------------------

        global_processors = {
            'pre': [list of global pre-processor objects],
            'post': [list of global post-processor objects],
            'exception': [list of global exception-processor objects],
            'context': [list of global context processor classes/functions]
        }

.. code-block:: python

    # Example
    # -------
    #
    #   script using global processors

    from pyats import aetest

    # define a function that prints the section's uid
    def print_uid(section):
        print('current section: ', section.uid)

    # define a function that prints the section result
    def print_result(section):
        print('section result: ', section.result)

    # define another function that prints the exception message and suppress the
    # exception
    def print_exception_message(section, exc_type, exc_value, exc_traceback):
        print('exception : ', exc_type, exc_value)
        return True

    # use the above functions global pre/post processors
    #   global pre-processor  : print_uid
    #   global post-processor : print_result
    #   global exception-processor : print_exception_message
    global_processors = {
        'pre': [print_uid,],
        'post': [print_result,],
        'exception': [print_exception_message,],
    }

    class Testcase(aetest.Testcase):

        @aetest.test
        def test(self):
            print('running testcase test section')

        @aetest.test
        def testException(self):
            pyATS()

    # script output
    #   - notice that the processors ran immediately before and after each
    #     section (testcase & test) execution.
    #   - note that section test result is null - because it hasn't been given
    #     a result by the executer yet.
    #
    #     +------------------------------------------------------------------------------+
    #     |                          Starting testcase Testcase                          |
    #     +------------------------------------------------------------------------------+
    # ->  Running pre-processor: 'print_uid'
    # ->  current section:  Testcase
    #     +------------------------------------------------------------------------------+
    #     |                            Starting section test                             |
    #     +------------------------------------------------------------------------------+
    # ->  Running pre-processor: 'print_uid'
    # ->  current section:  test
    #     running testcase test section
    # ->  Running post-processor: 'print_result'
    # ->  section result:  null
    #     The result of section test is => PASSED
    #     +------------------------------------------------------------------------------+
    #     |                        Starting section testException                        |
    #     +------------------------------------------------------------------------------+
    # ->  Running pre-processor: 'print_uid'
    # ->  current section:  testException
    #     Running exception-processor: 'print_exception_message'
    #     exception :  NameError name 'pyATS' is not defined
    #     section result:  null
    # ->  Running post-processor: 'print_result'
    # ->  section result:  null
    #     The result of section testException is => PASSED
    # ->  Running post-processor: 'print_result'
    # ->  section result:  passed
    #     The result of testcase Testcase is => PASSED

.. hint::

    global processors may be extremely useful in cases where you wish to run
    some functions before and after everything - for example, collecting
    code coverages (Cflow), and router healths (router health check), etc.


Runtime Behaviors
-----------------

The following rules describes the behavior of pre/post/exception processors when
defined.

- **pre-processors** are run immediately *before* test section execution

- **post-processors** are run immediately *after* test section execution

- **exception-processors** are run immediately *after* test section raised
  Exception_

  - **exception-processors** will be skipped if there is no Exceptions occurred
    during test section execution

- **context-processors** run before function-based processors. Eg:

  - before a section, any attached context-processor ``__enter__()`` will run
    before all other pre-processors

  - after a section, any attached context-processor's ``__exit__()`` will run,
    before all other exception processors and post-processors

- **global processors** are always run before local processors.

- if a processor requires an argument named ``section``, the current
  executing section is provided to that argument value.

  .. code-block:: python

      def processorFunc(section):
          pass

- while executing **pre-processor** functions or context-processor's
  ``__enter__()`` api, if any ``AssertionError`` is caught, or if the function
  returns ``False``, all remainining **pre-processor** and context-processors
  will be skipped, and the test section is skipped over with a
  result of ``Skipped``. All **post-processors** are also skipped. Otherwise,
  execution continues as originally scheduled.

  .. code-block:: python

      def preprocessorAssertionError():
          # assertion error causes all remaining pre-processors to be skipped
          # and the test section also receives a result of Skipped
          assert 'vim' is 'great'

      def preprocessorReturnFalse()
          # if a pre-processor returns False, all remaining pre-processors
          # are skipped, and the test section is skipped also.
          return False

- when returning ``False`` in **pre-processors** or context processor's
  ``__enter__()``, an optional *reason* message may also be returned. This is
  printed as the reason for skipping the current section in the log file.

  .. code-block:: python

      def preprocessorReturnFalseWithReason()
          # return false along with a reason (as a tuple)
          return False, "murphy's law :-("

- if any ``Exceptions`` are caught while executing processor functions, all
  remaining processors functions are skipped over, and the test section
  receives a result of ``Errored``. If that ``Exception`` occured within a
  **pre-processor**, the test section is skipped with a result of
  ``Errored``.

- if a section has any attached **exception-processors** or
  **context-processors**, any unhandled exception will be passed to the
  processor, with exception type, value and traceback.

  - in the case of generator-based context processors, the exception will be
    thrown into the generator using ``gen.throw()`` mechanism

- **exception-processors** will handle Exception_ in the following order:
  global, testcase, local.

- if any **exception-processors** or context-processor ``__exit__()`` returns
  ``True``, the Exception_ from executed test section will be suppressed.


.. note::

    **exception-processors** does not support AssertionError_ raised from
    :ref:`aetest_steps`. Other types of Exception_ raised from
    :ref:`aetest_steps` would be handled accordingly.

.. _AssertionError: https://docs.python.org/3.4/library/exceptions.html#AssertionError

Additional APIs
---------------

The list of pre/post/exception processors affixed to each test script section
can be dynamically accessed and queried during runtime, using the following
functions:

``processors.get(section, type_, incl_globals=False)``
    returns the list of pre/post/exception processors affixed to a section
    object. By default, get only returns the processors applied to that section.
    Using the ``incl_globals = True`` argument also includes current known
    global processors of that type.

    .. code-block:: python

        # Example
        # -------
        #
        #   processors.get function

        from pyats import aetest

        # create a global processor
        global_processors = dict(pre = [lambda: True])

        # testcase with two lambda functions as pre-processors
        @aetest.processors.pre(lambda: True, lambda: True)
        class Testcase(aetest.Testcase):
            pass


        aetest.processors.get(Testcase, type_ = 'pre')
        # [<function <lambda> at 0xf758e734>,
        #  <function <lambda> at 0xf769e0bc>]

        aetest.processors.get(Testcase, type_ = 'post')
        # []

        aetest.processors.get(Testcase, type_ = 'exception')
        # []

        aetest.processors.get(Testcase, type_ = 'pre', incl_globals = True)
        # [<function <lambda> at 0xf756b305>
        #  <function <lambda> at 0xf758e734>,
        #  <function <lambda> at 0xf769e0bc>]


``processors.affix(section, context = [], pre = [], post = [], exception = [])``
    dynamically affix pre/post/exception processors to a given section object.
    Any previously defined pre/post/exception/context processor functions are
    overwritten.

    .. code-block:: python

        # Example
        # -------
        #
        #   processors.add function

        from pyats import aetest

        # testcase with two lambda functions as pre-processors (false)
        @aetest.processors.pre(lambda: False, lambda: False)
        class Testcase(aetest.Testcase):
            pass

        # replace the two functions to Testcase
        aetest.processors.affix(Testcase, pre = [lambda: True, lambda: True])


``processors.add(section, context = [], pre = [], post = [], exception = [])``
    add more pre/post/exception/context processors to a given section object.
    This appends to the list of existing processors.

    .. code-block:: python

        # Example
        # -------
        #
        #   processors.add function

        from pyats import aetest

        class Testcase(aetest.Testcase):
            pass

        # add two lambda functions to Testcase as post-processors
        aetest.processors.add(Testcase, post = [lambda: True, lambda: True])


.. code-block:: python

    # Example
    # -------
    #
    #   using additional pre/post/exception processor APIs

    from pyats import aetest

    def print_parameters(section):
        print(section.parameters)

    def print_exception_message(section, exc_type, exc_value, exc_traceback):
        print('exception : ', exc_type, exc_value)
        return True

    class CommonSetup(aetest.CommonSetup):

        @aetest.subsection
        def subsection(self):
            # affix pre-processors and exception-processors to testcase
            aetest.processors.affix(Testcase, pre = [print_parameters],
                                    exception = [print_exception_message])

    class Testcase(aetest.Testcase):

        @aetest.setup
        def setup(self):
            # check if testcase has processors
            for type_ in ('pre', 'post', 'exception'):
                if aetest.processors.get(self, type_):
                    print('Testcase has %s-processors' % type_)

            # affix post-processors to test function
            aetest.processors.affix(self.test, post = [print_parameters])

            # affix exception-processors to testException function
            aetest.processors.affix(self.testException,
                                    exception = [print_exception_message])

        @aetest.test
        def test(self):
            pass

        @aetest.test
        def testException(self):
            pyATS()

    # the above example probably didn't make much sense.
    # the goal is to show you what can be done.


Reporting
---------

Processors dy default are not reported as sections of a test. This can be
changed using the :ref:`configuration <pyats_configuration>` option, or by using
the `processor.report` decorator on the processor function itself

.. code-block:: python

    @aetest.processors.report
    def my_post_processor(section):
        print(section.result)

Each processor appears as a child section of the Testcase/Test Section it is
being applied to, similar to adding another Test Section to a Testcase, or a
Step to a Test Section.

Even if reporting for a processor is disabled, any results raised will still be
propagated to the parent section, so the processor retains all functionality.