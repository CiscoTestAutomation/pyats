
.. _kleenex_cleaners:

Cleaning Model
==============

The Kleenex clean model is fairly straight forward: a common, built-in internal
clean engine takes care of the common mundane infrastructure work, and the
individual clean classes selected by the clean file carry out the actual work.

Under this model, these clean classes are the actual work-horses. A clean class
is **a device and/or platform family specific clean implementation**, carrying
out whatever work is necessary to recover/initialize a device with new images
and set its configuration back to default (bare minimum).

The Kleenex module does not come with a built-in, universal clean
implementation. Rather, it features ``BaseCleaner``: a base class template,
offering a set of standards, guidelines, rules & tools for anyone to build on.


Clean Engine
------------

    - is an integral, non-changeable internal component to Kleenex
    - sets up runtime directory & logfiles
    - loading and parsing :ref:`clean_file` and testbed file (if necessary)
    - applying clean file content towards testbed device objects
    - error handling, email notification, etc.
    - running the corresponding clean on all testbed devices simultaenously
      in parallel

      - If ``-pdb`` is specified via the command line,

        - devices are cleaned serially
        - if a cleaner throws an exception an interactive debugger is launched.


.. code-block:: text

    Pictorial View of Clean Engine
    ------------------------------

    +--------------+
    |  clean file  |---.             +-------------+
    +--------------+    \   input    |             |
                         >---------> | CleanEngine |
    +--------------+    /            |             |
    | testbed file |---'             +-------------+
    +--------------+                        |
                                            |
                                            |  fork   +--------------------+
                                            |---------| cleaner: Cleaner-1 |
                                            |         | target : Device-1  |
                                            |         +--------------------+
                                            |
                                            |  fork   +--------------------+
                                            |---------| cleaner: Cleaner-2 |
                                            |         | target : Device-2  |
                                            |         +--------------------+
                                            |
                                            |  fork   +--------------------+
                                            |---------| cleaner: Cleaner-3 |
                                            |         | target : Device-3  |
                                            |         +--------------------+
                                            |
                                           etc...



Clean Classes
-------------

    - clean classes are only responsible of handling/cleaning one device at a
      time, performing what is necessary to do the act of "clean"

    - clean classes must inherit from the
      `BaseCleaner<pyats.kleenex.bases.BaseCleaner>` class.

    - clean classes must implement at minimum, the ``clean()`` method. This is
      the primary entry point to start cleaning a device. This method shall
      accept a :ref:`Device object <topology_device_object>` as argument,
      which instructs it which device to clean.

    - clean classes should only pull their required clean-related information
      directly from the provided
      :ref:`Device object's <topology_device_object>`
      ``clean`` attribute dictionary.

    - cleaners are allowed to modify ``device.clean`` with discovered
      device metadata, which then appears in the user's :ref:`topology_objects`
      passed via the :ref:`easypy_testbed` parameter.

When clean classes are referenced in the clean file (using ``cleaners:`` block),
they are instantiated using the key/values given under its definition block.
The engine then calls the ``clean()`` method of that class as entry-point to
start cleaning the corresponding device.

.. code-block:: yaml

    # Example
    # -------
    #
    #   a sample clean file (only showing the cleaners block)

    cleaners:
        AwesomeClean:
            module: mollymaid.cleaners
            devices: [example-device, ]
            timeout: 100
            loglevel: INFO
            retry: 3

.. code-block:: python

    # -----------------------------------------------------
    # how Kleenex engine internally invokes cleaner classes
    # (pseudo code for demonstrating internals only)

    # the class is imported first, based on its class name and module info
    from mollymaid.cleaners import AwesomeClean

    # then the class is instantiated using kwargs from the clean file
    # definition (devices/groups keys are ignored: they are consumed by the
    # engine instead)
    cleaner = AwesomeClean(timeout = 100,
                           loglevel = 'INFO',
                           retry = 3)

    # finally, assuming that the testbed is already loaded
    # this clean class is invoked to do cleaning on that device
    cleaner.clean(device = testbed.devices['example-device'])

.. note::

    During runtime, the kleenex engine actually performs all cleaning in an
    asynchronous manner: it forks one subprocess per device and cleans all
    required devices in parallel. This is a framework-level runtime detail,
    and is not reflected in the above pesudo-code.

In retrospect, cleaner classes have a very intuitive implementation front-end.
All the necessary bits and pieces are provided by the engine, and the user is
only focused on coding the steps required to get clean done.


Clean Reporting
---------------

The results of cleaning for each device is found inside of the
``results.json`` file generated at the end of a pyats job or clean. Every device
is listed under the ``KleenexPlugin`` plugin in ``Testsuite`` / ``Cleansuite`` /
``Task`` plugins depending on the clean scope. Each device will have a result of
``Passed`` or ``Failed`` and the plugin will have a summary of the results for
all devices

The way a cleaner implementation indicates failure is by raising an exception
inside its ``clean`` API.


Clean Steps
-----------

.. sidebar:: Helpful Reading

    - `Context Manager`_
    - `The with statement`_

.. _Context Manager: https://docs.python.org/3.8/reference/datamodel.html#context-managers
.. _The with statement: https://docs.python.org/3.8/reference/compound_stmts.html#the-with-statement

Users may choose to slice a device clean into a series of steps that are
individually logged and included in the ``CleanResultsDetails.yaml`` report.

If a cleaner's ``clean`` API optionally includes the reserved ``steps``
parameter, a step may be created via the ``steps.start`` API and used as a
context manager.  Any exception raised while in the step's context causes the
step to be marked as failed and the clean for the entire device to be marked
as failed in the report.


Sample Implementation Without Steps
-----------------------------------

The following is a pesudo-code implementation of a clean class. The idea is to
walk you through on the look & feel of implementing your own cleaners.

.. code-block:: python

    # Example
    # -------
    #
    #   a pesudo-code example implementation of a cleaner class

    # all clean implementations inherit from BaseCleaner
    class ExampleCleaner(BaseCleaner):
        '''BaseCleaner

        demonstrating the details of how cleaners are to be implemented
        '''

        def __init__(self, arg_1, arg_2, arg_3):
            '''__init__

            clean class constructor. All clean initialization arguments should
            be defined as arguments to this method (eg, arg_1, arg_2, arg_3)
            '''

            # always call the parent __init__()
            super().__init__()

            # everything else necessary... eg:
            self.arg_1 = arg_1
            self.arg_2 = arg_2
            self.arg_3 = arg_3

        def clean(self, device):
            '''clean

            main entry point of this clean implementation, this method is called
            in a subprocess under kleenex runtime, specific to cleaning one
            particular device.

            A device object representing the device to clean is always provided.
            '''

            # connect to the device
            device.connect()

            # look up the details of how to clean this device, eg:
            clean_info = device.clean

            # do the actual clean, eg, pseudo-code
            self._imaginary_load_image_method(device = device,
                                              images = clean_info['images'])

            # maybe reload the device?
            self._imaginary_device_reload(device = device)

            # apply post-clean config?
            device.configure(clean_info['post-clean'])

            # we're done!
            device.disconnect()


Sample Implementation With Steps
--------------------------------

The preceding clean class could also be implemented by specifying steps.
The steps are written into the ``CleanResultsDetails.yaml`` file.

.. code-block:: python

    # Example
    # -------
    #
    #   a pesudo-code example implementation of a cleaner class

    # all clean implementations inherit from BaseCleaner
    class ExampleCleanerWithSteps(ExampleCleaner):
        '''BaseCleaner

        demonstrating the use of steps in a cleaner implementation.

        '''

        def clean(self, device, steps):
            '''clean

            main entry point of this clean implementation, this method is called
            in a subprocess under kleenex runtime, specific to cleaning one
            particular device.

            A device object representing the device to clean is always provided.

            A steps object is provided when the ``steps`` parameter is
            specified and may be used to define clean steps that are
            individually logged and tracked in the CleanResultsDetails.yaml
            clean report.
            '''

            # connect to the device
            device.connect()

            # look up the details of how to clean this device, eg:
            clean_info = device.clean

            with steps.start('Clean the device'):
                # do the actual clean, eg, pseudo-code
                self._imaginary_load_image_method(device = device,
                                                  images = clean_info['images'])

            with steps.start('Reload the device'):
                # maybe reload the device?
                self._imaginary_device_reload(device = device)

            with steps.start('Apply post-clean configuration'):
                # apply post-clean config?
                device.configure(clean_info['post-clean'])

            # we're done!
            device.disconnect()
