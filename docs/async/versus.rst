Asynchronous Methods
====================

.. sidebar:: Helpful Reading

    - `asyncio`_

    - `Threading`_

    - `Multiprocessing`_

.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _Threading: https://docs.python.org/3/library/threading.html
.. _Multiprocessing: https://docs.python.org/3/library/multiprocessing.html

What are the different ways of asynchronously executing code within Python? What
are their pros and cons? which one should I use in my testscript? 

This section of the documentation attempts to answer the above questions 
systematically in an introductory manner, providing comparisons, insights and 
explanations. 

.. tip::

    the quick answer? For all intents and purposes, use **multiprocessing**.
    Not convinced? Read on.


.. _pyats_asyncio:

asyncio
-------

`asyncio`_ is a newly added module since Python 3.4. The main goal of this
module is to provide native Python support for coroutines, event loops, tasks
and asynchronous I/O. 

`asyncio`_, coroutines and event-loops are **not** true parallelism. They are
*concurrent* in the sense that their states are kept independent of each other,
but are not run in parallel: at any given time, only one of the coroutines is
running (whilst the others are suspended), irregardless of the number of
CPU/cores. Coroutines are **not** threads: whereas threads are run in parallel
at the same time, coroutines collaborate and only run one at a time.

Despite not being true "parallelism", where asyncio and coroutines truly
shine is when operations are I/O bound: the program consistently waits for I/O
instead of waiting for the CPU. It allows libraries to perform at "parallel 
like" performance without the limitations & overhead of multi-process and
multi-thread.

Should you use `asyncio`_? **Most likely not**. This module is intended not for
the general user: it's more designed for developers to write libraries on top
of it for other developers to use, such as Gevent_, Tornado_, and Eventlet_.
For your day-to-day test automation libraries and scripts, using `asyncio`_
will only add further unneccesary complexity.

.. note::
    
    `asyncio`_ is so new that it is still receiving updates, and is therefore
    provided on a *provisional basis* (eg, no backwards compatibility
    guarantee).

.. _Gevent: http://www.gevent.org/
.. _Tornado: http://www.tornadoweb.org/en/stable/
.. _Eventlet: http://eventlet.net/


Threading
---------

Python `Threading`_ module provides a very user-friendly interface to create, 
handle and manage threads within the current process. Threads are very
lightweight and also natively shares memory and objects within the same process.

On the surface, threading may look promising. However, there are a few downsides
to threading that makes it very dangerous and bug-prone:

    - cPython - `Global Interpreter Lock`_

    - **not interrutable and/or killable**

    - thread safety is a major concern: all shared object accesses needs to be 
      done using lock acquire/release.

    - race condition prone, drastically increases code complexity

.. _Global Interpreter Lock: https://wiki.python.org/moin/GlobalInterpreterLock

A hanging thread, hangs forever in python: threads **cannot** be killed. The use
of threads in Python requires careful designs & coding, revolving around the use
of object locks & such in order to make your code thread-safe.

Should you use `Threading`_? **Most likely not**. Everything you can do with 
threads, can also be done using `Multiprocessing`_ with much less code changes
required.

.. warning::

    pyATS infrastructure is not thread-safe. If you must, use threads only on
    your own libraries and functions.


Multiprocessing
---------------

Python `Multiprocessing`_ module allows users to spawn/fork child processes
using an API interface similar to that of `Threading`_ (and thus also very easy
to use). Here's some highlights of the benefits of using multiprocessing:

    - separate memory space: no race conditions (except with external systems)

    - very simple, straightforward code

    - no `Global Interpreter Lock`_, takes full advantage of multiple CPU/cores

    - child processes are easily interruptable/killable

Typically speaking, processes are slower to spawn than threads, and tends
to also use a larger memory footprint (due to separate memory spaces). However,
on Linux systems (which pyATS is designed to run on), process forks are 
extremely lightweight, and parent-child memory is mostly shared until it starts
to differ (due to memory writes). 

The main benefit of multiprocessing is that it doesn't require much speciality
code: because each process runs in its own, separate memory space, virtually all
functions can be run in parallel. This, combined with the light-weightness of
process forking makes it the perfect candidate for easy-parallelism in test 
automation.

Thus, for all intents and purposes, users of pyATS should be mostly focused with
using `Multiprocessing`_ module and functionalities. 


Final Thoughts
--------------

Each system exists for a reason: they each have their advantages and
disadvantages. However, for the purposes of test-automation, weighing the pros
and cons of each async method, `Multiprocessing`_ comes out easily ahead of
the bunch.

Does this mean you should avoid `asyncio`_ and `Threading`_ altogether? No. It
only means that unless you know exactly why you need to use them, stick with
`Multiprocessing`_.
