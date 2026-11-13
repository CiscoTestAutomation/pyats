.. _aetest_retry:

Retry Sections
==============

.. sidebar:: Helpful Reading

    - `Classes Tutorial`_
    - `Decorators`_
    - `Scopes and Namespaces`_
    - `Iterator Types`_
    - `Yield Expressions`_
    - `Factory Design`_


.. _Decorators: https://wiki.python.org/moin/PythonDecorators
.. _Classes Tutorial: https://docs.python.org/3.4/tutorial/classes.html
.. _Scopes and Namespaces: https://docs.python.org/3.4/tutorial/classes.html#python-scopes-and-namespaces
.. _Iterator Types: https://docs.python.org/3.4/library/stdtypes.html#typeiter
.. _Yield Expressions: https://docs.python.org/3.4/reference/expressions.html#yieldexpr
.. _Factory Design: http://en.wikipedia.org/wiki/Factory_%28object-oriented_programming%29

``aetest`` supports section retry: re-execution of test section code
enabled via decorator or CLI argument.

The following describes each section and their retry capability and behaviors:

``CommonSetup``/``CommonCleanup``
    Common setup and cleanup sections are unique within each testscript. They
    are run only once per testscript execution, and are not retryable.

    ``subsection``
        Subsections within ``CommonSetup``and``CommonCleanup`` are retryable.
        When a ``subsection`` is marked for retry, each of its iterations is
        reported as a new subsection.

``Testcase``
    Testcases are retryable. Each iteration of a retry ``Testcase`` is reported
    individually as new testcase instances with different ``uid``. When a
    ``Testcase`` is retried, all of its contents (setup, tests and cleanup) are
    run fully per each iteration.

    ``setup``/``cleanup``
        Setup and cleanup sections within each testcase is unique, and are retryable.

    ``test``
        Test sections within ``Testcase`` are retryable individually. Each
        iteration has its own unique id, and is reported as a new test
        section.

.. hint::

    ``SetupSection``,``CleanupSection``,``SubSection``,``Testcase`` and
    ``TestSection`` sections are the only retryable sections.


Retry Decorator
---------------

Sections are marked for retry when they are decorated with ``@aetest.retry``, and its
looping parameters provided as decorator arguments. During runtime, when
``aetest`` infrastructure detects retryable section code, their corresponding
section object is then instantiated once for each of its iterations. It takes two
arguments:

- ``retries`` (int) - Number of retries.
- ``retry_wait`` (int) - Wait time between each retry.

.. note::
    By default the ``retries`` is set to 3 times and retry_wait is set to 10 seconds.

.. code-block:: python

    #   defining retry on sections

    from pyats import aetest

    # defining a testcase that retries
    # this testcase also contains a test section that is retried twice
    @aetest.retry(retries=3, retry_wait=2)
    class MyTestcase_1(aetest.Testcase):

        # test section
        @aetest.retry(retries=2, retry_wait=2)
        @aetest.test
        def testcase1(self):
            pass

As shown above, the minimum requirement to retry a section (eg, to run its code
1+ times) is to decorate the section with ``@aetest.retry``.

When ``@aetest.retry``is used on a``@aetest.subsection``or``@aetest.test``,
the section method is effectively decorated twice, and even though the order
does not matter, it make more sense to use ``@aetest.retry`` as the outermost
decorator, signifying that this method is first marked as a section, then this
section is retryable.


.. _aetest_loop_retry_scope:

Retry Scope with Loops
---------------------

Decorator placement determines which loop invocations a retry replays.
A retry outside a loop evaluates the combined result of the complete child
plan before deciding whether to replay it. Placing retry inside a loop gives
each outer iteration its own retry boundary.

.. code-block:: python

    from pyats import aetest

    class CheckDevices(aetest.Testcase):
        @aetest.retry(retries=2, retry_wait=0)
        @aetest.loop(devices=['r1', 'r2'])
        @aetest.loop(pids=['p1', 'p2'])
        @aetest.test
        def check(self, devices, pids):
            pass

One attempt runs ``r1/p1``, ``r1/p2``, ``r2/p1``, and ``r2/p2``. An eligible
failure replays all four invocations, including those that passed. The next
attempt starts only after the complete previous attempt has finished.
``retries=2`` allows one initial attempt and up to two retries.

Move retry inside the device loop to replay only the current device's PID
loop:

.. code-block:: python

    @aetest.loop(devices=['r1', 'r2'])
    @aetest.retry(retries=2, retry_wait=0)
    @aetest.loop(pids=['p1', 'p2'])
    @aetest.test
    def check(self, devices, pids):
        pass

Here, ``r1/p1`` and ``r1/p2`` complete and retry together if needed before the
plan advances to ``r2``. Placing retry below both loop decorators retries only
the current device/PID invocation.

Retrying a looped testcase replays its setup, test sections, and cleanup for
each testcase invocation in the retry boundary. Subsections support the same
loop/retry composition. Loops remain sequential and normal AEtest processors,
UID filters, and control-flow signals still apply.

Results and Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

The existing retry eligibility, wait interval, and CLI configuration apply.
By default, failed results are eligible; include ``'errored'`` in
``section_results`` to retry errored attempts. Retry-only targets retain their
existing behavior.

Each attempt's invocations appear separately in the report. UIDs gain a
`` [Retry 1]`` suffix on the first retry. When a target has multiple nested
retry boundaries, the suffix includes the boundary's outer-to-inner position,
for example `` [Retry 1.1]`` for the first retry of the outer boundary and
`` [Retry 2.1]`` for the first retry of the inner boundary.

Intermediate attempts remain visible while their results are excluded from
final parent rollup. The completed retry boundary contributes its final result.
A successful retry after a failed or errored attempt uses ``PASSX``; exhausted
retries retain the final attempt's result. The ``retry`` and ``retry_count``
parameters describe the innermost active retry boundary.

See :ref:`aetest_hierarchical_looping` for parameter precedence, input replay,
and nested UID formatting.


Function Arguments
------------------

The ``retry``and``retry_count`` arguments can be passsed as function
parameters check for retry and retry count values.

        - ``retry`` (bool) -  To check if the section is being retried. (Optional)
        - ``retry_count`` (int) - To track the retry count (Optional)

.. code-block:: python

        # retry function arguments

        @aetest.retry()
        @aetest.test
        def connect_testcase(self, steps, retry, retry_count):
            with steps.start('Failure case') as step:
                if retry and retry_count>1:
                    step.passed()
                step.failed()


Retry CLI argument
------------------

Retry can be enabled with default settings using the `\-\-retry` argument.

.. code-block:: text

    pyats run manifest job.tem --retry

To provide setting for retry, you can use one of the following formats:

    1. YAML file
    2. JSON formatted data
    3. Key/Value Pairs

The JSON and Key/Value pairs can optionally be Base64 encoded.

Schema
------

The schema for YAML and JSON structured settings is show below.

The values for sections and section_results are not case sensitive, i.e. you can use `Failed` or `failed` as values.

.. code-block:: python

    {
        Optional('sections'): list, # sections that needs to be retried. Eg  - Testcase, Subsection, Setupsection, Cleanupsection, Testsection
        Optional('section_results'): list, # section that needs to be retried based on its results. Eg Failed, Errored. Default: Failed
        Optional('testcases'): { # aetest testcases
            Any(): { # section name
                Optional('retries'): Default(int, 3), # number of retries
                Optional('retry_wait'): Default(int, 10), # retry delay between each retry
            }
        },
        'retries': Default(int, 3),
        'retry_wait': Default(int, 10),
    }

YAML file
~~~~~~~~~

To use a YAML file with retry settings, add the filename after the retry argument.

.. code-block:: text

    pyats run manifest job.tem --retry retry.yaml

.. code-block:: yaml

    # retry.yaml
    sections:
        - Testcase
        - Testsection
    retries: 4
    retry_wait: 2

The section type mentioned under the ``sections`` key will be retried.
This will retry testcase and testsection 4 times with a waiting period of 2 seconds.
If no sections provided then the testcase will be retried by default.

.. code-block:: yaml

    # retry.yaml
    section_results:
        - failed
        - errored
    retries: 4
    retry_wait: 2

The section results mentioned under the ``section_results`` key will be retried.

.. code-block:: yaml

    testcases:
        # Testcase class name
        test_flaky:
            # Optionally specify retry count and wait time
            retries: 3
            retry_wait: 2

To Enable retry on specific sections, refer the above example.

JSON formatted data
~~~~~~~~~~~~~~~~~~~

To use JSON as settings for retry, you can specify a raw JSON string or Base64
encoded JSON string.

.. code-block:: text

    pyats run manifest job.tem --retry \
    '{"sections": ["Cleanupsection", "Testsection"], "retries": 2, "retry_wait": 2}'

.. note::

    Using raw JSON strings on the command line is error prone, using Base64
    encoded JSON strings is recommended.

Key/value Pairs
~~~~~~~~~~~~~~~

Key/value argments can be used using ``k=v`` syntax on the command line.

.. code-block:: text

    pyats run manifest job.tem --retry retries=3 retry_wait=10

For a list of values for sections and section_results, use comma seperated values:

.. code-block:: text

    pyats run manifest job.tem --retry sections=testsection section_result=failed,errored


Base64 encoded JSON (or Key/Value pair)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below example base64 encoded JSON string has a value of `{"testcases": {"FlakyTest.test_flaky": {"retries": 3, "retry_wait": 10}}}`

Using Base64 encoding is recommended for JSON strings to avoid problems with
spacing and/or quote interpretation by the unix shell.

.. code-block:: text

    pyats run manifest job.tem --retry \
    eyJ0ZXN0Y2FzZXMiOiB7IkZsYWt5VGVzdC50ZXN0X2ZsYWt5IjogeyJyZXRyaWVzIjogMywgInJldHJ5X3dhaXQiOiAxMH19fQo=


Example output
--------------

TestSection Retry
~~~~~~~~~~~~~~~~~

This testscript's resulting section summary report would look like below with
section retry enabled.

.. code-block:: text

    +------------------------------------------------------------------------------+
    |                             Task Result Details                              |
    +------------------------------------------------------------------------------+
    Task-1: script_1                                                           PASSX
    `-- MyTestcase_1                                                           PASSX
        |-- testcase_setup                                                    PASSED
        |-- connect_testcase                                                  FAILED
        |   `-- STEP 1: Failure case                                          FAILED
        |-- connect_testcase [Retry 1]                                        FAILED
        |   `-- STEP 1: Failure case                                          FAILED
        |-- connect_testcase [Retry 2]                                         PASSX
        |   `-- STEP 1: Failure case                                          PASSED
        `-- testcase_cleanup                                                  PASSED


Testcase Retry
~~~~~~~~~~~~~~

This testscript's resulting section summary report would look like below with
testcase retry enabled.

.. code-block:: text

    +------------------------------------------------------------------------------+
    |                             Task Result Details                              |
    +------------------------------------------------------------------------------+
    Task-1: script                                                            FAILED
    |-- MyTestcase_1                                                          FAILED
    |   |-- testcase_setup                                                    PASSED
    |   |-- connect_testcase                                                  FAILED
    |   |   `-- STEP 1: Failure case                                          FAILED
    |   `-- testcase_cleanup                                                  PASSED
    |-- MyTestcase_1 [Retry 1]                                                FAILED
    |   |-- testcase_setup                                                    PASSED
    |   |-- connect_testcase                                                  FAILED
    |   |   `-- STEP 1: Failure case                                          FAILED
    |   `-- testcase_cleanup                                                  PASSED
    |-- MyTestcase_1 [Retry 2]                                                FAILED
    |   |-- testcase_setup                                                    PASSED
    |   |-- connect_testcase                                                  FAILED
    |   |   `-- STEP 1: Failure case                                          FAILED
    |   `-- testcase_cleanup                                                  PASSED
    `-- MyTestcase_1 [Retry 3]                                                FAILED
        |-- testcase_setup                                                    PASSED
        |-- connect_testcase                                                  FAILED
        |   `-- STEP 1: Failure case                                          FAILED
        `-- testcase_cleanup                                                  PASSED

Loop and Retry Review Job
-------------------------

Download the :download:`review job <examples/hierarchical_looping/loop_retry_matrix_job.py>`
and its :download:`testscript <examples/hierarchical_looping/loop_retry_matrix.py>`
into the same directory, then run:

.. code-block:: console

    pyats run job loop_retry_matrix_job.py --no-mail

The job exercises every retry placement at the boundaries around zero, one,
and two loop dimensions: 14 plans for each of the testcase, test-section, and
subsection targets. Six tasks cover passing runs, a single failure, inner retry
exhaustion followed by outer recovery, complete exhaustion, an eligible error,
and skipped invocations. This gives 252 scenarios and 1,212 probe invocations.
No testbed is required.

Scenario names encode depth and retry boundaries. For example, ``D2_R101``
uses two loop dimensions with retry outside both loops and at the leaf, while
``D2_R010`` retries only the inner loop for each outer iteration.

Each task logs ``MATRIX TRACE`` records with its plan, parameters, invocation UID,
and retry count. Its final ``zz_audit`` subsection checks replay counts and UID
uniqueness for all 42 scenarios. The archive includes the job, testscript,
``matrix_manifest.json``, and one ``matrix_<profile>.json`` trace per task.

The deliberately failed and errored scenarios make the overall job result
failed. All six ``zz_audit`` subsections should pass; these audits distinguish
expected demonstration outcomes from a replay mismatch.
