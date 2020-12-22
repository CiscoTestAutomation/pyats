.. _connection_class:

Connection Class
================

Connection classes are the workhorse of the connection model: their 
implementation represents the actual connection pipeline, carrying information
back and forth from the scripter's realm to their testbed devices.

As there are *over nine thousand* types of different devices and methods to 
connect to them, the Connections module does not come with a built-in, 
universal connector class. Rather, it features ``BaseConnection``: a base class
template, offering a set of standards, guidelines, rules & tools for anyone to 
build on. 


Fundamentals
------------

The fundamental idea behind standardizing using ``BaseConnection`` is to 
enable basic connector-swapping through `duck typing`_: changing connection
types & classes without impacting the library & user scripts (within reason, of
course). This also gives all connection implementations the same look &
feel, allowing for ease of extension, debugging & maintenance, etc.

Therefore, all connection implementations shall follow the same set of
rules & guidelines:

- always subclass from ``connections.BaseConnection``

- respect the basic design: arguments, properties, methods & etc.

- each instance should only represent a single connection pipe (eg, a single
  telnet instance, etc)

- all connections shall have a maximum timeout limit, and should **never**
  block forever.

- avoid race conditions & deadlocks when your connection instance is shared
  between processes/threads: use `semaphores`_.

- always implement using a bottom-up approach: 

  - start with the basic building blocks: ``send``/``receive``

  - then build the next level: ``expect``, ``dialogs``

  - then wrap up with top-levels: ``execute``, ``configure``, etc.

In essence, a connection class models the various ways of communicating with a
target device using object methods (also known as **services**). These methods
(**services**) vasly simplify the underlying protocol/behavior details into 
arguments, datastructure inputs and returns.

.. _semaphores: https://en.wikipedia.org/wiki/Semaphore_(programming)



BaseConnection
--------------

Base class to all connection implementations, ``BaseConnection`` is a simple set
abstract concepts & of bare-minimum methods. The following is a table describing 
each attribute/method and how it should be used.

.. csv-table:: BaseConnection Attributes & Methods
    :header: "Name", "Description"
    :widths: 30, 100

    ``__init__()``, "should always be called to instantiate a connection class."
    ``device``, "property, storing the connected Device object as weakref"
    ``connection_info``, "property, returns the dictionary of connection info based
    on path (``via``)"
    ``connected``, "property, returns the current connection state boolean"
    ``connect()``, "abstract method: open/establish this connection"
    ``disconnect()``, "abstract method: disconnect/close this connection"
    ``send()``, "abstract method: send a text string through this connection"
    ``receive()``, "abstract method: receive whatever is currently in the buffer"
    ``execute()``, "abstract method: high-level api to execute a command and
    collect its full return"
    ``configure()``, "abstract method: configure the device through this
    connection"

.. code-block:: text

    ** abstract methods are to be implemented in user's subclass.

.. hint::

    do not confuse ``ConnectionManager.connect()`` and connection class'
    ``YourConnection.connect()``: the former is a factory class creating new
    connection instances; the latter is the action that opens/establishes
    the actual connection.


Sample Implementation
---------------------

The following is a pseudo-code implementation of a connection class cooked up 
under 10 minutes. The idea is to walk you through how writing your own 
connection class looks & feels like.

.. code-block:: python

    # Example
    # -------
    #
    #   a very rudimentry implementation of telnet connection

    # using python's built-in library
    # to handle telnet connections client
    import telnetlib

    from pyats.connections import BaseConnection

    class TelnetConnection(BaseConnection):
        '''TelnetConnection

        Sample implementation of Telnet connection to linux, based on pyATS
        BaseConnection, allowing devices to telnet to end routers
        '''

        def __init__(self, *args, **kwargs):
            '''__init__

            instantiate a single connection instance. 
            '''

            # instantiate parent BaseConnection
            super().__init__(*args, **kwargs)

            # create an instance of telnetlib.Telnet
            self._telnet = telnetlib.Telnet()

            # let's hard code the expected prompt
            # (and assume it's a bash shell prompt)
            self._prompt = 'bash$ '

        def connect(self):
            '''connect

            opens the telnet connection and log us in.
            '''

            # open the telnet session
            # self.connection_info is inherited from BaseConnection
            self._telnet.open(host = self.connection_info['ip'],
                              port = self.connection_info['port'])

            # process login
            self._telnet.read_until(b"login: ")

            # send the login name
            self.send(self.device.tacacs['username'])

            # process password
            self._telnet.read_until(b"password: ")
            self.send(self.device.passwords['tacacs'])

            # find the prompt
            self._telnet.read_until(self._prompt.encode('ascii'))

        def send(self, text):
            '''send

            low-level api: sends raw text through telnet session.
            '''

            # remember to convert string to bytes
            return self._telnet.write(text.encode('ascii') + '\n')

        def receive(self):
            '''receive

            low-level api: reads from the telnet session and returns whatever is
            currently in the buffer
            '''

            # remember to convert back from bytes to string
            return self._telnet.read_eager().decode('utf-8')

        def execute(self, command):
            '''execute

            high-level api: sends a command through the session, expect it to
            be executed, and return back to prompt.
            '''

            # send the command
            self.send(command)

            # expect the prompt
            output = self._telnet.read_until(self._prompt.encode('ascii'))

            # convert the output to string
            output = output.decode('utf-8')

            # remove the telnet echo of our original command
            output.lstrp(command + '\n')

            # we're done!
            return output

        def configure(self, *args, **kwargs):
            raise NotImplementedError('just configure using execute api!')


The code above is **very** rudimentry, but hopefully gives you a basic idea as
to how connection classes work, and how it should be implemented. 

Word of advice: don't try to enhance this for production use. I can think of 42
ways it could go wrong, and 47 unhandled corner cases that will cause your
script to hang. (Hmm, this makes a great interview question).

    *"For everything, there is a first time." - Spock*

.. _duck typing: https://en.wikipedia.org/wiki/Duck_typing
