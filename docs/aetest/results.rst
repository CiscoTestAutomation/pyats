.. _aetest_section_results:

Section Results
===============

.. sidebar:: Helpful Reading

    - :ref:`result_objects`

    - :ref:`object_model`

    - `Errors and Exceptions`_

    - `Built-in Exceptions`_

.. _Errors and Exceptions: https://docs.python.org/3.4/tutorial/errors.html
.. _Built-in Exceptions: https://docs.python.org/3.4/library/exceptions.html#bltin-exceptions

*The outcome of all testing is some form of results.* This section thus explores
topics such as how results are propagated & stored internally in ``aetest``, how
exceptions are handled, and how users may override the default result reporting
behavior.

Internally in ``aetest``, all results are collected, rolled-up and reported
using :ref:`result_objects`. The following summarizes this behavior:

* all script section have a ``result`` attribute, storing its current
  result using the corresponding result object (see :ref:`object_model`).

* ``TestContainer`` section's ``result`` attribute represents the combined
  roll-up of all of its child section results. Eg, common setup's ``result``
  attribute stores the current combined rolled-up result of all of its
  subsections that ran so far.

Result Behavior
---------------

    *Ei incumbit probatio qui dicit, non qui negat. (Latin)*

The default result for all sections is ``Passed``, even if no meaningful actions
and/or testings were carried out. Think of this as: even though a test that
assesses nothing is a terrible test, running it still yields a "passing" grade.
Do not mix-up the usefulness/meaningfulness of a test with the result of its
testing. This behavior is inline with all other Python test infrastructures.

.. code-block:: python

    # Example
    # -------
    #
    #   default section result is always Passed

    from pyats import aetest

    # this testcase is entirely empty
    class Testcase(aetest.Testcase):
        pass


    # but if we instantiate this testcase and run it
    # we get Passed, even though it did nothing.
    tc = Testcase()
    tc()
    # Passed

When python Exceptions_ are raised during the execution of any test sections and
are caught by the ``aetest`` infrastructure, depending on the type of exception,
a corresponding result is assigned to that running section:

    - ``AssertionError``: AssertionError_ exceptions and all of its subclasses
      corresponds to section result ``Failed``, indicating a failed assertion
      test.

      Example: the test code is using ``assert`` statement to perform a
      check/test, and the exception is raised as a result of the failed
      assertion.

    - ``Exception``: Exception_ and all of its subclasses corresponds to section
      result ``Errored``, indicating of occurance of an un-handled test-code
      error.

      Example: a ``KeyError`` exception is raised when the script is accessing
      a dictionary key that does not exist.

.. code-block:: python

    # Example
    # -------
    #
    #   demonstrating exception result behaviors

    from pyats import aetest

    class Testcase(aetest.Testcase):

        # defining a test that raises a python exception
        # the expected behavior is test Errored
        @aetest.test
        def test_one(self):
            # creating an empty dictionary and accessing a key
            # that does not exist raises KeyError Exception
            {}['key does not exist']

        # defining a test that raises an AssertionError
        # the expected behavior is test Failed
        @aetest.test
        def test_two(self):
            # do an assertion that fails.
            assert 1 == 0, "unfortunately 1 doesn't equal to 0"

    # output of this script
    # ---------------------
    #
    #   +------------------------------------------------------------------------------+
    #   |                          Starting testcase Testcase                          |
    #   +------------------------------------------------------------------------------+
    #   +------------------------------------------------------------------------------+
    #   |                          Starting section test_one                           |
    #   +------------------------------------------------------------------------------+
    #   Caught exception: 'key does not exist'
    #   Traceback (most recent call last):
    #     File "examples.py", line 11, in test_one
    #       {}['key does not exist']
    #   KeyError: 'key does not exist'
    #   The result of section test_one is => ERRORED
    #   +------------------------------------------------------------------------------+
    #   |                          Starting section test_two                           |
    #   +------------------------------------------------------------------------------+
    #   An assertion exception was caught.
    #   unfortunately 1 doesn't equal to 0
    #   The result of section test_two is => FAILED
    #   The result of testcase Testcase is => ERRORED
    #
    # Note: the overall result of this testcase is Errored due to roll-ups
    #
    # SECTIONS/TESTCASES                                                 RESULT
    # --------------------------------------------------------------------------
    # .
    # `-- Testcase                                                      ERRORED
    #     |-- test_one                                                  ERRORED
    #     `-- test_two                                                   FAILED

Within your test sections, use ``try ... except ...`` statements to handle any
exceptions that are *expected*. This makes sure these *expected exceptions*
do not propagate to the test infrastructure, polluting the results of current
running sections.

.. note::

    Beware of the `Exception Hierarchy`_. Do not catch ``BaseException``, as it
    causes your scripts to ignore requests to exit and keyboard interrupts
    such as *ctrl-c*.

.. _AssertionError: https://docs.python.org/3.4/library/exceptions.html#AssertionError
.. _Exceptions: https://docs.python.org/3.4/library/exceptions.html
.. _Exception: https://docs.python.org/3.4/library/exceptions.html#Exception
.. _Exception Hierarchy: https://docs.python.org/3.4/library/exceptions.html#exception-hierarchy


.. _result_apis:

Result APIs
-----------

In addition to the automatic result assignment behaviors, it is also possible to
manually provide section results by calling one of the ``TestItem`` static
methods:

    - ``TestItem.passed(reason, goto, from_exception, data)``
    - ``TestItem.failed(reason, goto, from_exception, data)``
    - ``TestItem.errored(reason, goto, from_exception, data)``
    - ``TestItem.skipped(reason, goto, from_exception, data)``
    - ``TestItem.blocked(reason, goto, from_exception, data)``
    - ``TestItem.aborted(reason, goto, from_exception, data)``
    - ``TestItem.passx(reason, goto, from_exception, data)``

Upon calling, the current section execution  **terminates immediately**,
returns and is set with the corresponding result. In other words, result apis
can only be called **once** per script section, and all code immediately after
it is not executed (similar to how ``return`` statement works).

All results apis accept the following *optional* arguments:

    - ``reason``, describing the conditions & reasons of why this result is
      provided.

    - ``goto``, list of sections to "go to" after this section. Refer to
      :ref:`aetest_goto` documentation for details.

    - ``from_exception``, accepts an exception object and will add the
      traceback of this exception to the result's `reason`.

    - ``data``, accepts a dict of arbitrary data that is relevant to the result.
      A representation of this data is stored by the :ref:`Reporter` for
      external processing or reference.


.. tip::

    ``TestItem`` is the base class of all classes, and thus you can call
    ``self.failed()`` within section code directly instead of the absolute
    reference ``TestItem.failed()`` (see :ref:`object_model`).

.. code-block:: python

    # Example
    # -------
    #
    #   manually setting results for sections

    from pyats import aetest

    # using common setup as an example for a change
    class CommonSetup(aetest.CommonSetup):

        @aetest.subsection
        def subsection_that_passes(self):
            self.passed("failure is not an option")

            # any code after a result api is not executed
            evenThisAPICallThatDoesNotExist()

        @aetest.subsection
        def subsection_that_fails(self):
            self.failed("failure... is a must in this test")

        @aetest.subsection
        def subsection_that_is_skipped(self):
            self.skipped("i don't want to run this section.")

    # output of this script
    # ---------------------
    #
    #   +------------------------------------------------------------------------------+
    #   |                            Starting common setup                             |
    #   +------------------------------------------------------------------------------+
    #   +------------------------------------------------------------------------------+
    #   |                  Starting subsection subsection_that_passes                  |
    #   +------------------------------------------------------------------------------+
    #   Passed reason: failure is not an option
    #   The result of subsection subsection_that_passes is => PASSED
    #   +------------------------------------------------------------------------------+
    #   |                  Starting subsection subsection_that_fails                   |
    #   +------------------------------------------------------------------------------+
    #   Failed reason: failure... is a must in this test
    #   The result of subsection subsection_that_fails is => FAILED
    #   +------------------------------------------------------------------------------+
    #   |                Starting subsection subsection_that_is_skipped                |
    #   +------------------------------------------------------------------------------+
    #   Skipped reason: i don't want to run this section.
    #   The result of subsection subsection_that_is_skipped is => SKIPPED
    #   The result of common setup is => FAILED
    #
    #  SECTIONS/TESTCASES                                                RESULT
    #  -------------------------------------------------------------------------
    #  .
    #  `-- CommonSetup                                                   FAILED
    #      |-- subsection_that_passes                                    PASSED
    #      |-- subsection_that_fails                                     FAILED
    #      `-- subsection_that_is_skipped                               SKIPPED

Interaction Results
-------------------

There are also rare cases when a result must be manually determined by a human.
Such as a test that relies upon changes that happen in the physical world. For
these cases there is a utility that allows a user to decide the result.

The class ``WebInteraction`` can pause test execution and notify a user via
email that input is required. This email has a link to a webpage hosted by
``WebInteraction`` that has a form for the user to submit to give a result.

.. code-block:: python

    # Example
    # -------
    #
    #   example testscript for using WebInteraction

    from pyats import aetest
    from pyats.aetest.utils.interaction import WebInteraction

    class TestcaseOne(aetest.Testcase):

        @aetest.setup
        def setup(self): pass

        @aetest.test
        def test_one(self, section):
            WebInteraction('Brief title for this interaction',
                           'Message for the user about how to assess this test',
                           section = section,
                           timeout = 300
                          ).interact()

        @aetest.cleanup
        def cleanup(self): pass

.. csv-table:: WebInteraction Constructor Arguments
    :header: "Argument", "Type", "Description"
    :widths: 20, 20, 60

    "``subject``", "``str`` (required)", "A brief description of the
    interaction."
    "``message``", "``str`` (required)", "This is the message that describes to
    the user what the test is and how they determine the result."
    "``section``", "``ref`` (required)", "Reference to section or step that
    called interaction. This provides the name name of the test to the user, as
    well as the APIs to return a test result."
    "``host``", "``str``", "The host address to bind to. ``localhost`` will only
    allow processes from the same host to connect to the server."
    "``port``", "``int``", "The port for the webpage to be hosted at. Default is
    0 for a kernel provisioned port."
    "``web_template``", "``str``/``jinja2.Template``", "Template for the HTML
    webpage. This can inherit by extending default_web_template."
    "``timeout``", "``float``/``str``", "How long the test should wait for a
    human in seconds. Can also take string 'inf' for no timeout. Default is 1
    hour."
    "``timeout_result``", "``str``", "Name of the result given to the test when
    it times out. Default is ``'BLOCKED'``."
    "``no_email``", "``bool``", "When set to ``True``, blocks an email from
    being sent to notify a user for interaction."
    "``from_address``", "``str``", "The email address that the notification will
    be sent from. Defaults to the user login."
    "``to_address``", "``str``", "The email address that the notification will
    be sent to. Defaults to the user login."
    "``email_subject``", "``str``/``jinja2.Template``", "Alternate Subject line
    for email notification."
    "``email_body``", "``str``/``jinja2.Template``", "Alternate Body for email
    notification."

.. note::

    ``web_template`` can inherit from the existing default template. You can
    find this template at
    ``<python_install>/site-packages/pyats/aetest/utils/templates/default_web_template.html``
    to see what blocks are defined, as well as some arguments that can be
    used.

    Read about `jinja2 template inheritance`_.

.. _jinja2 template inheritance: http://jinja.pocoo.org/docs/2.10/templates/#template-inheritance

Result Counting
---------------

In ``aetest``, only ``TestContainer`` class' results counts in the *summary
result numbers*. Even though child sections within ``TestContainer`` classes
have their own results, they are considered to be a part of its parent
container, and their results is thus not counted for in the summary.

Accounted For
    ``CommonSetup``, ``Testcase`` and ``CommonCleanup``.

Not Accounted For
    ``Subsection``, ``SetupSection``, ``TestSection`` and ``CleanupSections``.


.. csv-table:: Result Counting Examples
    :header: Condition, Result Numbers
    :widths: 80, 20

    "``CommonSetup`` with 50 subsections", 1
    "``Testcase`` with ``setup``, 20x ``test`` and ``cleanup``", 1
    "2x ``Testcase``, ``CommonCleanup``", 3
    "``CommonSetup``, 20x ``Testcase``, ``CommonCleanup``", 22

.. code-block:: python

    # Example
    # -------
    #
    #   example testscript and number counting

    from pyats import aetest

    class CommonSetup(aetest.CommonSetup):

        @aetest.subsection
        def subsection_one(self): pass

        @aetest.subsection
        def subsection_two(self): pass

    class TestcaseOne(aetest.Testcase):

        @aetest.setup
        def setup(self): pass

        @aetest.test
        def test_one(self): pass

        @aetest.test
        def test_two(self):
            self.failed()

        @aetest.cleanup
        def cleanup(self): pass


    # +------------------------------------------------------------------------+
    # |                                Summary                                 |
    # +------------------------------------------------------------------------+
    #  Number of ABORTED                                                      0
    #  Number of BLOCKED                                                      0
    #  Number of ERRORED                                                      0
    #  Number of FAILED                                                       1
    #  Number of PASSED                                                       1
    #  Number of PASSX                                                        0
    #  Number of SKIPPED                                                      0
    # --------------------------------------------------------------------------


--------------------------------------------------------------------------------



Result API Internals
--------------------

.. sidebar:: Confucius Say...

    The information here onwards is for users interested in ``aetest``
    internals & extensions only.

    If you are new to this, do not read on. These advanced topics may
    further fuel your confusion.

Result APIs such as ``TestItem.passed()`` terminate current execution and
return immediately because they are internally implemented to raise
``AEtestInternalSignals`` exceptions, and are handled by the execution engine to
assign a corresponding result to the current test section.

``AEtestInternalSignals`` subclasses from ``BaseException`` class intentionally
in order to avoid any blanket catching of ``Exception`` in ``try ... except``
clause. They are called **signals** because they are used for signalling
purposes, to instruct the infrastructure to assign a result and carry on.


.. csv-table:: Internal Signal Mappings
    :header: Result API, Exception Signal, Result Object

    "``TestItem.passed(reason, goto)``", ``AEtestPassedSignal``, ``Passed``
    "``TestItem.failed(reason, goto)``", ``AEtestFailedSignal``, ``Failed``
    "``TestItem.errored(reason, goto)``", ``AEtestErroredSignal``, ``Errored``
    "``TestItem.skipped(reason, goto)``", ``AEtestSkippedSignal``, ``Skipped``
    "``TestItem.blocked(reason, goto)``", ``AEtestBlockedSignal``, ``Blocked``
    "``TestItem.aborted(reason, goto)``", ``AEtestAbortedSignal``, ``Aborted``
    "``TestItem.passx(reason, goto)``", ``AEtestPassxSignal``, ``Passx``

In essence, within anywhere in the testscript and/or libraries, if these
exceptions are raised (as they are still exceptions in nature), ``aetest``
behaves exactly the same as calling result apis.

.. code-block:: python

    # Example
    # -------
    #
    #   raising signalling exceptions

    from pyats import aetest
    from pyats.aetest.signals import AEtestAbortedSignal

    class CommonCleanup(aetest.CommonCleanup):

        @aetest.subsection
        def subsection(self):
            # subsection getting aborted using signaling
            raise AEtestAbortedSignal(reason = 'feeling it.')

    # output of this script
    # ---------------------
    #
    #   +------------------------------------------------------------------------------+
    #   |                           Starting common cleanup                            |
    #   +------------------------------------------------------------------------------+
    #   +------------------------------------------------------------------------------+
    #   |                        Starting subsection subsection                        |
    #   +------------------------------------------------------------------------------+
    #   Aborted reason: feeling it.
    #   The result of subsection subsection is => ABORTED
    #   The result of common cleanup is => ABORTED
