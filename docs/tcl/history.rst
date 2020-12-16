Interpreter History
===================

Introduction
------------

When an instance of ``Interpreter`` class is created, an associated instance of
``History`` is also loaded automatically. This class offers the ability to track 
user Tcl call history with time stamp information. In addition, the ``History``
class offers users to mark the beginning and end of important events as 
separate history queues, with filters that looks for particular Tcl calls. This
can be very effective when used to debug what-went-wrong during Python-Tcl
interactions.


.. code-block:: python

    # Example
    # -------
    #
    #   how history is tracked and read

    from pyats.tcl import Interpreter, History
    
    tcl = Interpreter()
    
    # note the history attribute
    assert type(tcl.history) is History

    # make some tcl calls
    tcl.eval('set testVar 1')
    tcl.eval('set testVar 2')

    # let's take a look at the history
    tcl.history.filter()
    # output:
    #   deque(
    #    [<HistoryEntry '2014-06-04T23:30:12.939354: set testVar 1' at ...>, 
    #     <HistoryEntry '2014-06-04T23:30:18.665275: set testVar 2' at ...>,
    #     maxlen=9999])

    # print it in a more usable fashion:
    for i in tcl.history.filter(): 
        print(i.timestamp, '-', i.api)
    # output:
    #   2014-06-04 23:30:12.939354 - set testVar 1
    #   2014-06-04 23:30:18.665275 - set testVar 2
    

How It Works
------------

History is stored as a first-in-last-out queue with a maximum limit. Each time
the user makes a call to ``eval``, it is added to the history with the current
timestamp. When the max queue is reached, the earliest historical entry is 
deleted to save from ever-growing memory usage.

Each historical event is saved as a ``HistoryEntry`` object. Each of these
object has ``timestamp`` and ``api`` attribute:
* ``timestamp`` being the time when the API was called
* ``api`` being the Tcl command itself.

The default max limit for the queue is *9999*. This can be altered if user 
manually replace the ``history`` attribute of the an ``Interpreter`` instance
with a new one with bigger queue:

.. code-block:: python
    
    # continuing from above...

    # replace the history tracker with a new, bigger one
    tcl.history = History(max_history = 15000)

    # note that this deletes all historical event up until now
    tcl.history
    # output:
    #   deque([], maxlen=15000)

.. hint::

    the API may be multi-line if multiple semi-colon ``;`` separated Tcl
    commands were evaluated in the same ``eval()``.

Filter
------

The ``filter`` API returns by default the last 20 historical events for better
viewing. Use this API to return an iterable history list. You can also use it
to only filter calls that match a particular regular expression.

.. code-block:: python
    
    # continuing from above (but assuming we didn't reset the history)
    tcl.history.filter(regex = 'testVar 1')
    # output:
    #   [<HistoryEntry '2014-06-04T23:30:12.939354: set testVar 1' at ...>]

Markers
-------

Consider markers as separate history queues that can be used to mark and store
important events. Eg: start at the beginning of a testcase and end of it, in
order to give users full picture of what Tcl commands were called within that
testcase.

By default, all history is appended to the **master** queue. This queue is
always updated with each Tcl call. When a new marker is started, all subsequent
Tcl calls are saved to both the new marker and the **master** queue, until
stopped.  There may be an indefinite number of markers active (limited by 
CPU/memory of course). 

Consider the **master** queue as a broad picture into everything, with the 
individual marker queues as a snapshot of a particular time/event.

.. code-block:: python
    
    # Example
    # -------
    #
    #   showing how markers work

    from pyats import tcl

    # run some Tcl code
    tcl.eval('set test 1')

    # create a new marker
    tcl.history.start_marker('testMarker')

    # run code under new marker
    tcl.eval('set a 1')

    # now create another marker
    tcl.history.start_marker('testMarker2')

    # run code under new marker as well
    tcl.eval('set b 2')

    # stop the markers
    tcl.history.end_marker('testMarker')
    tcl.history.end_marker('testMarker2')

    # run more code
    tcl.eval('set c 3')
    
    # now let's see history vs marker behavior
    # all calls are in the master (default) marker
    tcl.history.filter()
    # output:
    #   [<HistoryEntry '2014-08-19T14:17:57.697085: set test 1' at ...>, 
    #    <HistoryEntry '2014-08-19T14:18:12.505794: set a 1' at ...>, 
    #    <HistoryEntry '2014-08-19T14:18:29.150347: set b 2' at ...>, 
    #    <HistoryEntry '2014-08-19T14:18:52.338709: set c 3' at ...>]

    # 'testMarker' only has 1 calls
    tcl.history.filter(marker='testMarker')
    # output:
    #   [<HistoryEntry '2014-08-19T14:18:12.505794: set a 1' at ...>,
    #    <HistoryEntry '2014-08-19T14:18:29.150347: set b 2' at ...>]

    # 'testMarker2' only contains 1 call
    tcl.history.filter(marker='testMarker2')
    # output:
    # [<HistoryEntry '2014-08-19T14:18:29.150347: set b 2' at ...>]

Marker usage is pretty much trivial. For detailed usage to the API, refer to the
API documentation.
