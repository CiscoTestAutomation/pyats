.. _async_semaphores:

Semaphores
==========


.. sidebar:: Helpful Reading

    - `Semaphore`_

    - `Reentrant Mutex`_

    - `Mutex`_


.. _Semaphore: https://en.wikipedia.org/wiki/Semaphore_(programming)
.. _Mutex: https://en.wikipedia.org/wiki/Mutual_exclusion
.. _Reentrant Mutex: https://en.wikipedia.org/wiki/Reentrant_mutex

Semaphores are abstract data types used for controlling access, by multiple
processes, to a common resource. There is no "silver bullet" to when it comes to
resource sharing: Python ``multiprocessing`` module provides all the necessary 
tools, and users are expected to create their own semaphore implementations.

However, mutexes, especially reentrant mutexes, are a special type of binary
semaphore that are more commonly modelled. Therefore, this section focuses on 
particular implementations of reentrant mutexes that users can leverage and 
inherit.

.. _async_lockable:

Lockable
--------

``async.synchronize.Lockable`` is a class featured in the Async module that 
users can inherit directly from. It contains a built-in `Reentrant Mutex`_
``multiprocessing.RLock()``, allowing its subclass instances to be 
multiprocessing-safe, eg, its **method calls protected from multiprocessing 
race condition**, where only one process and/or thread can make a call at any 
given moment (eg, code-based locking).

The intention of this class is to facilitate the user in creating classes and
methods modeling resources that can be shared between multiple processes and
threads, without having to worry about internal implementation details. To take
advantage of it, simply inherit, and decorate all your "shared" methods using
``@Lockable.locked`` decorator. 

.. code-block:: python
    
    # Example
    # -------
    #
    #   async.synchronize.Lockable example

    from pyats.async_.synchronize import Lockable

    class MySharableClass(Lockable):

        def __init__(self):
            # make sure to always call Lockable class's __init__
            # (eg, via super)
            super().__init__()

        @Lockable.locked
        def do_work_one(self):
            pass

        @Lockable.locked
        def do_work_two(self):
            pass

``@Lockable.locked`` automatically adds method locking & unlocking to the 
decorated method: locks the instance when it is called, and unlocks after it
returns. As the internal locking mechaism is based on ``RLock()``, a locked
method can call another locked method internally (eg, ``do_work_one()`` calling
``do_work_two()`` in the above example) sans issues.

In addition to the decorator, this class also comes with two public methods:

``Lockable.acquire(blocking=True, timeout=None)``
    manually acquires the lock on this class instance. Instead of the decorator,
    users can call this api manually/directly within their implementations to 
    create a locking effect. 
    
    ``blocking``: controls whether to block until the lock is acquired, 
    defaulting to ``True``. 
    
    ``timeout``: controls the amount of time to wait for if ``blocking=True``, 
    defaulting to ``None`` (eg, indefinitly)
    
    Returns ``True``/``False`` based on whether lock was acquired or not. 

``Lockable.release()``
    Release lock. Only the current lock owner (process/thread) can call this
    method. Others receive an ``AssertionError``.

    Note that if ``acquire()`` was called multiple times due to recursion, 
    ``release()`` need to be called in the exact reverse order.

.. tip::
    
    keep in mind that this class only provides a **locking** capability to your
    class methods. If the class instance also contains live information such as
    resource states, those state attributes must be also shared (using things 
    like ``multiprocessing.Values``).
