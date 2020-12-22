.. _reports:

Report Details
==============

When ``aetest`` finishes running a testscript, an overall summary report is
provided to the user. This report provides an outlook of what testcases were
run, and what their results are. Depending on the :ref:`execution mode
<running_aetest_script>`, this reporting behavior may differ.

.. _aetest_standalone_reporter:

Standalone Reporter
-------------------

``StandaloneReporter`` is default reporter used when ``aetest`` scripts are run
directly from the commandline via :ref:`aetest_standalone_execution`. This
reporter directly prints testcases, sections and steps information to the screen
at the end of of the run in a tree-structure format.

.. code-block:: text

    # Example
    # -------
    #
    #   the following is an example standalone reporter ouput

    +------------------------------------------------------------------------------+
    |                               Detailed Results                               |
    +------------------------------------------------------------------------------+
     SECTIONS/TESTCASES                                                      RESULT
    --------------------------------------------------------------------------------
    .
    |-- common_setup                                                         PASSED
    |   |-- sample_subsection_1                                              PASSED
    |   `-- sample_subsection_2                                              PASSED
    |-- tc_one                                                               PASSED
    |   |-- prepare_testcase                                                 PASSED
    |   |-- simple_test_1                                                    PASSED
    |   |-- simple_test_2                                                    PASSED
    |   `-- clean_testcase                                                   PASSED
    |-- TestcaseWithSteps                                                   ERRORED
    |   |-- setup                                                            PASSED
    |   |   |-- Step 1: this is a description of the step                    PASSED
    |   |   `-- Step 2: another step                                         PASSED
    |   |-- step_continue_on_failure_and_assertions                          FAILED
    |   |   |-- Step 1: assertion errors -> Failed                           FAILED
    |   |   `-- Step 2: allowed to continue executing                        FAILED
    |   |-- steps_errors_exits_immediately                                  ERRORED
    |   |   `-- Step 1: exceptions causes all steps to skip over            ERRORED
    |   `-- steps_with_child_steps                                           PASSED
    |       |-- Step 1: test step one                                        PASSED
    |       |-- Step 1.1: substep one                                        PASSED
    |       |-- Step 1.1.1: subsubstep one                                   PASSED
    |       |-- Step 1.1.1.1: subsubsubstep one                              PASSED
    |       |-- Step 1.1.1.1.1: running out of indentation                   PASSED
    |       |-- Step 1.1.1.1.1.1: definitely gone too far...                 PASSED
    |       |-- Step 1.2: substep two                                        PASSED
    |       |-- Step 2: test step two                                        PASSED
    |       |-- Step 2.1: function step one                                  PASSED
    |       |-- Step 2.2: function step two                                  PASSED
    |       `-- Step 2.3: function step three                                PASSED
    `-- common_cleanup                                                       PASSED
        `-- clean_everything                                                 PASSED

There is no customization available for this reporter.


.. _aetest_reporter:

AETest Reporter
---------------
When testscripts are run under :ref:`aetest_jobfile_execution` mode,
:ref:`reporter` is used to collect test run information.
