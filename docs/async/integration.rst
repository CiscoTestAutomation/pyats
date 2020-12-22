Module Integration
==================

.. sidebar:: Helpful Reading

    - `Multiprocessing`_

    - `POSIX Shared Memory`_

    - `/dev/shm`_

.. _Multiprocessing: https://docs.python.org/3/library/multiprocessing.html
.. _POSIX Shared Memory: https://en.wikipedia.org/wiki/Shared_memory_(interprocess_communication)#Support_on_Unix-like_systems
.. _`/dev/shm`: http://www.cyberciti.biz/tips/what-is-devshm-and-its-practical-usage.html


As previously discussed in introduction, the existence of ``async`` module
in pyATS mostly serves as a central location where concepts & integrations of
parallel execution efforts/mechanisms are consolidated and documented.

The following is an overview of all current pyATS asynchronous execution
specific code & features.


Multiprocessing
---------------

Python ``multiprocessing`` library is used throughout pyATS as the de-facto
standard in parallel processing & asynchronous execution, with ``fork`` being
always used as the context for creating child processes.

Multiprocessing_ library features `Pipes/Queues`_ and `Shared ctype Objects`_
that facilitates inter-process communication and process synchronizations. Where
applicable, pyATS modules should automatically set them up for process state
synchronization.

Forking_ is always used to create child processes. Child processes created using
``fork`` automatically inherit its parent resources (where applicable).


.. _`Pipes/Queues`: https://docs.python.org/3.4/library/multiprocessing.html#pipes-and-queues
.. _Shared ctype Objects: https://docs.python.org/3.4/library/multiprocessing.html#shared-ctypes-objects
.. _Forking: https://en.wikipedia.org/wiki/Fork_(system_call)

.. note::

    Multiprocessing_ uses `POSIX Shared Memory`_ to create pipes, queues &
    shared variables. On Linux devices, this requires `/dev/shm`_ to be read and
    writable by your processes. The typical/default permission on this folder
    should be: ``drwxrwxrwt`` (or ``0o1777``).



Pickle
------

Pickling describes the method of serializing and de-serializing Python objects.
Due to the nature of inter-process communication, all objects passed/shared
through `Pipes/Queues`_ needs to be *pickleable* by the Python `pickle`_ module.

Essentially, objects are converted into byte streams during pickling, and
reconstructed in the unpickling inverse operation. All Python objects are
pickled before they are sent through `Pipes/Queues`_ in Multiprocessing_, and
automatically reconstructed (unpickled) in the other end.

However, keep in mind that because objects are serialized and reconstructed,
they are effectively two *copies*, eg: different instances of the same type of
objects. As well, pickle_ typically only restores object structure and value,
and does not restore external states if the object represent external systems
(such as telnet/ssh conenction classes, etc). Such states (eg, ssh connection)
would need to be restored/reconnected using the reconstructed object.

.. code-block:: python

    # Example
    # -------
    #
    #   pickling and unpickling

    import pickle

    # create an object
    # create a datastructure
    data = dict(name = 'tony stark',
                callsign = 'ironman',
                also_known_as = ('genius',
                                 'billionaire',
                                 'playboy',
                                 'philanthropist'))

    # pickle the data into a bytestream
    serialized_data = pickle.dumps(data)

    # this is what pickled data looks like (split lines)
    # b'\x80\x03}q\x00(X\x08\x00\x00\x00callsignq\x01X\x07\x00\x00\x00ironmanq
    # \x02X\x04\x00\x00\x00nameq\x03X\n\x00\x00\x00tony starkq\x04X\x0b\x00\x00
    # \x00alsoknownasq\x05(X\x06\x00\x00\x00geniusq\x06X\x0b\x00\x00\x00
    # billionaireq\x07X\x07\x00\x00\x00playboyq\x08X\x0e\x00\x00\x00
    # philanthropistq\ttq\nu.'

    # unpickle recreates the data structure
    reconstructed_data = pickle.loads(serialized_data)

    # data is the same before and after pickling
    assert data == reconstructed_data
    # True

    # however, they are two different copies (different object id)
    id(data)
    4151360332
    id(reconstructed_data)
    4151476044

.. _pickle: https://docs.python.org/3.4/library/pickle.html


Easypy
------

Easypy uses ``multiprocessing`` to fork child processes per each jobfile tasks.
This allows each task (and its corresponding testscript) to run within its own
memory space, independent of each other.

.. code-block:: text

    Pictorial View of Easypy Processes
    ----------------------------------

    +--------------------+    fork     +----------------------------+
    | easypy  (pid 1000) |-------------| Reporter Server (pid 1001) |
    +--------------------+             +----------------------------+
               |
               | fork          +-------------------------+
               +---------------| Task Task-1 (pid 1002) |
               |               +-------------------------+
               |
               | fork          +-------------------------+
               +---------------| Task Task-2 (pid 1003) |
               |               +-------------------------+
              etc.

The overall result of each task is automatically piped back to the job file as
``Task.result`` attribute.

In addition, Easypy also performs the following to enable hands-off
``multiprocessing`` usage in user Tasks:

    - ``TaskLogHandler``: enable auto-create new log file per forked process.

    - ``ReportClient``: enable auto-reconnect to Reporter server in forked
      processes.

    - re-open ``/dev/stdin`` as ``sys.stdin`` to enable ``pdb`` debugger to work
      within task processes when AEtest flag ``pdb = True`` is detected.


Logging
-------

Python ``logging`` is not process-aware (it is thread safe, though). It is
typically up to the user to reconfigure ``logging`` to emit to different log
files per process.

When executing through Easypy environment, Easypy automatically attaches
``TaskLogHandler`` to logging so that one TaskLog is created per Task. In
addition, Easypy also configures it so that when forks of a Task process is
created, a new log file is also automatically created.

This protocol is documented in detail in :ref:`log_multiprocessing`.


Reporter
--------

Easypy uses :ref:`reporter` to aggregate Task result reports. This is a Unix
socket-based server-client model, with each Task having its own
``ReportClient`` connection client object that talks to the parent ``Reporter``
server.

As ``AERunner`` server is client/pid aware, when a process is forked,
``AEclient`` instances within the forked process needs to reconnect to the
server before issuing further calls. Within Easypy, this is automatically
handled: the default client object is configured so that upon forking, the
child process client automatically re-establishes its link to the server.

This protocol is documented in detail in :ref:`log_multiprocessing`.
