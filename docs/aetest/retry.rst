.. _aetest_retry:

Retry Sections
================

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


As an integral extension of :ref:`test_parameters` data-driven testing concept, 
``aetest`` also supports section retry: reusing section code body by providing
it with different parameters during each retry iteration. 

The following describes each section and their retry capability and behaviors:

``CommonSetup``/``CommonCleanup``
    Common setup and cleanup sections are unique within each testscript. They
    are run only once per testscript execution, and are not retryable.

    ``subsection``
        Subsections within ``CommonSetup`` and ``CommonCleanup`` are retryable.
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

    in other words, ``setup``, ``cleanup`` ``subsection``, ``Testcase`` and ``test`` sections
    are the only retryable sections.


Defining Retry using retry decorator
------------------------------------

Sections are marked for retry when they are decorated with ``@retry``, and its
looping parameters provided as decorator arguments. During runtime, when 
``aetest`` infrastructure detects retryable section code, their corresponding 
section object is then instantiated once for each of its iterations. It takes two
arguments
        - ``retries``(int) - Number of retries.
        - ``retry_wait``(int) - Wait time between each retries.

Aetest retry parameters
------------------------
The user can use ``retry`` and ``retry_count`` aetest parameters in their script to do
the retry check and keep in track of retry count.

        - ``retry``(bool) -  To check if the section is being retried. (Optional)
        - ``retry_count``(int) - To track the retry count (Optional)

.. code-block:: python

    # Example-1
    # -------
    #
    #   defining retry on sections

    from pyats import aetest

    # defining a testcase that retries
    # this testcase also contains a test section that is retried thrice
    @aetest.retry(retries=3, retry_wait=2)
    class MyTestcase_1(aetest.Testcase):

        # setup section
        @aetest.retry(retries=2, retry_wait=2)
        @aetest.setup
        def testcase_setup(self):
            pass
        
        # To test retry on aetest.test and check the retry and retry_count parameters    
        @aetest.retry(retries=2, retry_wait=2)
        @aetest.test
        def connect_testcase(self, steps, retry, retry_count):
            with steps.start('Failure case') as step:
                if retry and retry_count>1:
                    step.passed()
                step.failed()

        # cleanup section
        @aetest.retry(retries=2, retry_wait=2)
        @aetest.cleanup
        def testcase_cleanup(self, retry, retry_count):
            pass

# This testscript's resulting sections would look like this

.. code-block:: log

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


As shown above, the minimum requirement to retry a section (eg, to run its code 
1+ times) is to decorate the section with ``@retry``.

When ``@retry`` is used on a ``@subsection`` or ``@test``, the section method
is effectively decorated twice, and even though the order does not matter, it 
make more sense to use ``@retry`` as the outermost decorator, signifying that
this method is first marked as a section, then this section is retryable.


Defining Retry using the `\-\-retry` argument
--------------------------------------

Retry feature can be triggered from cli as well, by using the `\-\-retry` argument.
It supports the following formats:

    1. yaml file
    2. json formatted data
    3. k=v Pair
    4. Base64 encoded

Examples:
---------

case 1: Yaml file
-----------------
.. code-block:: text
    pyats run manifest job.tem --retry retry.yaml

Example-1
---------
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

Example-2
---------
.. code-block:: yaml

    # retry.yaml
    section_results:
        - failed
        - errored
    retries: 4
    retry_wait: 2

The section results mentioned under the ``section_results`` key will be retried.

Example-3
---------
.. code-block:: yaml
    testcases:
        # section
        test_flaky:
            # Optionally specify retry count and wait time
            retries: 3
            retry_wait: 2

To Enable retry on specific sections, refer the above example.

Important
---------
These scenarios can also be enabled in retry with other supported
formats like json, k=v pair and Base64 encoded.

case 2: Json formatted data
---------------------------
.. code-block:: text
    pyats run manifest job.tem --retry \
    {"sections": ["Cleanupsection", "Testsection"], "retries": 2, "retry_wait": 2}

case 3: k=v Pair
----------------
.. code-block:: text
    pyats run manifest job.tem --retry retries=3 retry_wait=10

case 4: Base64 encoded
----------------------
.. code-block:: text
    pyats run manifest job.tem --retry \
    eyJ0ZXN0Y2FzZXMiOiB7IkZsYWt5VGVzdC50ZXN0X2ZsYWt5IjogeyJyZXRyaWVzIjogMywgInJldHJ5X3dhaXQiOiAxMH19fQo=

.. note::
    By default the ``retries`` is set to 3 times and retry_wait is set to 10 seconds.

