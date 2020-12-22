.. _aetest_steps:

Section Steps
=============

.. sidebar:: Helpful Reading

    - `Context Manager`_
    - `The with statement`_

.. _Context Manager: https://docs.python.org/3.4/reference/datamodel.html#context-managers
.. _The with statement: https://docs.python.org/3.4/reference/compound_stmts.html#the-with-statement


In ``aetest``, testscripts are naturally broken down into ``TestContainers``
and ``TestFunctions``, two-level segments defined in :ref:`object_model`. For
example:

    - ``CommonSetup``: ``subsection``
    - ``Testcase``: ``setup``/``test``/``cleanup``

This two-level approach is mostly sufficient when sections can be kept short &
independent. However, often times, there's a need for larger, longer sections,
mostly due to nature of the tests being carried out. In these situations, users
can leverage the optional section ``Steps`` feature: slicing down large
sections into groups of smaller, more granular linear actions that sums up
towards the same testing goal.


Defining Steps
--------------

To divide sections into smaller steps, define section methods with the
:ref:`reserved_parameters` ``steps`` in its function arguments. This enables
steps creation by bringing ``Steps`` class instance into the local method scope.

Each step is started by calling ``steps.start()``, and providing it a short
descriptive name for that new step. A longer description can also be provided,
which will be included in the final report. The returned :ref:`step_object` is a
python `Context Manager`_, intended to be consumed by the ``with`` statement.

.. code-block:: python

    # Example
    # -------
    #
    #   breaking a test section into smaller steps

    from pyats import aetest

    # using a testcase as example
    # applies to all sections (subsection/setup/cleanup/test)
    class NeilArmstrong(aetest.Testcase):

        # define section method with 'steps' reserved parameter argument
        # this enables the engine to pass steps object to the local scope
        @aetest.test
        def says(self, steps):

            # breaking down this test into two steps
            # using python "with" statement and steps parameter
            with steps.start('first step',
                             description = 'this is the first step'):
                print('one small step for [a] man')

            with steps.start('second step',
                             description = 'this is the second step'):
                print('one giant leap for mankind')

    # script output
    #
    #   +------------------------------------------------------------------------------+
    #   |                            Starting section says                             |
    #   +------------------------------------------------------------------------------+
    #   +..............................................................................+
    #   :                              STEP 1: first step                              :
    #   +..............................................................................+
    #   one small step for [a] man
    #   The result of STEP 1: first step is => PASSED
    #   +..............................................................................+
    #   :                             STEP 2: second step                              :
    #   +..............................................................................+
    #   one giant leap for mankind
    #   The result of STEP 2: second step is => PASSED
    #   +----------------------------------------------------------+
    #   |                       STEPS Report                       |
    #   +----------------------------------------------------------+
    #   STEP 1 - first step                                   Passed
    #   STEP 2 - second step                                  Passed
    #   ------------------------------------------------------------
    #   The result of section says is => PASSED

The usage of `Context Manager`_ allows each step's code to properly nest under
its own indentation block, allows the test infrastructure to identify each
step's boundaries, and allows independent error catching & result handling etc.

In addition, this returned :ref:`step_object` can be stored into variable using
``as`` statement, allowing users to access/refer to current step information,
and make calls to result apis:

.. code-block:: python

    # Example
    # -------
    #
    #   referring to the step object

    from pyats import aetest

    class Testcase(aetest.Testcase):

        @aetest.test
        def test(self, steps):

            # create step into 'step' variable
            with steps.start('the first step') as step:
                # eg, each step is automatically assigned a unique,
                # numeric index number, and can be accessed using the
                # "index" attribute.
                print('Current step index: ', step.index)
                # Current step index: 1


Step Results
------------

Each step comes with its own result, represented using :ref:`result_objects`.
When a script section is segmented using steps feature, that section's result is
calculated using the combined roll-up results of all its contained steps.

All other step result behaviors are identical to its parent
:ref:`aetest_section_results`:

    - the default result for all steps is ``Passed``

    - ``AssertionError``: AssertionError_ exceptions corresponds to ``Failed``

    - ``Exception``: Exceptions_ corresponds to ``Errored``

.. _AssertionError: https://docs.python.org/3.4/library/exceptions.html#AssertionError
.. _Exceptions: https://docs.python.org/3.4/library/exceptions.html


.. code-block:: python

    # Example
    # -------
    #
    #   step results default

    from pyats import aetest

    class Testcase(aetest.Testcase):

        @aetest.test
        def test_one(self, steps):

            # default step result -> Passed
            with steps.start('the passed step'):
                pass

            # AssertionErrors -> Failed
            with steps.start('the failed step'):
                assert 1 == 0

        @aetest.test
        def test_two(self, steps):

            # general Exceptions -> Errored
            with steps.start('the errored step'):
                # generate a python error
                {}['non existent key']

    # script output
    #   note that the result of each test section is the
    #   combined roll-up of its steps. Eg:
    #       test_one: Passed + Failed -> Failed
    #       test_two: Errored         -> Errored
    #
    #   +------------------------------------------------------------------------------+
    #   |                          Starting testcase Testcase                          |
    #   +------------------------------------------------------------------------------+
    #   +------------------------------------------------------------------------------+
    #   |                          Starting section test_one                           |
    #   +------------------------------------------------------------------------------+
    #   +..............................................................................+
    #   :                       Starting STEP 1: the passed step                       :
    #   +..............................................................................+
    #   The result of STEP 1: the passed step is => PASSED
    #   +..............................................................................+
    #   :                       Starting STEP 2: the failed step                       :
    #   +..............................................................................+
    #   An assertion error was caught during step:
    #   Traceback (most recent call last):
    #   File "example.py", line 14, in test_one
    #       assert 1 == 0
    #   AssertionError
    #   The result of STEP 2: the failed step is => FAILED
    #   +----------------------------------------------------------+
    #   |                       STEPS Report                       |
    #   +----------------------------------------------------------+
    #   STEP 1 - the passed step                              Passed
    #   STEP 2 - the failed step                              Failed
    #   ------------------------------------------------------------
    #   The result of section test_one is => FAILED
    #   +------------------------------------------------------------------------------+
    #   |                          Starting section test_two                           |
    #   +------------------------------------------------------------------------------+
    #   +..............................................................................+
    #   :                      Starting STEP 1: the errored step                       :
    #   +..............................................................................+
    #   The result of STEP 1: the errored step is => ERRORED
    #   Caught exception during execution:
    #   Traceback (most recent call last):
    #   File "example.py", line 22, in test_two
    #       {}['non existent key']
    #   KeyError: 'non existent key'
    #   +----------------------------------------------------------+
    #   |                       STEPS Report                       |
    #   +----------------------------------------------------------+
    #   STEP 1 - the errored step                            Errored
    #   ------------------------------------------------------------
    #   The result of section test_two is => ERRORED
    #   The result of testcase Testcase is => ERRORED
    #   +----------------------------------------------------------------------+
    #   |                            Detailed Results                          |
    #   +----------------------------------------------------------------------+
    #    SECTIONS/TESTCASES                                              RESULT
    #   ------------------------------------------------------------------------
    #    .
    #    `-- Testcase                                                   ERRORED
    #        |-- test_one                                                FAILED
    #        |   |-- Step 1: the passed step                             PASSED
    #        |   |-- Step 2: the failed step                             PASSED
    #        `-- test_two                                               ERRORED
    #            `-- Step 1: the errored step                           ERRORED


In addition, the :ref:`step_object` also offers result APIs to that enables
manual assignment of results to each step. Note that these APIs only affect the
current step's result, and do not have :ref:`aetest_goto` support.

    - ``Step.passed(reason)``
    - ``Step.failed(reason)``
    - ``Step.errored(reason)``
    - ``Step.skipped(reason)``
    - ``Step.blocked(reason)``
    - ``Step.aborted(reason)``
    - ``Step.passx(reason)``

.. code-block:: python

    # Example
    # -------
    #
    #   step result APIs

    from pyats import aetest

    class Testcase(aetest.Testcase):

        @aetest.test
        def test_one(self, steps):

            with steps.start('the passed step') as step:
                # manually provide Passed result
                step.passed('because i want to')

            with steps.start('the failed step') as step:
                # manually provide Failed result
                step.failed('because i had to')

By default, when a step's result is not ``Passed``, ``Passx``, or ``Skipped``,
all remaining steps are avoided and the engine terminates the current test
section immediately to achieve time-savings. This behavior can be avoided by
providing ``continue_ = True`` to ``steps.start()``.

.. code-block:: python

    # Example
    # -------
    #
    #   step continuation feature

    from pyats import aetest

    class Testcase(aetest.Testcase):

        # test section that immediately returns after the first step failure
        @aetest.test
        def test_stopped_due_to_step_failure(self, steps):

            with steps.start('the failed first step'):
                # intentionally cause a failure
                assert 1 == 0

            with steps.start('the step after failed step'):
                # do nothing - this would normally be Passed
                pass

        # same test content/steps, but using continue_ = True
        @aetest.test
        def test_continues_after_step_failure(self, steps):

            with steps.start('the failed first step', continue_ = True):
                # intentionally cause a failure
                assert 1 == 0

            with steps.start('the step after failed step'):
                # do nothing - this would normally be Passed
                pass

    # output of script:
    #    note that even though both test failed, the 2nd test ran both steps
    #    because we used continue_ = True to override the default quick-exit
    #    behavior
    #
    #     +------------------------------------------------------------------------------+
    #     |              Starting section test_stopped_due_to_step_failure               |
    #     +------------------------------------------------------------------------------+
    #     +..............................................................................+
    #     :                    Starting STEP 1: the failed first step                    :
    #     +..............................................................................+
    #     An assertion error was caught during step:
    #     Traceback (most recent call last):
    #       File "example.py", line 10, in test_stopped_due_to_step_failure
    #         assert 1 == 0
    #     AssertionError
    #     The result of STEP 1: the failed first step is => FAILED
    #     +----------------------------------------------------------+
    #     |                       STEPS Report                       |
    #     +----------------------------------------------------------+
    #     STEP 1 - the failed first step                        Failed
    #     ------------------------------------------------------------
    #     The result of section test_stopped_due_to_step_failure is => FAILED
    #     +------------------------------------------------------------------------------+
    #     |              Starting section test_continues_after_step_failure              |
    #     +------------------------------------------------------------------------------+
    #     +..............................................................................+
    #     :                    Starting STEP 1: the failed first step                    :
    #     +..............................................................................+
    #     An assertion error was caught during step:
    #     Traceback (most recent call last):
    #       File "example.py", line 21, in test_continues_after_step_failure
    #         assert 1 == 0
    #     AssertionError
    #     The result of STEP 1: the failed first step is => FAILED
    #     +..............................................................................+
    #     :                 Starting STEP 2: the step after failed step                  :
    #     +..............................................................................+
    #     The result of STEP 2: the step after failed step is => PASSED
    #     +----------------------------------------------------------+
    #     |                       STEPS Report                       |
    #     +----------------------------------------------------------+
    #     STEP 1 - the failed first step                        Failed
    #     STEP 2 - the step after failed step                   Passed
    #     ------------------------------------------------------------
    #     The result of section test_continues_after_step_failure is => FAILED

.. note::

    ``continue`` is a python reserved keyword. Following PEP8_, the convention
    is to add a trailing underscore: ``continue_``.

.. _PEP8: https://www.python.org/dev/peps/pep-0008/


Nesting Steps
-------------

Steps can be nested. If a new step is started before the current one finishes,
it is called a *child* step of the current step. The ``.`` separator separates
child indexes from the parent index. Nesting steps provides better visual
references & finer granuarity to the steps breakdown.

Nested step results follow the standard rollup rule: each step's result is the
combined roll-up result of its immediate child steps.

.. code-block:: python

    # Example
    # -------
    #
    #   step nesting example
    #   (using a function for demonstration)

    from pyats import aetest

    # import Steps
    from pyats.aetest.steps import Steps

    # defining a function that support child steps.
    # use Steps() as default value for steps, in case the function is called
    # outside the scope of a testscript.
    def myFunction(steps = Steps()):
        with steps.start('function step one'):
            pass
        with steps.start('function step two'):
            pass

    class Testcase(aetest.Testcase):

        @aetest.test
        def test(self, steps):

            # demonstrating a step with multiple child steps
            with steps.start('test step 1') as step:
                with step.start('test step 1 substep a'):
                    pass
                with step.start('test step 1 substep a') as substep:
                    with substep.start('test step 1 sub-step a sub-substep i'):
                        pass
                    with substep.start('test step 1 sub-step a sub-substep ii'):
                        pass

            # demonstrating a step where a function is called, and
            # the function it self takes a few child steps to complete
            with steps.start('call function step') as step:
                # call the function, pass current step into it
                myFunction(step)

    # example output:
    #
    #     +----------------------------------------------------------+
    #     |                       STEPS Report                       |
    #     +----------------------------------------------------------+
    #     STEP 1 - test step 1                                  Passed
    #     STEP 1.1 - test step 1 substep a                      Passed
    #     STEP 1.2 - test step 1 substep a                      Passed
    #     STEP 1.2.1 - test step 1 sub-step a sub-substep i     Passed
    #     STEP 1.2.2 - test step 1 sub-step a sub-substep ii    Passed
    #     STEP 2 - call function step                           Passed
    #     STEP 2.1 - function step one                          Passed
    #     STEP 2.2 - function step two                          Passed
    #     ------------------------------------------------------------


Details & Report
----------------

When steps are created within script sections, a *STEPS Report* is always logged
at the end of that section. This provides visual details in the log file on
**all** steps taken during this section, their names and corresponding results.

This information can also be accessed during runtime using steps attributes:

``report()``
    generate the same steps report based on the current step and all of its
    child steps. This allows users to generate a sliced view the whole picture.

``details``
    *read-only* property, returns a list of ``StepDetail`` namedtuple_ objects,
    listing out the current step and all of its child step information. Each
    ``StepDetail`` contains the following:

        - ``index`` - step index string
        - ``name`` - step name
        - ``result`` - step result

.. _namedtuple: https://docs.python.org/3.4/library/collections.html#collections.namedtuple

.. code-block:: python

    # Example
    # -------
    #
    #   accessing step details & localized reports

    from pyats import aetest

    # import Steps
    from pyats.aetest.steps import Steps

    class Testcase(aetest.Testcase):

        @aetest.test
        def test(self, steps):

            # creating a step monster
            with steps.start('test step 1') as step:
                with step.start('test step 1 substep a'):
                    pass
                with step.start('test step 1 substep a') as substep:
                    with substep.start('test step 1 sub-step a sub-substep i'):
                        pass
                    with substep.start('test step 1 sub-step a sub-substep ii'):
                        pass

                    # access local step information/report
                    print(substep.details)
                    substep.report()

            # access overall step details:
            print(steps.details)

    # output of example
    #    note the StepDetails printout, and the first STEPS Report (on substep)
    #
    #    +------------------------------------------------------------------------------+
    #    |                            Starting section test                             |
    #    +------------------------------------------------------------------------------+
    #    +..............................................................................+
    #    :                         Starting STEP 1: test step 1                         :
    #    +..............................................................................+
    #    +..............................................................................+
    #    :                   Starting STEP 1.1: test step 1 substep a                   :
    #    +..............................................................................+
    #    The result of STEP 1.1: test step 1 substep a is => PASSED
    #    +..............................................................................+
    #    :                   Starting STEP 1.2: test step 1 substep a                   :
    #    +..............................................................................+
    #    +..............................................................................+
    #    :          Starting STEP 1.2.1: test step 1 sub-step a sub-substep i           :
    #    +..............................................................................+
    #    The result of STEP 1.2.1: test step 1 sub-step a sub-substep i is => PASSED
    #    +..............................................................................+
    #    :          Starting STEP 1.2.2: test step 1 sub-step a sub-substep ii          :
    #    +..............................................................................+
    #    The result of STEP 1.2.2: test step 1 sub-step a sub-substep ii is => PASSED
    # -> [StepDetail(index='1.2', name='test step 1 substep a', result=Passed),
    # ->  StepDetail(index='1.2.1', name='test step 1 sub-step a sub-substep i', result=Passed),
    # ->  StepDetail(index='1.2.2', name='test step 1 sub-step a sub-substep ii', result=Passed)]
    #    +----------------------------------------------------------+
    #    |                       STEPS Report                       |
    #    +----------------------------------------------------------+
    #    STEP 1.2 - test step 1 substep a                      Passed
    #    STEP 1.2.1 - test step 1 sub-step a sub-substep i     Passed
    #    STEP 1.2.2 - test step 1 sub-step a sub-substep ii    Passed
    #    ------------------------------------------------------------
    #    The result of STEP 1.2: test step 1 substep a is => PASSED
    #    The result of STEP 1: test step 1 is => PASSED
    # -> [StepDetail(index='1', name='test step 1', result=Passed),
    # ->  StepDetail(index='1.1', name='test step 1 substep a', result=Passed),
    # ->  StepDetail(index='1.2', name='test step 1 substep a', result=Passed),
    # ->  StepDetail(index='1.2.1', name='test step 1 sub-step a sub-substep i', result=Passed),
    # ->  StepDetail(index='1.2.2', name='test step 1 sub-step a sub-substep ii', result=Passed)]
    #    +----------------------------------------------------------+
    #    |                       STEPS Report                       |
    #    +----------------------------------------------------------+
    #    STEP 1 - test step 1                                  Passed
    #    STEP 1.1 - test step 1 substep a                      Passed
    #    STEP 1.2 - test step 1 substep a                      Passed
    #    STEP 1.2.1 - test step 1 sub-step a sub-substep i     Passed
    #    STEP 1.2.2 - test step 1 sub-step a sub-substep ii    Passed
    #    ------------------------------------------------------------


Step Debugging
--------------

Step debugging is an optional value-add to steps. It allows the user to send
cli commands to currently connected testbed devices and/or run custom debugging
functions before and after each step, without modifying the testscript.

To use step debugging, a *step debug input file* (in YAML_ format) needs to be
provided to ``aetest``. The content of this file specifies where during script
execution & what clis to send to which testbed devices and which functions to
run.

.. _YAML: http://www.yaml.org/spec/1.2/spec.html

.. code-block:: yaml

    # Schema
    # -------
    #
    # step debug input file

    extends:    # Step debug file(s) to extend/build on.
                # Use this field to extend an existing yaml step debug file,
                # allowing you to create an inheritance hierarchy.
                # Supports full path/names or name of file in the same dir.
                # The content of the last file on the list forms the base and
                # is updated with the preceding file, and so on,
                # until the existing file content is updated last.
                # (optional)

    <step_name>:  # A regular expression of the step name
        - when:   # A list that is consist of 'start', 'end' or any result type,
                  # like 'passed'
                  # (mandatory)
          device: # List of devices that will be passed to the functions and
                  # will run the commands.
                  # (mandatory)
          cmd:    # List of cli commands to be run on devices,
                  # (optional)
          func:   # Functions list,
                  # (optional)

.. code-block:: yaml

    # Example
    # -------
    #
    # step debug input file

    step.*:

        - when:
            - 'start'
            - 'failed'

          device:
            - 'device.*'

          cmd:
            - 'mycommand1'
            - 'my_command2'

          func:
            - 'path.to.myscript.myfunction1'
            - 'path.to.myscript.myfunction2'


        - when:
            - 'end'

          device:
            - 'device1'

          cmd:
            - 'my_command'

          func:
            - 'path.to.myscript.myfunction1'


In essence, the step debug engine matches the following items:

    - the current step name as a regular expression

    - a particular action:

      - when encountering a result type using keyword in ``when``, for example:
        ``when('failed')``

      - before/after the step using action keyword "start", "end"
        ``when("start", "end")``

and sends a list of cli commands to the given devices. The output of each
command (regardless of error) is then logged to log file for debugging purposes.
Also, users can provide functions/callables to run with the ``func`` keyword.

The step debug YAML file is provided to ``aetest`` execution using the
:ref:`aetest_standard_arguments` ``-step_debug``. Upon the start of execution,
the input file is loaded & parsed. If there is a missing information in this
file that is mandatory, an exception is thrown. If there are some wrong
information in the file such as wrong device name or step name, it is just
ignored.

.. code-block:: text

    # standalone execution example
    python my_testscript.py -step_debug /path/to/my/stepDebugInput.yaml

Due to the string matching nature of step debug engine, `regular expressions`_
are supported for step names and device names.

About the keys:

    - ``when`` and ``device`` keys are mandatory in the step debug file. ``cmd``
      and ``func`` are optional and can be provided together.

    - If ``cmd`` and ``func`` are provided together, the cli commands are first
      executed in turn on matching devices and only then are the functions are
      called on each device in turn.

    - "func" parameter is not limited to just functions, it actually accepts any
      kind of python callable object(such as classes).

.. important::

    When a function is provided there are 3 keywords that step debug engine is
    using. If function accepts "section" variable, engine sends the current
    section object to the function, if "step" is defined then the current step
    object will also be sent. All of the matching devices are passed to the
    function one by one, if there is "device" within the function parameters.

    If there is a kwargs in the parameters of the function then all of the 3
    parameters above will be passed via kwargs.

.. _regular expressions: http://www.regular-expressions.info/tutorial.html

--------------------------------------------------------------------------------

.. _step_object:

Step Objects
------------

Step feature is internally implemented using two classes:

``Steps``
    base container class, containing one or more ``Step``. Allows the creation,
    reporting and handling of more steps within. The ``steps`` parameter
    passed to each section function is an instance of this class.

.. code-block:: text

    +--------------------------------------------------------------------------+
    | Steps                                                                    |
    +==========================================================================+
    | attribute       | description                                            |
    |-----------------+--------------------------------------------------------|
    | start           | starts a new step. returns Step instance               |
    | result          | roll-up result of all steps contained                  |
    | report          | reports current step details/results to log file       |
    | steps           | list of Step objects representing each step taken      |
    +==========================================================================+
    | properties      | description                                            |
    |-----------------+--------------------------------------------------------|
    | details         | list of steps details using StepDetail namedtuple      |
    +--------------------------------------------------------------------------+


``Step``
    extends the base ``Steps`` class. ``Step`` is a `Context Manager`_, intended
    to be used in conjunction with python ``with`` statement. This is the
    workhorse class that offers:

        - result apis: manually providing results to each step
        - error/exception handling: assigns corresponding results to the current
          step in case of abnormality.
        - continue on fail (``continue_``) feature
        - etc.

    Inheriting base class ``Steps`` enables steps nesting.

.. code-block:: text

    +--------------------------------------------------------------------------+
    | Step  (basecls: Steps)                                                   |
    +==========================================================================+
    | attribute       | description                                            |
    |-----------------+--------------------------------------------------------|
    | start           | starts a new child step. returns Step instance         |
    | result          | roll-up result of this step and all child steps ned    |
    | report          | reports current step details/results to log file       |
    | steps           | list of child Step objects                             |
    | description     | description of this step instance                      |
    +==========================================================================+
    | properties      | description                                            |
    |-----------------+--------------------------------------------------------|
    | details         | list of steps details using StepDetail namedtuple      |
    +==========================================================================+
    | result apis     | description                                            |
    |-----------------+--------------------------------------------------------|
    | passed          | provides passed result to this step                    |
    | failed          | provides failed result to this step                    |
    | aborted         | provides aborted result to this step                   |
    | blocked         | provides blocked result to this step                   |
    | skipped         | provides skipped result to this step                   |
    | errored         | provides errored result to this step                   |
    | passx           | provides passx result to this step                     |
    +==========================================================================+
    | built-in        | description                                            |
    |-----------------+--------------------------------------------------------|
    | __enter__       | method called with starting step through with statement|
    | __exit__        | method called with exiting step through with statement |
    +--------------------------------------------------------------------------+

.. note::

    the above is for reference only. Do not modify internals during runtime.

.. hint::

    intentionally modifying non-passing results to ``Passed`` is cheating. May
    be considered a C.L.M.

