Connection Sharing
==================

.. sidebar:: Helpful Reading

    - :ref:`async_semaphores`

    - `Object Pool Pattern`_

    - `Reentrant Mutex`_

    - `Mutex`_


.. _Mutex: https://en.wikipedia.org/wiki/Mutual_exclusion
.. _Reentrant Mutex: https://en.wikipedia.org/wiki/Reentrant_mutex
.. _Object Pool Pattern: https://en.wikipedia.org/wiki/Object_pool_pattern

Connections are typically synchronous resources, eg, each may be only used
by one process/thread/object at a time. Simultaneous accesses to the same 
connection (by different process/thread) typically ends up in a race condition,
with both ends failing to get what they needed and the output garbled.

This section of the documentation intends to help users to create connection
implemetations that are **sharable** by avoiding deadlocks through the use of
mutexes (mutual exclusions) and connection pools.


Method Locks
------------

One simple way to share a connection between multiple processes/threads is
through the use of `Mutex`_: assuming all actions (eg, send/receive) through
the connection pipeline is done only by calling class methods, locking up the
connection instance during method calls is an effective way to prevent 
`race conditions`_.

When a :ref:`connection_class` is first implemented following basic guidelines,
the resulting connection instances are synchronous resources and cannot yet be
shared. To add locking behavior, take advantage of the fact that 
``BaseConnection`` inherits from :ref:`async_lockable` parent class: use the
``@BaseConnection.locked`` decorator on methods that are prone to race conditions
when called simultaneously.

.. code-block:: python

    # Example
    # -------
    #
    #   adding locking & unlocking to our rudimentary telnetlib implementation

    import telnetlib

    from pyats.connections import BaseConnection

    class TelnetConnection(BaseConnection):
        '''TelnetConnection

        the same TelnetConnection class as previous chapter, now with locking
        '''

        def __init__(self, *args, **kwargs):
            # ...
            # same code as before

        @BaseConnection.locked
        def connect(self):
            # ...
            # same code as before

        @BaseConnection.locked
        def send(self, text):
            # ...
            # same code as before

        @BaseConnection.locked
        def receive(self):
            # ...
            # same code as before

        @BaseConnection.locked
        def execute(self, command):
            # ...
            # same code as before

        @BaseConnection.locked
        def configure(self, *args, **kwargs):
            # ...
            # same code as before

As we now applied locking & unlocking to all **actions**, whenever a process
or threads makes a call to the decorated api, the object is locked, and all
subsequent calls will have to wait until the lock is released. For more 
information on how the locks behave, refer to :ref:`async_lockable` class
documentation.

.. code-block:: python

    # Example
    # -------
    #
    #   demonstrating the above code in a multiprocessing environment
    #   (using async_.pcall as an example)

    from pyats.async_ import Pcall

    # assuming we had an imaginary device object...

    # using the above device and TelnetConnection, create a session
    device.connect(cls = TelnetConnection, via = 'console')

    # now let's use Pcall to perfrom two commands at the same time
    # in forked, child processes
    output = Pcall(device.execute, 
                   command = ['show version', 'show running-config'])

In the above example, if ``TelnetConnection`` was not multiprocessing-safe, both
processes would try to issue commands at approximately the same time, and the
connection would fizzle. When it is properly coded using locks, whichever 
process that first issues the command - would **lock** the session until it is 
done. The 2nd process would have to wait until it could acquire the lock, before
it can issue its command.

.. figure:: mutex_flow.png
    :align: center

However, keep in mind that this is only a primitive first step towards proper
connection-sharing in a multiprogramming environment. Through the use of 
code-locks, actions which uses the connection pipe is now safe from collisions. 
However, if any live connection state are stored within the objects, these
attributes would need to also be locked & shared (via the use of eg
``multiprocessing.Values``). This is an implementation detail to be performed on
a per-design basis.

.. tip::

    no, this is not true asynchronous execution - it is only an effective 
    measure in avoiding multiprogramming deadlocks by serializing connection 
    usages from different processes. 

.. _race conditions: https://en.wikipedia.org/wiki/Race_condition


.. _connectionpool:

Connection Pools
----------------

Connection pool is a feature-add to ``ConnectionManager``, allowing multiple of
the same type of connections (a.k.a. **workers**) to be pooled under the same 
alias, distributing action requests to any free workers within the pool in a
multiprogramming environment.

Connection pool operates under a **first come first serve** model, where
a free worker is allocated to the first requestor to do its desired work. The 
following sets of rules governs this behavior:

- a pool consists of multiple identical connections (type & path) called 
  workers.

- each action request is allocated a free worker. This worker is locked until
  the work to be performed is completed.

- if no free workers are present, the pool allocator waits until a free one is
  available (until timeout).

.. figure:: pool_flow.png
    :align: center

In effect, pools look & behave like any other :ref:`connection_class`: each 
carries its own unique ``alias``, has a path ``via``, and is of a certain type 
of connection implementation ``target``. The key difference is that it manages
multiple connections of that type (governed by ``pool_size``), and is started
using ``ConnectionManager.connect(pool_size=N)`` API.

.. code-block:: python

    # Example
    # -------
    #
    #   connection pool using TelnetConnection class example
    #   (and Pcall to make asynchronous executions)

    from pyats.async_ import Pcall

    # assuming we had an imaginary device object...

    # using the above device and TelnetConnection
    # create a pool of 5 workers
    device.connect(target = TelnetConnection, 
                   via = 'mgmt',
                   pool_size = 5)

    # now let's use Pcall to perfrom 5 commands at the same time
    # in forked, child processes
    output = Pcall(device.pool.execute, 
                   command = ['show version', 
                              'show running-config',
                              'show ip ospf database',
                              'show ip route',
                              'show ip bgp'])

By default, if all workers are currently busy, new requests will wait 
indefinitely until a worker is freed to do its deeds. This behavior can be 
changed by setting a timeout value: ``connect(..., pool_timeout=x)``, 
where ``x`` is an integer in seconds. If a worker cannot be allocated in 
the given time frame, a ``TimeoutError`` exception is raised.

.. note::

    keep in mind that if any action changes the states and/or configuration of
    a worker connection, it will linger around. As workers are freely 
    distributed with work, these lingering changes may negatively affect your
    testing.
