Introduction
============

.. sidebar:: Helpful Reading

    - `Threading`_

    - `Multiprocessing`_

.. _Threading: https://docs.python.org/3/library/threading.html
.. _Multiprocessing: https://docs.python.org/3/library/multiprocessing.html

Asynchronous (async) execution defines the ability to run programs and functions
in parallel and (possibly) independent of the main program flow. The proper use 
of async execution can greatly improve of performance of a program, and is only
bounded by the physical number of CPUs and I/O limits.

This module & documentation provides the insights, concepts and tools within 
pyATS that supports asynchronous execution, allowing users to reap the full
benefit of async without having to deal with its logistics & overhead.

    *those who don't. There are 0b10 types of people in the world: those who 
    understand asynchronous jokes and*

Intentions
----------

The intent of this module is not to reinvent asynchronous execution: Python's 
built in library `Threading`_ and `Multiprocessing`_ already provides a great
basis to do so, are quite powerful and user-friendly. 

However, these libraries only provides a foundation to further build on. It is 
still up to the end user to write boilerplate code to handle and configure 
things like:

    - managing of log files
    - re-establishing lost connections, sessions
    - resource sharing & locking (such as telnet/ssh connections)
    - two-way inter-process communication and state synchronization

Therefore, the intent of this module is:

    *to strengthen pyATS's support of asynchronous execution, automate some of 
    the above items, and further streamlining the user experience.*

However, keep in mind that not everything can be done within this module alone:
in order to properly support asynchronous execution, each module/package has
to be individually overhauled with parallelism in mind. Thus, this module
documentation also serves as a central location where these concepts and changes
are consolidated and shared in a overviewing fashion.
