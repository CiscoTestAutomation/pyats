Attribute Dictionaries
======================

``AttrDict``
------------

``AttrDict``, Attribute Dictionary, is the exact same as a python native
``dict``, except that in *most* cases, you can use the dictionary key as if it
was an object attribute instead. This allows users to create container objects
that looks as if they are class objects (as long as the user objects the proper
limitations).

.. code-block:: python

    # Example
    # -------
    #
    #   AttrDict use case

    from pyats.datastructures import AttrDict

    # create a nested AttrDict chain
    obj = AttrDict()
    obj.a = AttrDict()
    obj.a.b = AttrDict()

    # now you can access it via chaining
    obj.a.b.c = 'value'

    # it looks & feels like class instances, but is really just a
    # dictionary doing the dirty heavy lifting
    obj
    # AttrDict({'a': AttrDict({'b': AttrDict({'c': 'value'})})})

.. tip::
    
    this is extremely useful when used as container objects, eliminating the
    need to create the actual classes.
    

Creation
^^^^^^^^

Create an ``AttrDict`` the same way as creating your typical ``dict`` objects.

.. code-block:: python

    # Example
    # -------
    #
    #   attribute dictionary creations

    from pyats.datastructures import AttrDict

    # instantiate an AttrDict the same as how you'd instantiate a dict
    attrdict = AttrDict(key = 'value', a = 1)
    # AttrDict({'a': 1, 'key': 'value'})

    # you can also instantiate using a dictionary as input
    attrdict = AttrDict({'a': 1, 'key': 'value'})

    # or an iterable of item size 2
    attrdict = AttrDict([('a', 1), ('key', 'value')])

Access
^^^^^^

Keys in an ``AttrDict`` can be accessed via the traditional ``dict[ ]`` method, 
or using the keys as attributes.


.. code-block:: python

    # Example
    # -------
    #
    #   attribute dictionary access

    from pyats.datastructures import AttrDict
    attrdict = AttrDict(key = 'value', a = 1)

    # access it as if it was a dictionary
    attrdict['key']
    # 'value'
    attrdict['a']
    # 1

    # access it as attributes
    attrdict.key
    # 'value'
    attrdict.a
    # 1

    # set attributes is the same as adding new keys
    #   same as attrdict['b'] = 2
    attrdict.b = 2
    attrdict
    # AttrDict({'b': 2, 'a': 1, 'key': 'value'})

.. note::

    all other native ``dict`` behaviors and APIs are unchanged.


Limitations
^^^^^^^^^^^

Like previously stated, this only works *most* of the time. Here is a known list
of limitations

- in order to access a value as an attribute, its key must of type ``str`` (in 
  standard python ``dict``, keys can be any hashable objects)

- keys with characters such as ``-``, ``.``, ``\`` etc, cannot be accessed as 
  attributes. This is due to the limitation of python identifiers.

    .. code-block:: text

        # python valid identifiers
        identifier ::=  (letter|"_") (letter | digit | "_")*
        letter     ::=  lowercase | uppercase
        lowercase  ::=  "a"..."z"
        uppercase  ::=  "A"..."Z"
        digit      ::=  "0"..."9"

.. tip::

    if there's something that cannot be accessed as an attribute, you can always
    fall back to the standard method using ``[ ]``



``NestedAttrDict``
------------------

Nested attribute dictionary is a special subclass of ``AttrDict`` that 
recognizes when its key values are other dictionaries, and auto-convert them
automatically into further ``NestedAttrDict``. This allows the whole nested 
dictionary structure to be traversable using attribute getters automatically 
without user intervention (eg, ``.`` operator).

.. code-block:: python

    # Example
    # -------
    #
    #   NestedAttrDict use case

    from pyats.datastructures import NestedAttrDict

    # if we had a big nested dict structure
    my_dict = {
        'a': 1,
        'b': 2,
        'c': {
            'x': 10,
            'y': 20,
            'z': {
                'value': 100,
            },
        },
    }

    # create a nested attribute dictionary
    obj = NestedAttrDict(my_dict)

    # now you can access it via chaining
    obj.c.z.value
    # 100

    # it looks & feels like class instances, but is really just a
    # dictionary doing the dirty heavy lifting
    # (notice all child dicts got turned into NestedAttrDict)
    obj
    # NestedAttrDict({'a': 1, 
    #                 'b': 2, 
    #                 'c': NestedAttrDict({'x': 10, 
    #                                      'y': 20, 
    #                                      'z': NestedAttrDict({'value': 100})})})


Features & Limitations
^^^^^^^^^^^^^^^^^^^^^^

- ``NestedAttrDict`` inherits the same limitations as ``AttrDict`` where the
  key names, if accessed as attributes, can only be strings without special
  characters

- When nested dictionaries are detected on set or update, they are auto 
  converted into a new instance of ``NestedAttrDict``. Eg - its object id 
  will change, and will no longer refer to the old instance

- Key methods supports using ``.`` separator to perform automated nested
  access.

  .. code-block:: python

      # Example
      # -------
      #
      #     various object access

      my_dict = {
          'a': 1,
          'b': 2,
          'c': {
              'x': 10,
              'y': 20,
              'z': {
                  'value': 100,
              },
          },
      }

      obj = NestedAttrDict(my_dict)
      
      # get api
      obj.get('c.y')
      # 20

      obj.get('a')
      # 1

      # get with default
      obj.get('c.z.non_existent_value', 1000)
      # 1000

      # delete
      del obj['c.x']
      # NestedAttrDict({'a': 1, 
      #                 'b': 2, 
      #                 'c': NestedAttrDict({'y': 20, 
      #                                      'z': NestedAttrDict({'value': 100})})})

      # set
      obj['c.z.value_two'] = 200
      # NestedAttrDict({'a': 1, 
      #                 'b': 2, 
      #                 'c': NestedAttrDict({'y': 20, 
      #                                      'z': NestedAttrDict({'value': 100,
      #                                                           'value_two': 200})})})

