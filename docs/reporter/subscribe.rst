.. _subscribe:

Subscribe
=========

The Reporter Client supports subscribing to the Reporter Server for live
updates about each section starting and stopping. `pyats.reporter.ReportClient`
has an async function `subscribe(callback)` for this purpose. Users must be
familiar with :ref:`pyats_asyncio` in order to leverage this API.

API
---

`subscribe(callback)` takes only one argument which is an async function to call
with event data each time it is received.

Example:

.. code-block:: python

    import asyncio

    from pyats.reporter import ReportClient

    async def my_callback(event):
        # handle event data
        pass

    client = ReportClient(path_to_socket)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.subscribe(my_callback))

Event Data
----------

Event data is a `dict` of information about an event that just occurred. All of
the possible entries are listed in the following table:

.. csv-table:: Event Data Values
    :header: "Key", "Description"

    ``event``, "A string to specify what kind of event occurred such as 'start_task' or 'stop_section'"
    ``type``, "The type of section that triggered this event"
    ``seq_num``, "A unique number specific to the section triggering this event"
    ``parent_seq_num``, "The seq_num of the parent section if there is one"
    ``id``, "The id of the related section"
    ``name``, "The name of the related section"
    ``starttime``, "A timestamp for when the section started"
    ``stoptime``, "A timestamp for when the section ended"
    ``runtime``, "How many seconds the section ran for"
    ``result``, "The result of the section"
    ``logfile``, "The name of the log file"
    ``logs``, "A mapping of log file name, and offset of relevant section of logs"
    ``xref``, "The location of this section in the script"

Only values that exist for that section are included in the event data.

Two notable divergences from typical `start_` and `stop_` events are
`init_testsuite` and `init_task`. A pre-task plugin is associated with a
specific Task, but runs before that Task starts. With `init_task` the Task is
defined before either the Task or the plugin runs. This allows the plugin to be
associated with that Task despite preceding it. This also applies to pre-job
tasks and the Testsuite.

.. sectionauthor:: Ben Astell <bastell@cisco.com>