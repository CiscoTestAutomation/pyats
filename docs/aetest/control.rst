.. _aetest_control:

Flow Control
============

This section focuses on script execution control features offered in ``aetest``.

Control features allows users to master the flow of the testscript, performing
actions such as breaking the execution continuity and jumping ahead, skipping
or only executing specific testcases by ``uid``, grouping testcases together,
etc.

Control features described in this section are entirely *optional*.

.. _aetest_skip_conditions:


Skip Conditions
---------------

``aetest`` comes out-of-box with a few built-in **preprocessors** defined using
:ref:`aetest_processors` feature, intended to be used as shortcuts to skipping
test sections.

``@aetest.skip(reason = 'message')``
    unconditionally skip the decorated section. *reason* should describe why
    that section is being skipped.

``aetest.skip.affix(testcase, reason)``
    Same as the skip decorator, but can be used on the fly. So depending on one
    testcase result, the other testcases can be skipped.

``@aetest.skipIf(condition, reason = 'message')``
    skip the decorated test section if *condition* is ``True``.

``aetest.skipIf.affix(testcase, condition, reason)``
    It can be used to assign skipIf decorator to the testcases, condition can
    be a callable or a boolean.

``@aetest.skipUnless(condition, reason = 'message')``
    skip the decorated test section unless *condition* is ``True``.

``aetest.skipUnless.affix(testcase, condition, reason)``
    Can be used on the fly to assign decorators to the testcases

.. code-block:: python

    # Example
    # -------
    #
    #   skip/skipIf/skipUnless examples

    from pyats import aetest

    # skip testcase intentionally
    @aetest.skip('because we had to')
    class Testcase(aetest.Testcase):
        pass

    class TestcaseTwo(aetest.Testcase):

        # skip test section using if library version < some number
        @aetest.skipIf(mylibrary.__version__ < (1, 3),
                       'not supported in this library version')
        @aetest.test
        def test_one(self):
            pass

        # skip unless library version > some number
        @aetest.skipUnless(mylibrary.__version__ > (1, 3),
                           'not supported in this library version')
        @aetest.test
        def test_two(self):
            pass

        @aetest.test
        def test_three(self):
            aetest.skip.affix(section = TestcaseTwo.test_four,
                              reason = "message")
            aetest.skipIf.affix(section = TestcaseTwo.test_five,
                                condition = True,
                                reason = "message")
            aetest.skipUnless.affix(section = TestcaseThree,
                                    condition = False,
                                    reason = "message")

        @aetest.test
        def test_four(self):
            # will be skipped because of test_three
            pass

        @aetest.test
        def test_five(self):
            # will be skipped because of test_three
            pass

        @aetest.test
        def test_six(self):
            # will be skipped because of test_three
            pass

    class TestcaseThree(aetest.Testcase):
        # will be skipped because of TestcaseTwo.test_three
        pass

.. tip::

    the above skip decorators only support boolean conditions. Use the full
    :ref:`aetest_processors` feature if your skip condition are functions that
    requires access to ``section`` objects.


.. _aetest_uids:

Run IDS
-------

Run ``uids`` is the concept of only executing testcases & sections with uids
that matches up to a particular requirement. It provides users direct, finer
control before and during execution, over which sections to run, and which
sections to skip over.

There are two methods of providing ``aetest`` with this requirement:

    - through :ref:`aetest_standard_arguments` as part of script run arguments,
      or,

    - by setting :ref:`aetest_runtime` variable, ``runtime.uids`` dynamically
      during execution.

``uids`` accepts a python ``callable`` (eg, a function). The list of currently
running section uids are provided as inputs to this ``callable``, and if the
function evaluates to ``True``, the section is run, otherwise, the section is
not run and ignored completely so that it's not displayed in the report.

.. code-block:: python

    # Example
    # -------
    #
    #   setting from jobfile example

    from pyats.easypy import run

    # function determining whether we should run testcase_A
    # currently executing uids is always a list of:
    #       [ <container uid>, <section uid>]
    # eg, ['common_setup', 'subsection_one']
    # thus varargs (using *) is required for the function input.
    def run_only_testcase_A(*ids):
        # check that we are running testcase_A
        return 'testcase_A' in uids

    # run only testcase_A and its contents (using callable)
    # executing uids has testcase_A:
    run('example_script.py', uids = run_only_testcase_A)


The ``callable`` provided to ``uids`` feature is evaluated against the list of
current run ids, using varargs (eg, ``*uids``). This feature combined with
:ref:`logic_tests` objects can provide quite a bit of control over which
testcases to run and which not to.


.. code-block:: python

    # Example
    # -------
    #
    #   setting from jobfile example, using logics

    from pyats.easypy import run

    # import the logic objects
    from pyats.datastructures.logic import And, Or, Not

    # run the testscript with a bunch of logic involved
    # eg: both common_setup and common_cleanup,
    #     and all bgp and ospf non-sanity traffic tests.
    run('example_script.py', uids = Or('common_setup',
                                       And('^bgp.+', '.*traffic.*', Not('sanity')),
                                       And('^ospf.+', '.*traffic.*', Not('sanity')),
                                       'common_cleanup'))

    # or, when this testscript is run, call it with -uids argument
    #   python example.py -uids="Or('common_setup', \
    #                               And('^bgp.+', '.*traffic.*', Not('sanity')),\
    #                               And('^ospf.+', '.*traffic.*', Not('sanity')),\
    #                               'common_cleanup')"

Current ``uids`` requirements is stored and accessible using
:ref:`aetest_runtime` feature as ``runtime.uids``. This value is write enabled:
when dynamically set during runtime, it takes effect immediately starting
from the next section onwards.

.. code-block:: python

    # Example
    # -------
    #
    #   setting uids dynamically in testscript

    from pyats import aetest

    # using logics
    from pyats.datastructures.logic import Not, And

    class CommonSetup(aetest.CommonSetup):

        @aetest.subsection
        def subsection(self):

            # set uids dynamically during runtime
            # eg, run all tests with bgp in the name, but not traffic.
            aetest.runtime.uids = And('.*bgp.*', Not('traffic'))


If both methods of providing ``uids`` is used, then the engine first
starts up by following the list provided using
:ref:`aetest_standard_arguments`, until the :ref:`aetest_runtime` variable
``runtime.uids`` is updated.

.. _aetest_groups:

Testcase Grouping
-----------------

Testcase grouping feature enables testcases to be "associated" together by
certain keywords, allowing a testscript execution be limited to only running
testcases of one or more particular **groups** that matches up to input
criterion.

To use this feature, testcases needs to be labelled first with corresponding
groups by setting their ``groups`` attribute. By default, testscases do not
belong to any groups (``groups = []``).

.. code-block:: python

    # Example
    # -------
    #
    #   associating testcases to run groups

    # syntax
    #
    #   groups = [ <list of group names in str. no spaces> ]

    from pyats import aetest

    class Testcase(aetest.Testcase):

        # associating this testcase to 3 separate groups
        groups = ['group_A', 'group_B', 'group_C']

After labelling testcases to one or more groups, use one of the following
methods to control which testcase groups are run:

    - using :ref:`aetest_standard_arguments` ``-groups``, or,

    - by setting :ref:`aetest_runtime` variable, ``runtime.groups`` dynamically.

Like :ref:`aetest_uids` feature, ``groups`` also accepts a python ``callable``
(eg, a function). Each testcase's groups values are provided as inputs to this
``callable``, and if the return value is ``True``, the testcase is run.
Otherwise, the testcase is not run and ignored completely so that it's not
displayed in the report.

.. code-block:: python

    # Example
    # -------
    #
    #   setting groups from jobfile example

    from pyats.easypy import run

    # create a function that tests for testcase groups
    # this api tests that a testcase belongs to sanity but not traffic.
    # note that varargs (using *) is required, as the list of groups to each
    # testcase is unknown.
    def non_traffic_sanities(*groups):
        return 'sanity' in groups and 'traffic' not in groups

    # run the testscript by providing the above function to test groups
    run('example_script.py', groups = non_traffic_sanities)

    # --------------------------------------------------------------------------
    # behind the scenes (pseudo code)
    # for each testcase:
    #     if non_traffic_sanities(testcase.groups):
    #         run testcase
    #     else:
    #         pass

The ``callable`` provided to groups feature is evaluated against the list of
groups each testcase belongs to, using *varargs* (eg, ``*groups``). This feature
is intended to be used in conjunction with :ref:`logic_tests` objects.

.. code-block:: python

    # Example
    # -------
    #
    #   setting groups from jobfile example, using logics

    from pyats.easypy import run

    # import the logic objects
    from pyats.datastructures.logic import And, Not

    # same as above, run sanity non-traffic testcases
    run('example_script.py', groups = And('sanity', Not('traffic')))

    # or, from command line:
    # python example.py -groups="And('sanity', Not('traffic'))"


Similarly, ``groups`` can also be set dynamically during runtime:

.. code-block:: python

    # Example
    # -------
    #
    #   setting groups dynamically

    from pyats import aetest
    from pyats.datastructures.logic import And, Not

    class CommonSetup(aetest.CommonSetup):

        @aetest.subsection
        def subsection(self):

            # set groups dynamically during runtime
            aetest.runtime.groups = And('sanity', Not('traffic'))

And takes effect immediately.

Grouping feature is only applicable to testcases. In essence, the control of
whether testcases are run based on their grouping is handed entirely to the
user via boolean truth testing. Users can read the current executing groups
via :ref:`aetest_runtime` variable, and manipulate it based on a variety of
other factors, etc.

.. _aetest_requisite_testcase:

Requisite Testcase
------------------

Requisite testcase feature allows users to mark important testcases as
*must pass*: if such testcases failed, the current script execution is
aborted automatically by jumping forward to ``CommonCleanup`` section using
:ref:`aetest_goto`.

To mark testcases as *requisite* or *must pass*, set its attribute ``must_pass``
to ``True``. By default, no testcase is "requisite", eg, ``must_pass = False``.

.. code-block:: python

    # Example
    # -------
    #
    #   must_pass feature demonstration

    from pyats import aetest


    class TestcaseOne(aetest.Testcase):

        must_pass = True

        @aetest.test
        def test(self):
            self.failed('boom!')

    class TestcaseTwo(aetest.Testcase):
        pass

    class CommonCleanup(aetest.CommonCleanup)

        @aetest.subsection
        def subsection(self):
            pass

    # output result
    #
    #  SECTIONS/TESTCASES                                                RESULT
    # --------------------------------------------------------------------------
    #  .
    #  |-- TestcaseOne                                                   FAILED
    #  |   `-- test                                                      FAILED
    #  |-- TestcaseTwo                                                  BLOCKED
    #  `-- common_cleanup                                                PASSED
    #      `-- subsection                                                PASSED

.. note::

    the use of testcase ``must_pass`` flag does not imply testcase dependency
    It only marks a testcase as "critical" in terms of importance, where, if it
    failed then the rest of the execution should be abandoned.


.. _aetest_testcase_randomization:

Testcase Randomization
----------------------

Testcase randomization feature allows testcases within each testscript to be
executed in `pseudo-random`_ order. This allows for mixed script coverage
trails, yielding to better overall testing over time.

.. _pseudo-random: https://en.wikipedia.org/wiki/Pseudorandomness

By default, testcase randomization is turned off, and all testcases are executed
in the order described by :ref:`aetest_section_ordering`. To turn on
randomization, set :ref:`aetest_standard_arguments` ``random=True``. This
causes all testcases within the current testscript to be shuffled before
execution.

Normally, the system automatically picks a random integer value to seed the
python randomizer. This value is always printed in the log. This behavior can be
averted by setting the optional argument ``random_seed`` to a integer value,
fixing the outcome. This might be highly useful when trying to reproduce an
issue caused by a particular randomized testcase order: simply reuse the
seed value as shown in the logfile, and the same "randomized" order is
repeated.


.. code-block:: python

    # Example
    # -------
    #
    # randomization of testcases feature demonstration

    from pyats import aetest

    # define a couple testcases
    class TestcaseOne(aetest.Testcase):
        pass

    class TestcaseTwo(aetest.Testcase):
        pass

    class TestcaseThree(aetest.Testcase):
        pass

    # run it
    aetest.main(random = True)

    # output result
    #
    #  Testcase randomization is enabled, seed: 1461425170
    #
    #  SECTIONS/TESTCASES                                                RESULT
    # --------------------------------------------------------------------------
    #  .
    #  |-- TestcaseTwo                                                   PASSED
    #  |-- TestcaseOne                                                   PASSED
    #  `-- TestcaseThree                                                 PASSED

.. note::

    testcase randomization only affects the order of ``Testcases``.
    ``CommonSetup`` and ``CommonCleanup`` continue to run before and after
    all testcases, respectively.

.. tip::

    testcase randomization feature should be turned off before submitting
    testscript to regression.


.. _aetest_max_failures:

Maximum Failures
----------------

The maximum failures feature allows users to put a limit to the number of testcase
failures in a testscript before the script auto-aborts. This feature is intended to
safeguard against massive failures in long-running scripts, and avoids wasting
valuable testbed runtime when something goes horribly wrong.

To use this feature, set :ref:`aetest_standard_arguments` ``max_failures`` to an
integer value. During execution, if the total number of failed ``Testcases``
reaches the provided value, the script auto-aborts by jumping forward to
``CommonCleanup`` section using :ref:`aetest_goto`.

.. code-block:: python

    # Example
    # -------
    #
    # maximum failures feature demonstration

    from pyats import aetest

    class TestcaseOne(aetest.Testcase):

        @aetest.test
        def test(self):
            self.failed()

    class TestcaseTwo(aetest.Testcase):

        @aetest.test
        def test(self):
            self.failed()

    class TestcaseThree(aetest.Testcase):
        pass

    class CommonCleanup(aetest.CommonCleanup):
        pass

    # run it
    aetest.main(max_failures = 1)

    # output result
    #
    # Max failure reached: aborting script execution
    #
    #  SECTIONS/TESTCASES                                                RESULT
    # --------------------------------------------------------------------------
    #  .
    #  |-- TestcaseOne                                                   FAILED
    #  |-- TestcaseTwo                                                  BLOCKED
    #  |-- TestcaseThree                                                BLOCKED
    #  `-- common_cleanup                                                PASSED

As demonstrated above, when the total number of testcases failed reaches the
given value, the testscript is aborted with the remaining testcases blocked.


.. _aetest_goto:

Goto
----

`Goto`_ is the concept found in many programming languages that allows a
**one-way transfer** of control to another line of code. To this day, there are
still considerable debates with the academia and industry on its merits.

.. _Goto: http://en.wikipedia.org/wiki/Goto

``aetest`` supports the concept of *goto* on the simple basis that testscripts,
while still a piece of software, is mostly linear in execution & logic. Adding
to it the support for *goto* grants users a higher order of control, and enables
**early flow termination**: exiting out of current section and skipping ahead
for the sole purpose of saving execution/testbed time. This was born out of pure
necessity: router testing is a heavily time-consuming process, and any time
saving measures is a plus.

In ``aetest``, *goto jumps* can be invoked as optional arguments to
:ref:`result_apis`. This `keyword-only argument`_ accepts a list of **targets**
to jump to. Upon activation:

    1. the test engine jumps to and executes each listed **target** location
       in sequence.
    2. any by-passed sections receive a result based on the following
       criterion:

       a. if the section that initiated the jump has a result of ``Passed``, any
          by-passed section receives result ``Skipped``: eg, they were
          skipped over intentionally.

       b. if the section that initiated the jump has a result other than
          ``Passed``, any by-passed section receives result ``Blocked``: eg,
          they were blocked due to "x" reasons.

    3. after the **targets** list is exhausted, execution continues as
       normally expected.

.. important::

    ``aetest`` only allows **forward** jumping. All *goto* targets must be valid
    and in-line of current execution.

.. _keyword-only argument: https://www.python.org/dev/peps/pep-3102/

.. csv-table:: Available Goto Targets
    :header: Target, Comments
    :widths: 20, 80

    ``cleanup``, "jumps to the testcase cleanup section, by-passing all other
    test sections"
    ``next_tc``, "jumps to the next testcase in line"
    ``common_cleanup``, "jumps to the script's ``CommonCleanup`` section."
    ``exit``, "terminates the testscript immediately without going further."

If a goto target is invalid or does not exist, the test engine gives the
current section a result of ``Errored`` and continues executing. If there are no
more testcases, and goto ``next_tc`` is called, no error is given and
``common_cleanup`` is executed to finalize the testscript.

    *This is by design: make sure your goto targets actually exist.*

.. code-block:: python

    # Example
    # -------
    #
    #   goto syntax
    #   (pseudo code, not showing the entire testcase)

    from pyats import aetest

    # Syntax:
    #   <resultAPI>(goto = ['target_1', 'target_2', ... , 'target_x'])

    class CommonSetup(aetest.CommonSetup):
        @aetest.subsection
        def subsection(self):
            # goto with a message
            self.errored('setup error, abandoning script', goto = ['exit'])

    # --------------------------------------------------------------------------
    class TestcaseOne(aetest.Testcase):
        @aetest.setup
        def setup(self):
            # setup failed, go to cleanup of testcase
            self.failed('test failed', goto = ['cleanup'])

    # --------------------------------------------------------------------------
    class TestcaseTwo(aetest.Testcase):
        # test failed, move onto next testcase
        @aetest.test
        def test(self):
            self.failed(goto = ['next_tc'])

    # --------------------------------------------------------------------------
    class TestcaseThree(aetest.Testcase):
        @aetest.setup
        def setup(self):
            # setup failed, move onto cleanup of this testcase, then
            # jump to common_cleanup directly.
            self.failed(goto=['cleanup','common_cleanup'])


Essentially, **goto** is an optional step after providing a test section with an
appropriate result. For example, users may leverage this feature to skip to the
testcase's ``cleanup`` section after a dramatic failure in a ``test`` section,
or skip all testcases directly and go to ``common_cleanup`` instead. It allows
controlled skip-aheads during execution in favor of reducing script execution
time, avoiding expected errors/failures, etc.

.. code-block:: python

    # Example
    # -------
    #
    #   goto testscript demonstration

    from pyats import aetest

    # this testcase defines two tests
    # in the first test, we'll give it a result and
    # immediately skip forward to cleanup
    class Testcase(aetest.Testcase):

        @aetest.test
        def test_one(self):
            # skip ahead and go to cleanup instead
            self.passed(goto = ['cleanup'])

        @aetest.test
        def test_two(self):
            pass

        @aetest.cleanup
        def cleanup(self):
            pass

    # output result
    #
    #  SECTIONS/TESTCASES                                                RESULT
    # --------------------------------------------------------------------------
    #  .
    #  `-- Testcase                                                      PASSED
    #      |-- test_one                                                  PASSED
    #      |-- test_two                                                 SKIPPED
    #      `-- cleanup                                                   PASSED


.. _aetest_discovery_class:

Custom Discovery and Order
--------------------------

Normally, testcases are discovered by the default discovery class,
``ScriptDiscovery`` which is located under ``discovery`` module of ``aetest``
package. This class implements the default behavior of testcase discovery and
ordering discussed throughout this user guide. For example, ``common_setup`` has
to be run first, and then other testcases. Finally ``common_cleanup`` runs as
the last testcase of the script.

Advanced users may want to extend and enhance this built-in discovery mechanism,
eg, dynamic testcase/section generation, and/or alternative testcase ordering.

.. _aetest_custom_discovery:

Custom Discovery
^^^^^^^^^^^^^^^^

Users may overload discovery behavior at the following levels:

    - Script Discovery
    - Testcase Discovery
    - Common Discovery

.. note::

    **ScriptDiscovery** finds ``testcases`` within a ``testscript``.
    **TestcaseDiscovery** finds ``testsections`` within a ``testcase``
    **CommonDiscovery** finds ``subsections`` within a common section

Rules:

- **pyats.aetest.discovery.ScriptDiscovery** is the default discovery class
  for testcases and, it can be changed as shown in the following example:

.. code-block:: python

    from pyats.aetest import runtime
    runtime.discoverer.script = MyCustomScriptDiscovery

.. note::

    User defined custom script discovery class has to be inherited from
    `ScriptDiscovery<pyats.aetest.discovery.ScriptDiscovery>`

.. code-block:: python

    from pyats.aetest import runtime
    from pyats.aetest.discovery import ScriptDiscovery

    class MyCustomScriptDiscovery(ScriptDiscovery)
        pass

    runtime.discoverer.script = MyCustomScriptDiscovery

- **pyats.aetest.discovery.TestcaseDiscovery** is the default discovery class
  for testsections and, it can be changed as shown in the following example:

.. code-block:: python

    from pyats.aetest import runtime
    runtime.discoverer.testcase = MyCustomTestcaseDiscovery

.. note::

    User defined custom test discovery class has to be inherited from
    `TestcaseDiscovery<pyats.aetest.discovery.TestcaseDiscovery>`


.. code-block:: python

    from pyats.aetest import runtime
    from pyats.aetest.discovery import TestcaseDiscovery

    class MyCustomTestcaseDiscovery(TestcaseDiscovery)
        pass

    runtime.discoverer.testcase = MyCustomTestcaseDiscovery

- Using the ``runtime.discoverer`` properties sets the default discovery
  classes.

- As shown in the following example, It is possible to provide different
  discovery classes to different testcases by using the ``discoverer``
  attribute.

.. code-block:: python

    from pyats import aetest
    from pyats.aetest import runtime

    runtime.discoverer.testcase = MyDefaultDiscovery

    class my_testcase1(aetest.Testcase):
        discoverer = MyTestcaseDiscovery1

    class my_testcase2(aetest.Testcase):
        discoverer = MyTestcaseDiscovery2

    class my_testcase3(aetest.Testcase):
        pass

In the example above, ``my_testcase1`` uses ``MyTestcaseDiscovery1`` class,
``my_testcase2`` uses ``MyTestcaseDiscovery2`` and ``my_testcase3`` uses
``MyDefaultDiscovery`` class

- **pyats.aetest.discovery.CommonDiscovery** is the default discovery class for
  subsections and, it can be changed as shown in the following example:

.. code-block:: python

    from pyats.aetest import runtime
    runtime.discoverer.common = MyCustomCommonDiscovery

.. note::

    User defined custom common test discovery class has to be inherited from
    `CommonDiscovery<pyats.aetest.discovery.CommonDiscovery>`


.. code-block:: python

    from pyats.aetest import runtime
    from pyats.aetest.discovery import CommonDiscovery

    class MyCustomCommonDiscovery(CommonDiscovery)
        pass

    runtime.discoverer.common = MyCustomCommonDiscovery

- Using the ``runtime.discoverer`` properties sets the default discovery
  classes.

- As shown in the following example, It is possible to provide different
  discovery classes to different common sections by using the ``discoverer``
  attribute.

.. code-block:: python

    from pyats import aetest
    from pyats.aetest import runtime

    runtime.discoverer.common = MyDefaultDiscovery

    class common_setup(aetest.CommonSetup):
        pass

    class common_cleanup(aetest.CommonCleanup):
        discoverer = MyCommonDiscovery1

In the example above, ``common_cleanup`` uses ``MyCommonDiscovery1`` class,
and ``common_setup`` uses ``MyDefaultDiscovery`` class

How do discovery classes work?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are 3 main methods that users need to know.

1. ``discover()``
2. ``order()``
3. ``__iter__()``

Rules:

    - ``discover()`` method "discoveres" all child sections defined in the
      current target
    - ``order()`` method re-orders all sections according to rules of ordering
      and execution.
    - ``discover()`` always calls ``order()`` before it returns value
    - Finally, the result comes from the order is passed to the execution engine
    - Custom script discovery classes must be inherited from **ScriptDiscovery**
    - Custom testcase discovery classes must be inherited from
      **TestcaseDiscovery**
    - Custom common subsection discovery classes must be inherited from
      **CommonDiscovery**
    - Custom methods must follow the same structure with the default discovery
      methods
    - ``__init__`` method has to accept a parameter called ``target`` for
      all classes, containing the object to be discovered
    - ``__iter__`` method instantiates all child sections defined in the current
      target and makes discovery class instance `iterable`_.

.. _iterable: https://docs.python.org/3.4/glossary.html#term-iterable

**ScriptDiscovery Implementation**

.. code-block:: python

    class ScriptDiscovery():
        def __init__(self, target):
            self.target = target

        def __iter__(self):
            # some default logic written here
            ...
            for testcase in self.discover():
                yeild instantiated_testcase

        def discover(self):
            # some default logic written here
            ...
            return self.order(setup, testcases, cleanup)

        def order(self, setup=None, testcases=list(), cleanup=None):
            # some default logic written here
            ...
            return ordered_testcases

**TestcaseDiscovery Implementation**

.. code-block:: python

    class TestcaseDiscovery():
        def __init__(self, target):
            self.target = target

        def __iter__(self):
            # some default logic written here
            ...
            for test in self.discover():
                yeild instantiated_test

        def discover(self):
            # some default logic written here
            ...
            return self.order(setup, testcases, cleanup)

        def order(self, setup=None, tests=list(), cleanup=None):
            # some default logic written here
            ...
            return ordered_tests

**CommonDiscovery Implementation**

.. code-block:: python

    class CommonDiscovery():
        def __init__(self, target):
            self.target = target

        def __iter__(self):
            # some default logic written here
            ...
            for test in self.discover():
                yeild instantiated_test

        def discover(self):
            # some default logic written here
            ...
            return self.order(tests)

        def order(self, *sections):
            # some default logic written here
            ...
            return ordered_tests

**Custom Discovery Class Examples**

.. code-block:: python

    class MyCustomScriptDiscovery(ScriptDiscovery):
        def discover(self):
            # some logic
            return [self.target.module.tc_one, self.target.module.common_cleanup]

    class MyCustomTestcaseDiscovery(TestcaseDiscovery):
        def discover(self):
            #some logic
            return [self.target.my_section1]

    class MyCustomCommonDiscovery(CommonDiscovery):
        def discover(self):
            # some logic
            return [self.target.subsection1]

.. _aetest_custom_ordering:

Custom Ordering
^^^^^^^^^^^^^^^

There are 3 levels of custom ordering just like in the custom discovery,

1. Script Level
2. Testcase level
3. Common Level

In order to use **Script level ordering** a custom discovery class has to be
provided to the ``runtime.discoverer.script`` of ``aetest``. For more
information on how to provide a custom ScriptDiscovery class to the
``runtime.discoverer.script`` please refer :ref:`aetest_custom_discovery`

Rules:

    - Providing ``order`` method will replace the default ordering logic with
      the user defined one

.. code-block:: python

    class MyCustomScriptDiscovery(ScriptDiscovery):
        def order(self, setup=None, testcases=list(), cleanup=None):
            # some logic
            return [\
                self.module.common_setup,\
                self.module.tc_two,\
                self.module.tc_one,\
                self.module.common_cleanup]

Rules:

    - The rules that applies to the ``discover`` method also applies for
      ``order`` method as well.
    - ``discoverer`` attribute can be used in order to define ``testcase``
      specific discovery classes for testsections and subsections.
    - For more information about how to provide discovery classes, please
      check :ref:`aetest_custom_discovery`

.. code-block:: python

    class MyCustomTestcaseDiscovery(TestcaseDiscovery):
        def order(self, setup=None, tests=list(), cleanup=None):
            # some logic
            return [\
                self.target.common_setup,\
                self.target.tc_two,\
                self.target.tc_one,\
                self.target.common_cleanup]


.. code-block:: python

    class MyCustomCommonDiscovery(CommonDiscovery):
        def order(self, *sections):
            # some logic
            return [\
                self.target.subsection1,\
                self.target.subsection2]

Example
^^^^^^^

**Demonstration of how to provide custom Script, Testcase and Common Discovery
classes and how they work**


.. code-block:: python

    from pyats import aetest

    # importing the runtime to have access to the runtime.discoverer
    from pyats.aetest import runtime

    # importing ScriptDiscovery, TestcaseDiscovery and CommonDiscovery classes
    # for inheritance
    from pyats.aetest.discovery import ScriptDiscovery, TestcaseDiscovery,\
                                     CommonDiscovery

    # Custom Script Discovery class that changes only the discover method
    # which will return common_setup and tc_one
    class CustomScriptDiscovery(ScriptDiscovery):
        def discover(self):
            return [self.target.module.common_setup, self.target.module.tc_one]

    # Custom Testcase Discovery Class that changes both discover and order
    # classes. This class returns nothing from the discover method to the order
    # so, nothing will run in the provided tetscase
    class CustomTestcaseDiscovery_1(TestcaseDiscovery):
        def discover(self):
            return []

        def order(self, setup=None, testcases=list(), cleanup=None):
            if setup is not None:
                testcases.insert(0, setup)
            if cleanup is not None:
                testcases.append(cleanup)

            return testcases

    # Common Discovery Class that returns nothing to be run
    class CustomCommonDiscovery_1(CommonDiscovery):
        def discover(self):
            return []

        def order(self, *sections):
            return sections

    # Custom Common Discovery Class, order method returns sample_subsection_1
    # so it's the only test section that will run for the provided testcase
    class CustomCommonDiscovery_2(CommonDiscovery):
        def order(self, *sections):
            return [self.target.sample_subsection_1]

    # setting runtime.discoverer properties so that default discovery classes
    # will change to user defined ones.
    runtime.discoverer.script = CustomScriptDiscovery
    runtime.discoverer.testcase = CustomTestcaseDiscovery_1
    runtime.discoverer.common = CustomCommonDiscovery_1

    # This testcase has discoverer attribte so that, runtime.discoverer.common
    #  will be ignored
    class common_setup(aetest.CommonSetup):
        discoverer = CustomCommonDiscovery_2

        @aetest.subsection
        def sample_subsection_1(self):
            pass

        @aetest.subsection
        def sample_subsection_2(self, section):
            pass

    class tc_one(aetest.Testcase):

        @aetest.setup
        def prepare_testcase(self, section):
            pass

        @ aetest.test
        def simple_test_1(self):
            pass

        @ aetest.test
        def simple_test_2(self):
            pass

        @aetest.cleanup
        def clean_testcase(self):
            pass

    class common_cleanup(aetest.CommonCleanup):
        @aetest.subsection
        def clean_everything(self):
            pass


In this example, ``CustomScriptDiscovery`` class was passed as the default
discovery class to the ``runtime.discoverer.script``. It only has ``discover``
method and this method returns only ``common_setup`` and ``tc_one``. Therefore,
only these 2 testcases runs.

``CustomTestDiscovery_1`` class was also provided as default testcase discovery
class so all the testcases within this script is going to use this class unless
there is ``discoverer`` parameter is provided. Nothing should be run as it
doesn't return any test section.

``CustomCommonDiscovery_1`` class was also provided as default common discovery
class so all the common sections within this script is going to use this class
unless there is ``discoverer`` parameter is provided like in ``common_setup``.
The output of ``order`` and ``discover`` calls from this class will return empty
list. So, none of the testcases, should run any testsection except
``common_setup``

``discoverer`` was provided within the ``common_setup`` section so, this
parameter will be applied over ``runtime.discoverer.commmon`` for this section.
``CustomCommonDiscovery_2`` class was used and it returns only
``sample_subsection_1``.

**Output**

.. code-block:: text

    %EASYPY-INFO: +------------------------------------------------------------------------------+
    %EASYPY-INFO: |                             Task Result Details                              |
    %EASYPY-INFO: +------------------------------------------------------------------------------+
    %EASYPY-INFO: Task-1: basic_example_script
    %EASYPY-INFO: |-- commonSetup                                                           PASSED
    %EASYPY-INFO: |   `-- sample_subsection_1                                               PASSED
    %EASYPY-INFO: `-- tc_one                                                                PASSED
