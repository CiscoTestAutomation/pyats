.. _connection_manager:

Connection Manager
==================

.. sidebar:: Confucius Say...

    The information here onwards is for users interested in ``connections``
    internals & how it works only.

    If you are new to this, do not read on. These advanced topics may
    further fuel your confusion.


As the behind-the-scene director, ``ConnectionManager`` is pivotal in binding
each connections to ``topology.Device``.

This section details how this integration works, and may provide insights as to
how users may leverage the design and do more with it.


Modelling
---------

Connection instances are bound to their corresponding device instances through
a ``ConnectionManager``. The following describes the rules governing this
relationship:

- all connections are created & managed by a device's ``ConnectionManager``.

  - each ``topology.Device`` instance receives its own ``ConnectionManager``.

- each connection is modelled as an instance of a connection class.

- each connection instance is assigned an alias (eg, keyword ``alias``), unique
  to that device.

  - if none is provided, the default alias is ``default``.

- each connection must be provided with a certain *path* (eg, keyword ``via``),
  describing the "how-to" and route taken in order to connect.

  - paths should already defined in this device's ``.connections`` attribute.

  - there is **no default path**: if no path is specified (eg, not providing
    ``via`` argument, it is up to the connection class implementor to select a
    path most appropriate for itself, available for the current device object.

- after a connection is created, all communication methods it offers (eg,
  ``execute``/``config``) are called *services*, and should appear as methods
  to that class.

- if defined, ``Device.connections['defaults']`` dictionary may contain
  key/values that alter the "default" behavior of its connection manager:

  - ``class: <class object>`` changes the default connection class

  - ``alias: <str>`` changes the default connection alias

  - ``via: <str>`` sets a default connection path

**ConnectionManager** class is always automatically instantiated for each device
object, and stored as its ``.connectionmgr`` attribute. It is always unique to
the device it serves, storing internally a *weakref* of its parent device.

.. csv-table:: ConnectionManager Attributes & Methods
    :header: "Name", "Description"
    :widths: 30, 100

    ``device``, "parent device object which this manager belongs to"
    ``connections``, "dictionary storing connection instances by their alias"
    ``instantiate()``, "creates the connection/pool object without connecting to it"
    ``connect()``, "establish connection/, create the connection object if not already created"
    ``disconnect()``, "api to disconnect an existing connection"
    ``destroy()``, "api to destroy/delete a connection"
    ``is_connected()``, "api to check whether a connection is alive"
    ``disconnect_all()``, "api to disconnect all existing connections"
    ``destroy_all()``, "api to destroy/delete all connections"

With the exception of ``disconnect_all()`` and ``destroy_all``, all apis accepts
the ``alias`` argument, specifying the connection instance to operate on. If not
provided, it defaults to ``default``.

.. code-block:: python

    # Example
    # -------
    #
    #   behind-the-scene integration & apis

    # assume we had a device object
    device
    # <Device phoenix at 0xf7714c0c>

    # it always features its own connection manager
    device.connectionmgr
    # <pyats.connections.ConnectionManager object at 0xf76f1c4c>

    # if we make the default connection
    device.connect()

    # and dice things further
    # eg, single out the connection manager
    manager = device.connectionmgr

    # notice that each manager is unique to its parent device
    manager.device
    # <Device phoenix at 0xf7714c0c>

    # and contains a dictionary of connections it currently knows
    # stored as alias: object mapping
    # note how the default connection is assigned with alias "default"
    manager.connections
    # AttrDict({'default': <Connection phoenix at 0xf76c3d08>})


Interworkings
-------------

At the ``topology.Device`` object level, all connection-related method calls
described in :ref:`connection integration <connection_integration>` are actually
translated to a corresponding call to the ``ConnectionManager`` instance.

.. csv-table:: Device & ConnectionManager API Mappings
    :header: "Device Method", "ConnectionManager Mapping"
    :widths: 30, 100

    ``Device.instantiate()``, ``Device.connectionmgr.instantiate()``
    ``Device.connect()``, ``Device.connectionmgr.connect()``
    ``Device.disconnect()``, ``Device.connectionmgr.disconnect()``
    ``Device.destroy()``, ``Device.connectionmgr.destroy()``
    ``Device.is_connected()``, ``Device.connectionmgr.is_connected()``
    ``Device.disconnect_all()``, ``Device.connectionmgr.disconnect_all()``
    ``Device.destroy_all()``, ``Device.connectionmgr.destroy_all()``
    ``Device.<service>()``, ``Device.connectionmgr.connections['default'].<service>()``
    ``Device.<alias>.<service>()``, ``Device.connectionmgr.connections[<alias>].<service>()``

.. code-block:: python

    # Example
    # -------
    #
    #   demonstrating the above translations

    # given any device, take a look at the repr() of its connection methods
    device.connect
    # <bound method ConnectionManager.connect of <pyats.connections.ConnectionManager object at 0xf75d03ec>>
    device.disconnect
    # <bound method ConnectionManager.disconnect of <pyats.connections.ConnectionManager object at 0xf75d03ec>>

    # connect and take a look at the service bindings
    device.connect()
    device.execute
    # <connection.services.router_services.ExecService object at 0xf705e1ac>
    device.configure
    # <connection.services.router_services.ConfigService object at 0xf705e1ad>

    # ergo, the mappings are equal
    device.connect == device.connectionmgr.connect
    # True
    device.execute == device.connectionmgr.connections['default'].execute
    # True
    device.configure == device.connectionmgr.connections['default'].configure
    # True

In order words, the above mapping relationship hides the users from having to
deal with ``ConnectionManager`` directly and making long & chained method calls.
Of course, if any defaults were changed (eg, through ``connections[defaults]``),
this behavior would change accordingly, eg:

.. code-block:: python

    # Example
    # -------
    #
    #     changing defaults of ConnectionManager
    from myconnection import MyConnectionClass

    # if the device object had the following connections attribute
    # (note that this could be coming from loading YAML file, or set manually)
    device.connections = {
        'defaults': {
            'class': MyConnectionClass,
            'alias': 'ironman',
            'via': 'highway'
        },
        'highway': {
            'protocol': 'telnet',
            'ip': '1.1.1.1',
        }
    }

    # the following call
    #  - would use MyConnectionClass() as the connection class,
    #  - would have a default alias of 'ironman'
    #  - and via 'highway'
    device.connect()

    # and thus the following would be true instead
    device.execute == device.connectionmgr.connections['highway'].execute
    type(device.connectionmgr.connections['highway']) is MyConnectionClass
    device.connectionmgr.connections['highway'].via == 'highway'

.. hint::

    sometimes black magic like above are a *necessary evil*: it provides
    code layering from an architectural design perspective without taxing the
    user experience.


Method: instantiate(), connect()
--------------------------------

``ConnectionManager.instantiate()`` method creates a new connection class/pool
instance without starting up the connection.
``ConnectionManager.connect()`` method establishes full connectivity to the
device using the above connection object. In effect, internally, ``connect()`` 
calls ``instantiate()`` when needed to create a new connection object.

These are `factory methods`_: eg, it instantiates a new connection instance
based on input parameters and internal defaults. Behaviors are as follows:

- takes in a :ref:`connection_class` via argument ``cls``.

- requires an alias for each connection. Defaults to ``default``.

- **[optional]** if ``pool_size`` argument is provided, creates a 
  :ref:`pool of new connections <connectionpool>` (for parallel execution).

- if the provided alias already exists, use that existing connection instance
  associated with that alias, and call its ``.connect()`` method.

- if the provided alias doesn't exist, instantiate a new connection object, and
  call its ``.connect()`` method.

- stores the new connection under ``ConnectionManager.connections`` dictionary
  as ``<alias>: <object>``.

.. csv-table:: ConnectionManager.connect() and instantiate() Arguments
    :header: "Name", "Description"
    :widths: 30, 100

    ``cls``, ":ref:`connection_class` to use to create this connection or pool worker"
    ``alias``, "alias/name of this connection, unique. Defaults to ``default``"
    ``pool_size``, "number of connection instances to be started in pool"
    ``pool_timeout``, "max time to wait for an available worker from the pool,
    defaults to ``0`` (forever)"
    ``via``, "path to use to create this connection, must be defined in
    ``Device.connections`` dict"
    "``*args, **kwargs``", "all other argument to be propagated to the actual
    connection's ``__init__()`` method"


.. code-block:: python

    # Example
    # -------
    #
    #   ConnectionManager.connect() and .instantiate() method
    #   (simple/single connection class instance)

    # given a device connection manager object
    device.connectionmgr
    # <pyats.connections.ConnectionManager object at 0xf76f1c4c>

    # we could establish connections using the default class
    # ------------------------------------------------------
    # just connect
    device.connect()
    # equivalent to: device.connectionmgr.connect()

    # connect using a different path and alias
    # (this requires device.connections['mgmt'] to be populated)
    device.connect(alias = 'vty_1', via = 'mgmt')
    # equivalent to: device.connectionmgr.connect(alias = 'vty_1', via = 'mgmt')

    # we could establish connections using another class
    # --------------------------------------------------
    from some_connection_lib import AltConnImpl

    # just connect using it
    device.connect(cls = AltConnImpl)
    # equivalent to: device.connectionmgr.connect(cls = AltConnImpl)

    # connect using a different path and alias and that class
    device.connect(cls = AltConnImpl, alias = 'vty_1', via = 'mgmt')
    # equivalent to: device.connectionmgr.connect(cls = AltConnImpl,
    #                                             alias = 'vty_1',
    #                                             via = 'mgmt')

    # additionally, we could instantiate the object first
    # ---------------------------------------------------
    connection = device.instantiate(cls = AltConnImpl)
    # and modify various attributes before we connect
    connection.new_attribute = 'x'
    connection.connect()
    # note that after device.instantiate() is called, the newly created
    # connection object is saved both under the given alias in the connection
    # manager, and returned for your direct access.

    # --------------------------------------------------------------------------
    # all other arguments to connect() api are propagated to the connection class
    # (assuming AltConnImpl took arguments timeout, term_width and max_buffer)
    device.connect(cls = AltConnImpl,
                   alias = 'session_1',
                   timeout = 100,
                   term_width = 512,
                   max_buffer = 999999)
    # eg, equivalent to:
    # device.connectionmgr.connections['session_1'] = AltConnImpl(timeout = 100,
    #                                                             term_width = 512,
    #                                                             max_buffer = 999999)
    # device.connectionmgr.connections['session_1'].connect()


.. code-block:: python

    # Example
    # -------
    #
    #   ConnectionManager.connect() and .instantiate() method
    #   (starting pool of connections)

    # given a device connection manager object
    device.connectionmgr
    # <pyats.connections.ConnectionManager object at 0xf76f1c4c>

    # we could establish a pool of connections using the default class
    # ----------------------------------------------------------------
    # just give the alias 'pool' for simplicity
    # and start it with 3 workers
    device.connect(pool_size = 3)

    # or connect using a different path
    # (this requires device.connections['mgmt'] to be populated)
    device.connect(pool_size = 3, via = 'mgmt')

    # we could establish a pool of workers using another class
    # --------------------------------------------------------
    from some_connection_lib import AltConnImpl

    # start pool directly (default path)
    device.connect(pool_size = 5, cls = AltConnImpl)

    # start pool using a different path and this class
    device.connect(pool_size = 5,
                   cls = AltConnImpl,
                   via = 'mgmt')

    # additionally, we could instantiate the pool object first
    # --------------------------------------------------------
    pool = device.instantiate(pool_size = 5,
                              cls = AltConnImpl,
                              via = 'mgmt')
    # and modify various attributes before we connect
    pool.new_attribute = 'x'
    pool.connect()

    # once a pool is started, use it like any other connection
    # --------------------------------------------------------
    # calls are redirected to the first available worker
    device.pool.execute('command')

When a connection pool is created using ``pool_size=N``, it behaves like 
any other direct connections and internally distributes the api calls/work 
to its workers. All other means of disconnecting, destroying, etc mentioned
in the rest of this documentation also applies to connection pools.

.. tip:

    Connection pools must be of the same type & path, eg, you cannot create a
    pool of connections to a router's console port, but you can to its
    management port (multiple vty)

.. warning::

    When using connection pools, appling changes on any connection (regardless 
    of pool worker) may affect the whole system, eg, don't reload a router 
    in one worker and expect show tech output in the other. Keep this in mind...

For more information on how connection pools work, please refer to
:ref:`connectionpool` guide.


Method: disconnect()
--------------------

``ConnectionManager.disconnect()`` method disconnects a given connection from
its host device by first looking up the connection object using the provided
``alias``, then calling that object's ``.disconnect()`` api.

.. csv-table:: ConnectionManager.disconnect() Arguments
    :header: "Name", "Description"
    :widths: 30, 100

    ``alias``, "alias/name of connection to disconnect. Defaults to ``default``"

.. code-block:: python

    # Example
    # -------
    #
    #   ConnectionManager.disconnect() method

    # disconnect the default aliased connection
    device.disconnect()
    # equivalent to: device.connectionmgr.disconnect(alias = 'default')

    # disconnect a specific alias
    device.disconnect(alias = 'vty_1')
    # equivalent to: device.connectionmgr.disconnect(alias = 'vty_1')

    # in effect, it is the same as doing:
    device.connectionmgr.connections['vty_1'].disconnect()

.. tip::

    keep in mind that disconnect is only a **change of state** from a connection
    class perspective. Eg: the class instance still exists, but the pipe is
    no longer active. Calling ``.connect()`` again simply re-establishes the
    pipe.


Method: destroy()
-----------------

``ConnectionManager.destroy()`` method disconnects a given connection from
its host device, and also destroys/deletes the connection object. Behavior:

- lookup the connection object by the provided alias, and call its
  ``.disconnect()`` api.

- delete that connection object from ``ConnectionManager.connections``
  dictionary.

.. csv-table:: ConnectionManager.destroy() Arguments
    :header: "Name", "Description"
    :widths: 30, 100

    ``alias``, "alias/name of connection to destroy. Defaults to ``default``"

.. code-block:: python

    # Example
    # -------
    #
    #   ConnectionManager.destroy() method

    # destroy the default aliased connection
    device.destroy()
    # equivalent to: device.connectionmgr.destroy(alias = 'default')

    # destroy a specific alias
    device.destroy(alias = 'vty_1')
    # equivalent to: device.connectionmgr.destroy(alias = 'vty_1')

    # in effect, it is the same as doing:
    device.connectionmgr.connections['vty_1'].disconnect()
    del device.connectionmgr.connections['vty_1']

.. tip::

    destroy is a non-recoverable call: the object representing the connection
    is deleted.

Method: is_connected()
----------------------

``ConnectionManager.is_connected()`` method returns ``True``/``False`` depending
on whether a connection object (referred to by its alias) is in a connected
state or not. Behavior:

- lookup the connection object by the provided alias, and get its
  ``.connected`` property.

- if a connection alias/object doesn't exist, return ``False`` anyway, do not
  error out.

.. csv-table:: ConnectionManager.is_connected() Arguments
    :header: "Name", "Description"
    :widths: 30, 100

    ``alias``, "alias/name of connection to lookup. Defaults to ``default``"

.. code-block:: python

    # Example
    # -------
    #
    #   ConnectionManager.is_connected() method

    # lookup the default aliased connection
    device.is_connected()
    # equivalent to: device.connectionmgr.is_connected(alias = 'default')

    # lookup a specific alias
    device.is_connected(alias = 'vty_1')
    # equivalent to: device.connectionmgr.is_connected(alias = 'vty_1')

    # in effect, it is the same as doing:
    device.connectionmgr.connections['vty_1'].connected


Method: disconnect_all()
------------------------

``ConnectionManager.disconnect_all()`` method attempts to change all current
connection's state to disconnected. It accepts no arguments.

.. code-block:: python

    # Example
    # -------
    #
    #   ConnectionManager.disconnect_all() method

    # disconnect everything!
    device.disconnect_all()
    # equivalent to: device.connectionmgr.disconnect_all()

    # in effect, it is the same as doing:
    for conn in device.connectionmgr.connections.values():
        conn.disconnect()

Method: destroy_all()
---------------------

``ConnectionManager.destroy_all()`` method attempts to change all current
connection's state to disconnected, then removes the connection object. It
accepts no arguments.

.. code-block:: python

    # Example
    # -------
    #
    #   ConnectionManager.destroy_all() method

    # destroy_all everything!
    device.destroy_all()
    # equivalent to: device.connectionmgr.destroy_all()

    # in effect, it is the same as doing:
    for conn in device.connectionmgr.connections.values():
        conn.disconnect()
    device.connectionmgr.connections.clear()


.. _factory methods: https://en.wikipedia.org/wiki/Factory_method_pattern
