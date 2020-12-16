Connection Hook
===============

Whereas a connection class provides the fundamentals of communicating to target
devices using object methods (**services**), the goal of a connection hook is 
to *tap* onto particular services and *inject* code to run before and after the 
actual service call, **without modifying** the original behavior. 

Here are some typical use cases of connection hooks:

    - tracking the sequence/occurance of CLI command calls throughout a script

    - debug-logging the input arguments to, and output values from particular
      services.

    - building a LRU cache based on script inputs and device states.

    - etc.


Usage
-----

A connection hook wraps the original connection service method, and replaces it
during runtime (dynamically). The original functionality of the service remains
intact, but the hook enables uses to add code before/after the service method.

- all connection hooks should inherit the base ``connections.hooks.ServiceHook`` 
  class 

- to add code *before a service*, define the ``enter()`` method under your 
  class.

  - all arguments to the service is passed to ``enter()`` method in the same way
    as the original call.

- to execute code *after a service*, define the ``after()`` method under your
  class

  - the return of the service is passed to the ``after()`` method

- to enable custom error/exception tracking, define a ``error_handle()`` method
  under you class. 

  - the current exception is passed into the error handler as ``e``.

- to disable the current hook, call the ``restore()`` method of the hook.

.. note:: 

    error handlers can suppress an exception, and/or track/register it 
    internally. By default the built-in error handler will simply raise the
    current exception. Developer can modify that to suppress the current 
    exception being handled, and return a fixed/altered result.


.. code-block:: python

    # Example
    # -------
    #
    #   a simple tracking implementation

    import pdb
    import collections
    
    from pyats.connections.hooks import ServiceHook

    class Tracker(ServiceHook):
        '''A hook implementation intended to count the number of CLI calls, and 
        track their result returns'''

        def __init__(self, *args, **kwargs):

            # always call the parent 
            super().__init__(*args, **kwargs)

            # create a local counter
            self.counter = collections.Counter()

            # create a command return storage dictionary
            self.returns = {}

        def enter(self, cmd, *args, **kwargs):
            '''enter

            Track the command occurance (calls) by assuming execute() command's
            first argument is the CLI command to run, and ignoring the rest of
            the arguments
            '''

            # increment the counter
            # (using this command as key)
            self.counter[cmd] += 1

            # store the current command for use in exit()
            self.cmd = cmd

        def exit(self, retval):
            '''exit

            store the return from the command call in another dictionary
            '''

            # the current command from enter()
            cmd = self.cmd

            # current command occurance
            index = self.counter[cmd]

            # because a command can be called multiple times, store each
            # possible command using a dictionary with their counter as index
            self.returns.setdefault(cmd, {})

            # now store the return
            self.returns[cmd][index] = retval

        def error_handle(self, e):
            '''error_handle

            This dummy handler will just print the current exception and go into
            pdb - that could be very useful! 

            Note
            ----
                for demonstration purpose only.

                NEVER do this in production :) you will BLOCK sanity/regression
                automated runs.
            '''

            print(e)
            print('-' * 80)

            # go into pdb
            pdb.set_trace()

            # re-raise the exception
            # (default behavior)
            raise


    # now that we've defined a hook implementation 
    # let's hook an actual device.
    # -----------------------------------------------------------

    # assuming we have a testbed from somewhere
    from pyats.topology import loader
    testbed = loader.load('/path/to/testbed.yaml')

    # get the device and connect to it
    device = testbed.devices['my-device']
    device.connect()

    # use our hook and hook onto the execute() service
    hook = Tracker(device, 'execute')
    # note that device.execute is actually device.connections['default'].execute
    # as per connection manager integration with device objects.
    # thus it's actually more accurate to hook onto the connection itself
    # eg:
    #   hook = Tracker(device.connections['default'], 'execute')

    # from here onwards, all calls to device.execute() will be tracked
    device.execute('show version')
    device.execute('show ip interface brief')

    # the returned hook instance can be used to check the hook returns & etc
    hook.counter
    hook.returns

    # to disable the hook behavior, call the restore() api.
    hook.restore()
    # this will restore the original functionality and disable the hook
