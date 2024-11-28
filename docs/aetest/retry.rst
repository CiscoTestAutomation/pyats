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

    *What is a  retry? Refer to the end of this section.*

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


Defining Retry
--------------

Sections are marked for retry when they are decorated with ``@retry``, and its
looping parameters provided as decorator arguments. During runtime, when 
``aetest`` infrastructure detects retryable section code, their corresponding 
section object is then instantiated once for each of its iterations. It takes two
arguments
        retries - Number of retries.
        retry_wait - Wait time between each retries.

.. code-block:: python

    # Example
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

        # To test retry on aetest.cleanup and check the retry and retry_count parameters
        @aetest.retry(retries=2, retry_wait=2)
        @aetest.cleanup
        def testcase_cleanup(self, retry, retry_count):
            if retry and retry_count>1:
                pass
            else:
                raise AEtestStepFailedSignal
    

    # this testscript's resulting sections would look like this below

+------------------------------------------------------------------------------+
  SECTIONS/TESTCASES                                                      RESULT
 --------------------------------------------------------------------------------
 .
 |-- MyTestcase_1                                                          FAILED
 |   |-- testcase_setup                                                    PASSED
 |   |-- connect_testcase                                                  FAILED
 |   |   `-- Step 1: Failure case                                          FAILED
 |   |-- connect_testcase Retry 1                                          FAILED
 |   |   `-- Step 1: Failure case                                          FAILED
 |   |-- connect_testcase Retry 2                                           PASSX
 |   |   `-- Step 1: Failure case                                          PASSED
 |   |-- testcase_cleanup                                                  FAILED
 |   |-- testcase_cleanup Retry 1                                          FAILED
 |   `-- testcase_cleanup Retry 2                                           PASSX
 |-- MyTestcase_1 Retry 1                                                  FAILED
 |   |-- testcase_setup                                                    PASSED
 |   |-- connect_testcase                                                  FAILED
 |   |   `-- Step 1: Failure case                                          FAILED
 |   |-- connect_testcase Retry 1                                          FAILED
 |   |   `-- Step 1: Failure case                                          FAILED
 |   |-- connect_testcase Retry 2                                           PASSX
 |   |   `-- Step 1: Failure case                                          PASSED
 |   |-- testcase_cleanup                                                  FAILED
 |   |-- testcase_cleanup Retry 1                                          FAILED
 |   `-- testcase_cleanup Retry 2                                           PASSX
 |-- MyTestcase_1 Retry 2                                                  FAILED
 |   |-- testcase_setup                                                    PASSED
 |   |-- connect_testcase                                                  FAILED
 |   |   `-- Step 1: Failure case                                          FAILED
 |   |-- connect_testcase Retry 1                                          FAILED
 |   |   `-- Step 1: Failure case                                          FAILED
 |   |-- connect_testcase Retry 2                                           PASSX
 |   |   `-- Step 1: Failure case                                          PASSED
 |   |-- testcase_cleanup                                                  FAILED
 |   |-- testcase_cleanup Retry 1                                          FAILED
 |   `-- testcase_cleanup Retry 2                                           PASSX
 `-- MyTestcase_1 Retry 3                                                  FAILED
     |-- testcase_setup                                                    PASSED
     |-- connect_testcase                                                  FAILED
     |   `-- Step 1: Failure case                                          FAILED
     |-- connect_testcase Retry 1                                          FAILED
     |   `-- Step 1: Failure case                                          FAILED
     |-- connect_testcase Retry 2                                           PASSX
     |   `-- Step 1: Failure case                                          PASSED
     |-- testcase_cleanup                                                  FAILED
     |-- testcase_cleanup Retry 1                                          FAILED
     `-- testcase_cleanup Retry 2                                           PASSX


As shown above, the minimum requirement to retry a section (eg, to run its code 
1+ times) is to decorate the section with ``@retry``.

When ``@retry`` is used on a ``@subsection`` or ``@test``, the section method
is effectively decorated twice, and even though the order does not matter, it 
make more sense to use ``@retry`` as the outermost decorator, signifying that
this method is first marked as a section, then this section is retryable.


To use the retry using the cli args.

case 1: Yaml file

pyats run manifest job.tem --retry retry.yaml

retry.yaml

 sections:
   - Testcase
   - Subsection

 retries: 4
 retry_wait: 2

case 2: Json formatted data

pyats run manifest job.tem --retry {"sections": ["Cleanupsection", "Testsection"], "retries": 2, "retry_wait": 2}

case 3: Parameters

pyats run manifest job.tem --retry retries=3 retry_wait=10

case 4: Base64 encoded

`pyats run manifest job.tem --retry eyJ0ZXN0Y2FzZXMiOiB7IkZsYWt5VGVzdC50ZXN0X2ZsYWt5IjogeyJyZXRyaWVzIjogMywgInJldHJ5X3dhaXQiOiAxMH19fQo=


