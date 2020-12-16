.. _async_pcall:

Parallel Call
=============

Parallel call ``pcall`` is an API provided by ``async`` module that supports
calling procedures and functions in parallel using ``multiprocessing`` fork,
without having to write boilerplate code to handle the overhead of process
creation, waiting and terminations.

``pcall`` supports calling any and all procedures, functions and methods in
parallel, as long as they satisfy the following requirements:

    - the return of called target must be a **pickleable** object.
      (refer to: `What can be pickled`_)

Consider ``pcall`` as a shortcut library to ``multiprocessing``, intended to
satisfying most users' need for parallel processing. However, for more custom
& advanced use cases, stick with direct usages of ``multiprocessing``.

.. _What can be pickled: https://docs.python.org/3.4/library/pickle.html#what-can-be-pickled-and-unpickled


Usages
------

``pcall`` API allows users to call any function/method (a.k.a. **target**) in
parallel. It comes with the following built-in features:

    - builds arguments for each child process/instance

    - creates, handles and gracefully terminates all processes

    - returns target results in their called order

    - re-raises child process errors in the parent process


.. code-block:: python

    # Example
    # -------
    #
    #   a simple parallel call

    # import pcall
    from pyats.async_ import pcall

    # define a function to be called in parallel
    def add(x, y):
        return x + y

    # invoke parallel calling of the above function
    # to calculate 1 + 4, 2 + 5, 3 + 6
    result = pcall(add, x = (1, 2, 3), y = (4, 5, 6))
    # (5, 7, 9)

In essense, arguments to ``pcall`` are zipped together to create multiple calls
to the given target(s), and run concurrently through forked child processes.
The number of child processes forked is automatically optimized based on the
number of target calls, arguments and so on.

``pcall`` argument builder is coded with python ``zip``, and follows the ``zip``
mentality: the iterator stops when the shortest input iterable is exhausted,
instead of throwing an exception about iterable length mismatches.

The final results of all child processes is automatically aggregated together
into a tuple and returned to the user. The order of these results appear exactly
as the order of arguments provided and used to built/launch each child process
with.

.. csv-table:: Pcall Argument List
    :header: "Argument", "Description"

    ``targets``, "a single, or a list of callable targets to be invoked in
    parallel"
    ``timeout``, "max runtime of any single child process in seconds"
    ``cargs``, "positional arguments common to all target calls"
    ``iargs``, "list of specific positional argument for each target"
    ``ckwargs``, "keyword-arguments common to all target calls"
    ``ikwargs``, "list of specific keyword arguments for each target"
    ``varkwargs``, "any other variable keyword arguments and value lists for
    each target"

Do not be discouraged by the above list of available arguments: they're mostly
optional. The intent is to present an interface sufficient for all possible
types of usages scenarios. The examples below cover most of the useful
combinations.


Single Target
-------------

When only a single **target** function is passed through ``pcall``, the number
of parallel instances is controlled by the number of instance arguments. If
both positional and keyword instance arguments are used together, their numbers
of iterations must match, otherwise any extra iterations are tossed away.
This is inline with  Python ``zip()`` function behavior.

.. code-block:: python

    # Example
    # -------
    #
    #   pcall argument combinations (single target)
    #   (using a lot of tuples instead of lists)

    # import pcall
    from pyats.async_ import pcall

    # define a function to be called by pcall
    # (this function returns all of its arguments back to the caller)
    def func(*args, **kwargs):
        return (args, kwargs)

    # positional argument building
    # ----------------------------
    #   child 1: args=(1, 2, 3, 4), kwargs= {}
    #   child 2: args=(1, 2, 3, 5), kwargs= {}
    #   child 3: args=(1, 2, 3, 6), kwargs= {}
    pcall(func, cargs = (1, 2, 3),
                iargs = ((4,), (5,), (6,))

    # keyword argument building
    # -------------------------
    #   child 1: args=(), kwargs= {'a': 1, 'b': 2, 'c': 3}
    #   child 2: args=(), kwargs= {'a': 1, 'b': 2, 'c': 4}
    #   child 3: args=(), kwargs= {'a': 1, 'b': 2, 'c': 5}
    pcall(func, ckwargs = {'a': 1, 'b': 2},
                ikwargs = [{'c': 3},
                           {'c': 4},
                           {'c': 5}])

    # variable keyword argument building
    # ----------------------------------
    #   child 1: args=(), kwargs= {'x': 1, 'y': 4, 'z': 7}
    #   child 2: args=(), kwargs= {'x': 2, 'y': 5, 'z': 8}
    #   child 2: args=(), kwargs= {'x': 3, 'y': 6, 'z': 9}
    pcall(func, x = (1, 2, 3),
                y = (4, 5, 6),
                z = (7, 8, 9))

    # combo is always fun
    # -------------------
    #   child 1: args=(1, 2, 3, 6, 7),
    #            kwargs= {'a': 1, 'b': 2, 'c': 3, 'x': 10, 'y': 100}
    #   child 2: args=(1, 2, 3, 8, 9),
    #            kwargs= {'a': 1, 'b': 2, 'c': 4, 'x': 20, 'y': 200}
    pcall(func, cargs = (1, 2, 3),
                iargs = ((6, 7), (8, 9)),
                ckwargs = {'a': 1, 'b': 2},
                ikwargs = ({'c': 3}, {'c': 4}),
                x = (10, 20), y = (100, 200))

    # iargs and ikwargs's number of iterations must match
    # ---------------------------------------------------
    #   child 1: args=(1, 2), kwargs= {'a': 1}
    #   child 2: args=(3, 4), kwargs= {'a': 2}
    # there is no child #3, as there is no ikwargs to match (5, 6) of iargs
    pcall(func, iargs = ((1, 2), (3, 4), (5, 6)),
                ikwargs = ({'a': 1}, {'a': 2}))


Multiple Targets
----------------

When a **list of target** functions is provided to ``pcall``, each target is run
within its own child process, and elements of ``iargs`` and ``ikwargs`` directly
corresponds to each target in the same order as they appear.

.. code-block:: python

    # Example
    # -------
    #
    #   pcall argument combinations (multiple target)
    #   (using a lot of lists this time for a change)

    # import pcall
    from pyats.async_ import pcall

    # define a couple function to be called by pcall
    def func1(*args, **kwargs):
        return dict(name = 'func1', arg = args, kwargs = kwargs)

    def func2(*args, **kwargs):
        return dict(name = 'func2', arg = args, kwargs = kwargs)

    def func3(*args, **kwargs):
        return dict(name = 'func3', arg = args, kwargs = kwargs)

    # positional argument building
    # ----------------------------
    #   child 1: name='func1', args=(1, 2, 3, 4, 5, 6), kwargs={}
    #   child 2: name='func2', args=(1, 2, 3, 7, 8, 9), kwargs={}
    #   child 3: name='func3', args=(1, 2, 3, 9, 10, 11), kwargs={}
    pcall([func1, func2, func3], cargs = [1, 2 ,3],
                                 iargs = [[4, 5, 6], [7, 8, 9], [9, 10, 11]])

    # keyword argument building
    # ----------------------------
    #   child 1: name='func1', args=(), kwargs={'a': 1, 'b': 2, 'c': 3}
    #   child 2: name='func2', args=(), kwargs={'a': 1, 'b': 2, 'c': 4}
    #   child 3: name='func3', args=(), kwargs={'a': 1, 'b': 2, 'c': 5}
    pcall([func1, func2, func3], ckwargs = {'a': 1, 'b': 2},
                                 ikwargs = [{'c': 3},
                                            {'c': 4},
                                            {'c': 5}])

    # combine it all together
    # -----------------------
    #   child 1: name='func1',
    #            args=(1, 2, 3, 6, 7),
    #            kwargs= {'a': 1, 'b': 2, 'c': 3, 'x': 10, 'y': 100}
    #   child 2: name='func2',
    #            args=(1, 2, 3, 8, 9),
    #            kwargs= {'a': 1, 'b': 2, 'c': 4, 'x': 20, 'y': 200}
    pcall([func1, func2], cargs = (1, 2, 3),
                          iargs = ((6, 7), (8, 9)),
                          ckwargs = {'a': 1, 'b': 2},
                          ikwargs = ({'c': 3}, {'c': 4}),
                          x = (10, 20), y = (100, 200))

    # as usual, iargs and ikwargs's number of iterations must match
    # -------------------------------------------------------------
    #   child 1: name='func1', args=(1, 2), kwargs= {'a': 1}
    #   child 2: name='func2', args=(3, 4), kwargs= {'a': 2}
    # there is no child #3, as there is no ikwargs to match (5, 6) of iargs, and
    # thus not enough knowledge on how to call func3
    pcall([func1, func2, func3], iargs = ((1, 2), (3, 4), (5, 6)),
                                 ikwargs = ({'a': 1}, {'a': 2}))

Errors and Timeouts
-------------------

When exceptions occur in child processes invoked by ``pcall``, they are caught,
and re-raised within the calling process as ``ChildProcessException``. The
details and traceback of the original exception is attached as the *cause* of
this ``ChildProcessException``.

.. note::

    this is only available in python-3. In python-2, only the exception message
    is raised (without traceback). This is a limitation of python-2 language.

When child processes exceed the provided ``timeout`` value, ``SIGTERM`` is sent
to each child process, and ``TimeoutError`` is raised in the calling process.

Logging
-------

By default, each Pcall process will log to its own forked tasklog file while it
runs. This ensures that concurrent log messages are not interleaved within the
same file.

Once the Pcall finishes (eg, ``Pcall.join()`` is called), the log files will
automatically be joined into the main tasklog, with each process having its own
section.

.. code-block:: text

    2: SERVER: 2018-10-09T13:47:46: %LOG-6-INFO: >>>> Begin child log /path/to//basic_example_job.2018Oct09_13:47:44.782943/TaskLog.Task-1:pid-88466
    3: SERVER: 2018-10-09T13:47:46: %SCRIPT-6-INFO: this is a message from 88466
    4: SERVER: 2018-10-09T13:47:46: %LOG-6-INFO: <<<< End child log /path/to//basic_example_job.2018Oct09_13:47:44.782943/TaskLog.Task-1:pid-88466
    2: SERVER: 2018-10-09T13:47:46: %LOG-6-INFO: >>>> Begin child log /path/to//basic_example_job.2018Oct09_13:47:44.782943/TaskLog.Task-1:pid-88467
    3: SERVER: 2018-10-09T13:47:46: %SCRIPT-6-INFO: this is a message from 88467
    4: SERVER: 2018-10-09T13:47:46: %LOG-6-INFO: <<<< End child log /path/to//basic_example_job.2018Oct09_13:47:44.782943/TaskLog.Task-1:pid-88467
    2: SERVER: 2018-10-09T13:47:46: %LOG-6-INFO: >>>> Begin child log /path/to//basic_example_job.2018Oct09_13:47:44.782943/TaskLog.Task-1:pid-88468
    3: SERVER: 2018-10-09T13:47:46: %SCRIPT-6-INFO: this is a message from 88468
    4: SERVER: 2018-10-09T13:47:46: %LOG-6-INFO: <<<< End child log /path/to//basic_example_job.2018Oct09_13:47:44.782943/TaskLog.Task-1:pid-88468


Pcall Object
------------

``pcall`` API is atually a classmethod of ``Pcall`` class, intended to further
minimize the number of lines of boilerplate code in user libraries and scripts.
You can instantiate your own instances of ``Pcall`` to poll and control the
forked parallel processes.

``Pcall`` class methods are similar to those of ``multiprocessing.Pool``. In
fact, they only differ in the following:

    - ``Pool`` allows users to create a fixed number of worker processes to do
      generic processing. ``Pcall`` automatically creates processes based on
      user inputs and only runs the given procedure/function once.

    - ``Pcall`` builds argument for each function/process. ``Pool`` expects the
      user to provide it the exact arguments per invocation.

.. csv-table:: Pcall Class Methods/Properties
    :header: "Attribute", "Description"

    ``__init__``, "takes in the exact same arguments as ``pcall``"
    ``pids``, "tuple of all child processes"
    ``living``, "tuple of all currently alive child processes"
    ``results``, "tuple of results from all child processes. None if no results
    currently available"
    ``start()``, "starts all child worker processes"
    ``join()``, "blocks the current process and wait for all childs to finish,
    or until ``timeout`` is reached"
    ``terminate()``, "terminates all children processes with SIGTERM"

Once all processes are started using ``start()`` method, make sure to call
``join()`` so that results can be collected. ``results`` defaults to ``None``
when the process has not yet started, or joined.

.. code-block:: python

    # Example
    # -------
    #
    #   using the Pcall class

    from pyats.async_ import Pcall

    # define a function to be called in
    def add(x, y):
        return x + y

    # create a Pcall object
    p = Pcall(add, x = (1, 2, 3), y = (4, 5, 6))

    # start all child processes
    p.start()

    # wait for everything to finish
    p.join()

    # collect results
    results = p.results
