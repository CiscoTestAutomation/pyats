Using Multiprocessing
=====================

.. sidebar:: Helpful Reading

    - `Multiprocessing`_

    - `Pipes/Queues`_

    - `pickle`_


.. _Multiprocessing: https://docs.python.org/3/library/multiprocessing.html
.. _`Pipes/Queues`: https://docs.python.org/3.4/library/multiprocessing.html#pipes-and-queues
.. _pickle: https://docs.python.org/3.4/library/pickle.html

Because of the high-degree of automated process handling & configurations done
by :ref:`easypy`, in pyATS, users are encouraged to use ``multiprocessing``
module directly to achieve parallelism in their code/scripts without needing to
worry about things like logging and reporting.

The following are examples of using Python ``multiprocessing`` module directly.
Keep in mind that ``multiprocessing`` is a built-in Python module: users are
expected read and understand how it works, and investigate their own process
errors. The purpose of this document is to demonstrate the integration of pyATS
around ``multiprocessing`` process forks.


Example
-------

When scripts are run under Easypy, forking processes using ``multiprocessing``
automatically creates a new TaskLog log file in the child process. The
parent log has an indicator pointing where the new log file is.

.. code-block:: python

    # Example
    # -------
    #
    #   using multiprocessing in your testscript

    # multiprocess_example.py
    # -----------------------
    import time
    import logging
    import multiprocessing

    from pyats import aetest

    logger = logging.getLogger(__name__)

    # define some functions to be called in forked processes
    def f(x):
        result = x*x
        logger.info('%s * %s == %s' % (x,x, result))
        return result

    def sleep(x):
        logger.info('sleeping for %s seconds' % x)
        time.sleep(x)
        logger.info('done sleeping, fully recharged :)')

    class Testcase(aetest.Testcase):

        # create a child process to run the sleep function & block
        @aetest.test
        def sleep_test(self):
            p = multiprocessing.Process(target = sleep, args = (30,))
            p.start()
            p.join()

        # create a pool of child processes to do computing
        # (not that this makes sense... for example's sake)
        @aetest.test
        def pool_test(self):
            with multiprocessing.Pool(2) as pool:
                result = pool.map(f, range(20))

            logger.info('result = %s' % result)


    # multiprocess_example_job.py
    # ---------------------------
    from pyats.easypy import run

    def main():
        run('multiprocess_example.py')


    # when the above is ran through pyats using, the following is the output.
    # note how tasklogs are split automatically per process
    #
    # bash$ pyats run job multiprocess_example_job.py
    #
    # Starting job run: multiprocess_example_job
    # Starting task execution: Task-1
    #     test harness = pyats.aetest
    #     testscript   = multiprocess_example.py
    # +------------------------------------------------------------------------------+
    # |                          Starting testcase Testcase                          |
    # +------------------------------------------------------------------------------+
    # +------------------------------------------------------------------------------+
    # |                         Starting section sleep_test                          |
    # +------------------------------------------------------------------------------+
    # Forked process 31682 started, log: /path/to/multiprocess_example_job.2015Sep14_10:06:13.zip&fn=TaskLog.Task-1:pid-31682&zp=1
    # sleeping for 3 seconds
    # done sleeping, fully recharged :)
    # The result of section sleep_test is => PASSED
    # +------------------------------------------------------------------------------+
    # |                          Starting section pool_test                          |
    # +------------------------------------------------------------------------------+
    # Forked process 31684 started, log: /path/to/multiprocess_example_job.2015Sep14_10:06:13.zip&fn=TaskLog.Task-1:pid-31684&zp=1
    # Forked process 31685 started, log: /path/to/multiprocess_example_job.2015Sep14_10:06:13.zip&fn=TaskLog.Task-1:pid-31685&zp=1
    # 0 * 0 == 0
    # 1 * 1 == 1
    # 2 * 2 == 4
    # 3 * 3 == 9
    # 4 * 4 == 16
    # 5 * 5 == 25
    # 6 * 6 == 36
    # 7 * 7 == 49
    # 8 * 8 == 64
    # 9 * 9 == 81
    # 12 * 12 == 144
    # 10 * 10 == 100
    # 13 * 13 == 169
    # 11 * 11 == 121
    # 14 * 14 == 196
    # 15 * 15 == 225
    # 16 * 16 == 256
    # 18 * 18 == 324
    # 17 * 17 == 289
    # 19 * 19 == 361
    # result = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361]
    # The result of section pool_test is => PASSED
    # The result of testcase Testcase is => PASSED
    # Finished task execution: Task-1

    # and the following are the contents of each log file:
    # TaskLog.Task-1
    # ---------------
    # 12: +------------------------------------------------------------------------------+
    # 13: |                          Starting testcase Testcase                          |
    # 14: +------------------------------------------------------------------------------+
    # 15: +------------------------------------------------------------------------------+
    # 16: |                         Starting section sleep_test                          |
    # 17: +------------------------------------------------------------------------------+
    # 18: Forked process 31682 started, log: /path/to/multiprocess_example_job.2015Sep14_10:06:13.zip&fn=TaskLog.Task-1:pid-31682&zp=1
    # 19: The result of section sleep_test is => PASSED
    # 20: +------------------------------------------------------------------------------+
    # 21: |                          Starting section pool_test                          |
    # 22: +------------------------------------------------------------------------------+
    # 23: Forked process 31684 started, log: /path/to/multiprocess_example_job.2015Sep14_10:06:13.zip&fn=TaskLog.Task-1:pid-31684&zp=1
    # 24: Forked process 31685 started, log: /path/to/multiprocess_example_job.2015Sep14_10:06:13.zip&fn=TaskLog.Task-1:pid-31685&zp=1
    # 25: result = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361]
    # 26: The result of section pool_test is => PASSED
    # 27: The result of testcase Testcase is => PASSED
    #
    # TaskLog.Task-1:pid-31685
    # -------------------------
    # 19: 9 * 9 == 81
    # 20: 10 * 10 == 100
    # 21: 11 * 11 == 121
    # 22: 15 * 15 == 225
    # 23: 16 * 16 == 256
    # 24: 17 * 17 == 289
    #
    # TaskLog.Task-1:pid-31684
    # -------------------------
    # 19: 0 * 0 == 0
    # 20: 1 * 1 == 1
    # 21: 2 * 2 == 4
    # 22: 3 * 3 == 9
    # 23: 4 * 4 == 16
    # 24: 5 * 5 == 25
    # 25: 6 * 6 == 36
    # 26: 7 * 7 == 49
    # 27: 8 * 8 == 64
    # 28: 12 * 12 == 144
    # 29: 13 * 13 == 169
    # 30: 14 * 14 == 196
    # 31: 18 * 18 == 324
    # 32: 19 * 19 == 361


Warnings
--------

When using ``multiprocessing`` module directly, beware of the following:

- users are responsible of gracefully handling and terminating their own
  processes. At the end of Easypy, all outstanding child processes are
  terminated without mercy. Dangling processes killed in this manner may leave
  the test environment in an undesirable state.

- resources such as testbeds, devices, device telnet/ssh connections & etc are
  shared system resources. Therefore, if you only have a single console
  connection to a device, sharing that connection between multiple processes
  will result in race conditions & deadlocks.
