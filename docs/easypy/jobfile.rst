Jobfile & Tasks
===============

In pyATS, the aggregation of multiple testscripts together and executed within
the same runtime environment is called a **job**.

The concept of Easypy revolves heavily around the execution of such **jobs**.
Each **job** corresponds to a ``jobfile``: a standard python file containing the
*instructions* of which testscripts to run, and *how* to run them.

During runtime, these testscripts are launched as **tasks** and executed through
a test harness (eg, ``aetest``). Each **task** is always encapsulated in its own
child process. The combined **tasks** in the same jobfile always share the same
system resources, such as testbeds, devices and their connections.


.. _easypy_jobfile:

Jobfiles
--------

Jobfiles are the bread and butter of Easypy. It allows aggregation of multiple
testscripts to run under the same environment as tasks, sharing testbeds, and
archiving their logs and results together. It is an excellent method to batch
and/or consolidate similar testscripts together into relevant result summaries.

Jobfiles are required to satisfy the following criterion:

    - each job file must have a ``main()`` function defined. This is the main
      entry point of a job file run.

    - the ``main()`` function accepts an argument called ``runtime``. When
      defined, the engine automatically passes the current :ref:`easypy_runtime`
      object in.

    - inside the ``main()`` function, use ``easypy.run()`` or ``easypy.Task()``
      to define and run individual testscripts as :ref:`easypy_tasks`.

    - the name of the job file, minus the ``.py`` extension, becomes this job's
      reporting name. This can be modified by setting ``runtime.job.name``
      attribute.

Jobfiles are provided as the only mandatory argument to the ``easypy`` launcher.

.. code-block:: python

    # Example
    # -------
    #
    #   a simple, sequential job file

    import os

    from pyats.easypy import run

    # main() function must be defined in each job file
    #   - it should have a runtime argument
    #   - and contains one or more tasks
    def main(runtime):
        
        # provide custom job name for reporting purposes (optional)
        runtime.job.name = 'my-job-overwrite-name'

        # using run() api to run a task
        #
        # syntax
        # ------
        #   run(testscript = <testscript path/file>,
        #       runtime = <runtime object>,
        #       max_runtime = None,
        #       taskid = None,
        #       **kwargs)
        #
        #   any additional arguments (**kwargs) to run() api are propagated
        #*  to AEtest as input arguments.
        run(testscript = 'script_one.py', runtime = runtime)

        # each job may contain one or more tasks.
        # tasks defined using run() api always run sequentially.
        run(testscript = 'script_two.py', runtime = runtime)

        # access runtime information, such as runtime directory
        # eg, save a new file into runtime directory
        with open(os.path.join(runtime.directory, 'my_file.txt')) as f:
            f.write('some content')

In essence, the jobfile is just a python program file, with ``main()`` defined
as the mandatory point of entry for all tasks' execution. As it is a program
file, it allows the user to write code that processes environment variables into
testscript inputs and processes any additional script arguments following
the :ref:`argument propagation scheme <easypy_argument_propagation>`.

.. code-block:: python

    # Example
    # -------
    #
    #   job file with environment variable processing

    import os
    from pyats.easypy import run

    # using this file's path to compute the relative location of script file
    # and collecting some arguments from environment variables
    here = os.path.dirname(__file__)
    argA = os.environ.get('SCRIPT_ARG_A', 'argument value a')
    argB = os.environ.get('SCRIPT_ARG_B', 'argument value b')

    # entry point
    def main(runtime):

        # relative script path/file based on this file's location
        run(testscript = os.path.join(here, 'path', 'to', 'script_one.py'),
            runtime = runtime)


        # passing script arguments collected from environment variable
        run(testscript = os.path.join(here, 'path', 'to', 'script_two.py'),
            runtime = runtime,
            argument_A = argA,
            argument_B = argB)

.. note::

    an exception will be thrown if your job file is empty or does not
    contain a ``main()`` definition.


.. _easypy_tasks:

Tasks
-----

An Easypy **task** is essentially a testscript being executed by a test-harness
like ``aetest`` in a child process. They exhibit the following properties:

    - each task is encapsulated in its own child process, forked from main
      easypy program.

    - each task contains a single :ref:`tasklog` where all messages are logged
      to.

    - all tasks report to their results via :ref:`reporter`.

    - the rolled up script result of each task is returned to the caller.

Tasks are created inside a jobfile's ``main()`` function by either calling the
shortcut :ref:`easypy_run_api` or by creating your own task objects using the
:ref:`easypy_task_class`.

Tasks may be run *sequentially* (in series), or *asynchronously* (in parallel).
This control is left entirely to the hands of the user. Each task is associated
with a unique task id, and can be controlled in the same fashion as all other
python processes.

.. tip::

    when a task is running, its Linux process name shows up as ``easypy task:
    <taskid> - <testscript>``


.. warning::

    even if tasks are run sequentially, it is still possible for a prior task
    to crash and leave the testbed in a dangling state, causing the next task
    to fail.

.. warning::

    keep in mind that even though tasks may be run in parallel, they are still
    sharing the same testbed and devices under-test. Users are expected to be
    aware of the requirements of each task (testscript), and avoid all race
    conditions between parallel-running tasks.


.. _easypy_run_api:

run() API
---------

``run()`` api is a shortcut to :ref:`easypy_task_class` for running tasks in
a sequential (serial) fashion. It helps the user to avoid boilerplate code that
handles ``Task`` class overheads, and always performs the following:

    - create & start a ``Task()`` with the given arguments

    - wait for it to finish (optionally, safeguard against runaway situations
      with ``max_runtime``)

    - return the task's result back to the caller.

.. csv-table:: run() Function Arguments
    :header: "Argument", "Description"

    ``testscript``, "testscript to be run in this task"
    ``taskid``, "unique task id (defaults to ``Task-#`` where # is an
    incrementing number)"
    ``max_runtime``, "maximum tax runtime in seconds before termination"
    ``runtime``, "easypy runtime object"
    ``kwargs``, "any other keyword-arguments to be passed to the testscript
    as script parameters"

.. code-block:: python

    # Example
    # -------
    #
    #   job file run() api example

    from pyats.easypy import run

    # main() function
    def main(runtime):

        # using run() api to run a task, save the result to variable
        # (max runtime = 60*5 seconds = 5 minutes)
        result = run(testscript = 'script_one.py',
                     runtime = runtime,
                     taskid = 'example_task_1',
                     max_runtime = 60*5)

        # check whether the next script should continue
        # based on previous task's results.
        if result:
            # last result passed, run the next task
            run(testscript = 'script_two.py',
                runtime = runtime,
                taskid = 'example_task_1',
                max_runtime = 60*5)


.. warning::

    all forward slash ``/`` found in the ``taskid`` are replaced with an
    underscore ``_``.


.. _easypy_task_class:

Task Class
----------

``Task`` class objects represent the task/testscript being executed in a child
process. It is a subclass of Python ``multiprocessing.Process`` class, and
always uses ``multiproessing.get_context('fork')`` to fork and create child
processes.

.. csv-table:: Task Class Arguments
    :header: "Argument", "Description"

    ``testscript``, "testscript to be run in this task"
    ``taskid``, "unique task id (defaults to ``Task-#`` where # is an
    incrementing number)"
    ``runtime``, "easypy runtime object"
    ``kwargs``, "any other keyword-arguments to be passed to the testscript
    as script parameters"

Like its parent ``Process`` class, instantiating a ``Task`` object does not
create the actual child process: the class constructor only sets internal states
and pipes, preparing for a process fork. The task is started only when its
``start()`` method is called to start the child process's activity.

.. code-block:: python

    # Example
    # -------
    #
    #   job file tasks using Task() api (sequential execution)
    #   (recreating the same job file as run() api example using Task class)

    from pyats.easypy import Task

    # main() function
    def main(runtime):

        # using Task class to create a task object
        # (max runtime = 60*5 seconds = 5 minutes)
        task_1 = Task(testscript = 'script_one.py',
                      runtime = runtime,
                      taskid = 'example_task_1')

        # start the task
        task_1.start()

        # wait for a max runtime of 60*5 seconds = 5 minutes
        task_1.wait(60*5)

        # check whether the next script should continue
        # based on previous task's results.
        if task_1.result:
            # last result passed, run the next task
            task_2 = Task(testscript = 'script_two.py',
                          runtime = runtime,
                          taskid = 'example_task_1')

            # start & wait
            task_2.start()
            task_2.wait(60*5)

The main advantage of using ``Task`` class directly is the ability to run tasks
asynchronously (in parallel), and an added level of more granular controls over
each task process.

.. code-block:: python

    # Example
    # -------
    #
    #   job file tasks using Task() api (asynchronous execution)

    import time
    from datetime import datetime, timedelta
    from pyats.easypy import Task

    # main() function
    def main(runtime):

        # using Task class to create a two tasks
        # (max runtime = 60*5 seconds = 5 minutes)
        task_1 = Task(testscript = 'script_one.py',
                      runtime = runtime,
                      taskid = 'example_task_1')

        task_2 = Task(testscript = 'script_two.py',
                      runtime = runtime,
                      taskid = 'example_task_1')

        # start both tasks simultaneously
        task_1.start()
        task_2.start()

        # poll for tasks to finish (max of 5minutes)
        counter = timedelta(minutes = 5)

        while counter:
            # check if processes are alive, if so, continue to wait
            if task_1.is_alive() or task_2.is_alive():
                time.sleep(1)
                counter -= timedelta(seconds=1)
            else:
                # all is good
                break
        else:
            # exceeded runtime
            task_1.terminate()
            task_1.join()
            task_2.terminate()
            task_2.join()

            # raise exception
            raise TimeoutError('Not all tasks finished in 5 minutes!')

Easypy expects all tasks to be finished/terminated when ``main()`` scope is
exited (eg, the jobfile finished execution). Therefore, all tasks created and
started using ``Task`` class should always be waited for using ``wait()``, and
properly handled/terminated by the user.

If  ``wait()`` is not called and/or there are tasks left dangling after exiting
``main()`` function scope, they are abruptly terminated, and reported to the
user in the report email as an exception/error.

``Task`` objects have the following methods & properties:

``taskid``, ``name``
    the task's unique task id (also the same as its process name)

``kwargs``
    the keyword arguments provided to this ``Task``. This is typically the
    testscript's script arguments/parameters.

``result``
    the task's result (eg, the testscript's overall result). This is
    ``None`` when the task has not yet terminated.

``pid``
    the task process's process id. This is set to ``None`` when the task
    has not yet started.

``start()``
    starts the task process. This is when the actual process fork occurs, and
    can only be called once per task.

``join([timeout])``
    if the optional argument ``timeout`` is ``None`` (the default), this method
    blocks until the task terminates. If ``timeout`` is a positive number, it
    blocks at most ``timeout`` seconds.

``wait([max_runtime])``
    if the optional argument ``max_runtime`` is ``None`` (the default), this
    method blocks until the task terminates. If ``max_runtime`` is a positive
    number, it blocks at most ``max_runtime`` seconds. If the task has not
    finished/terminated by ``max_runtime``, it is automatically terminated,
    and a ``TimeoutError`` is raised.

``is_alive()``
    returns whether the task is still alive.

``terminate()``
    terminates the task process by sending ``SIGTERM`` signal to it. This
    abruptly stops the process without running exit handlers, finally clauses,
    etc, and may leave your test environment in a dangling state.


Log Levels
----------

Jobfiles are the perfect location to configure log levels for your testscripts
and libraries. To do so, import the ``logging`` module and set your desired log
levels for each of your modules and libraries.

.. tip::

    the default :ref:`tasklog` logging level is ``logging.INFO``.

.. code-block:: python

    # Example
    # -------
    #
    #   controlling log levels from job file

    from pyats.easypy import run

    # import logging module
    import logging

    # relative script path based on pyats root.
    prefix = sys.prefix

    # main block
    def main(runtime):

        # set logging levels for various modules
        # eg, setting aetest log level to INFO
        # and setting 'mylibrary' to DEBUG
        logging.getLogger('pyats.aetest').setLevel('INFO')
        logging.getLogger('mylibrary').setLevel('DEBUG')
        # if you set the root logger's log level, then it affects all
        # loggers as per rules of logger parent-child relationship
        # eg, turning on DEBUG for all loggers.
        logging.root.setLevel('DEBUG')

        # you can now provide those new values to your pyATS script.
        run(testscript = os.path.join(prefix, 'path', 'to', 'script_two.py'),
            runtime = runtime)

Refer to `Python Logging`_ for details of how loggers work.

.. _Python Logging: https://docs.python.org/3.4/library/logging.html

.. note::

    the name of each logger needs to correspond to their absolute module name.
    This is inline with our requirement for each module logger to be created
    using ``__name__`` as its name.


Shared States
-------------

As all :ref:`easypy_tasks` are encapsulated in its own child process, sharing
information between tasks can be done via the use of shared memory, eg: using
`Pipes and Queues`_, `Shared ctypes Objects`_ or `Server Processes`_.

.. code-block:: python

    # Example
    # -------
    #
    #   passing information back from a task to the jobfile
    #   (using runtime.synchro to create shared dict/list objects)

    from pyats.easypy import run

    # main() function
    def main(runtime):

        # runtime provides a multiprocessing manager instance
        # called runtime.synchro

        # create two shared objects: a dictionary and a list
        shared_dict = runtime.synchro.dict()
        shared_list = runtime.synchro.list()

        # run the task, and pass the shared objects in as parameters
        # if the testscript updates the shared objects, their values
        # are also synchronized to this jobfile level
        run(testscript = 'script_one.py',
            runtime = runtime,
            shared_dict = shared_dict,
            shared_list = shared_list)

        # now you can access the shared objects's values, and do more
        # eg, check for testbed sanity flag
        if shared_dict['testbed_is_sane']:
            # pass it along to the next task
            run(testscript = 'script_two.py',
                runtime = runtime,
                shared_dict = shared_dict,
                shared_list = shared_list)

Refer to Python multiprocessing_ module for details on how shared memory works.

.. _multiprocessing: https://docs.python.org/3.4/library/multiprocessing.html
.. _Pipes and Queues: https://docs.python.org/3.4/library/multiprocessing.html#pipes-and-queues
.. _Shared ctypes Objects: https://docs.python.org/3.4/library/multiprocessing.html#shared-ctypes-objects
.. _Server Processes: https://docs.python.org/3.4/library/multiprocessing.html#sharing-state-between-processes


Custom Arguments
----------------

If leveraging :ref:`easypy_argument_propagation`, your jobfiles may also contain
code to parse jobfile custom arguments stored in ``sys.argv``. Python argparse_
is a reference module to be used for parsing custom arguments.

.. _argparse: https://docs.python.org/3.4/library/argparse.html

.. code-block:: python

    # Example
    # -------
    #
    #   parsing custom arguments in Easypy

    # assuming that this job file is run with the following command:
    #   pyats run job example_job.py --my_custom_arg 'value'
    #
    # where "--my_custom_arg_a" is a custom argument to be parsed by the jobfile

    import sys
    import os
    from pyats.easypy import run

    # using argparse module to do the parsing
    import argparse

    # create your own parser to parse script arguments
    # outside of the main block. This only creates a parser object
    parser = argparse.ArgumentParser(description = "my custom parser")
    parser.add_argument('--my_custom_arg', help = 'my custom argument')
    # add any additional arguments as required...

    # main block
    def main(runtime):

        # do the parsing first thing in the main() block
        # always use parse_known_args as per requirement in argument propagation
        # also stores back extra arguments back to sys.argv
        args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

        # you can now provide those new values to your pyATS script.
        run(testscript = os.path.join(prefix, 'path', 'to', 'script_two.py'),
            runtime = runtime,
            my_custom_arg = args.my_custom_arg)
