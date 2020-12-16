Dictionary Represented Using Lists
==================================

Accessing nested dictionaries often calls for recursive functions in order to
properly parse and/or walk through them. This isn't always easy to code around.
``ListDict`` provides an alternative view on nested dictionaries, breaking down
the value nested within keys to a simple concept of *path* and *value*. This
flattens the nesting into a linear list, greatly simplifying the coding around
nested dictionaries.

Concept
-------

Consider the following nested dictionary:

.. code-block:: python
    
    # Nested Dict
    # -----------

    d = {
        'a': {
            'b': {
                'c': {
                    'd': 'value',
                },
            },
        },
        'x': {
            'y': {
                'z': 100,
            },
        },
    }


    # accessing 'value', means
    d['a']['b']['c']['d']
    # 'value'

    # accessing 100, means
    d['x']['y']['z']
    # 100

Looking at the above code, it's not hard to generalize the access pattern into
path/value, where:
    
    - ``d['a']['b']['c']['d']`` can be broken down to:

        - Path: ``['a', 'b', 'c', 'd']``

        - Value: ``'value'``

    - ``d['x']['y']['z']`` can be broken down to:

        - Path: ``['x', 'y', 'z']``

        - Value: ``100``

Where each path value represents a level of dictionary nesting, with the last
path key holding the final value at the end of the chain.

Taking advantage of this pattern, ``ListDict`` takes each nested ``dict`` and
breaks it down into a list of ``(path, value)`` (``DictItem`` namedtuples):

.. code-block:: python

    # Representing Nested Dict using path/value
    # -----------------------------------------
    #
    #   reusing the dictionary 'd' from before

    from pyats.datastructures import ListDict

    # ListDict format:
    #   [(path_x, value_x), 
    #    (path_y, value_y),
    #     ... ]
    #
    # where path is of the form tuple():
    #   (nesting_a, nesting_b, ... , final_key)

    ld = ListDict(d)
    # [DictItem(path=('x', 'y', 'z'), value=100), 
    #  DictItem(path=('a', 'b', 'c', 'd'), value='value')]

Each item stored within a ListDict corresponds to a path of nested dicts to a
stored end value. Same paths always yield the same ``dict``, for example:

.. code-block:: python
    
    # Understanding Paths
    # -------------------
    #
    #   same paths always yield the same dict

    # given path ('a', 'b', 'c') and ('a', 'b', 'e')
    # notice that the first two position 'a' and 'b' are similar
    # and only the last position 'c' and 'e' is different.

    # this suggests the following nested datastructure:
    suggest = {
        'a': {
            'b': {
                'c': object(),
                'e': object(),
            },
        },
    }

Creation
--------

A ``ListDict`` can only be instantiated from another (nested) ``dict``.

.. code-block:: python

    # Example
    # -------
    #
    #   Creating ListDict

    from pyats.datastructures import ListDict

    # reusing 'suggest' variable from previous section
    ld = ListDict(suggest)
    # [DictItem(path=('a', 'b', 'e'), value=<object object at 0xf7683f40>), 
    #  DictItem(path=('a', 'b', 'c'), value=<object object at 0xf7683d00>)]

The returned datastructure is simply a list, except that the content of the list
is always of format path/value (``DictItem`` named tuple).


Access & Reconstruction
-----------------------

``ListDict`` is an extension (inheriting from) ``list``, and thus all known APIs
of ``list`` is expected to continue to work.

.. code-block:: python

    # Example
    # -------
    #
    #   Accessing ListDict

    from pyats.datastructures import ListDict

    # reusing 'ld' from above
    ld[0]
    # DictItem(path=('a', 'b', 'e'), value=<object object at 0xf7683f40>)
    ld[0].path
    # ('a', 'b', 'e')
    ld[0].value
    # <object object at 0xf7683f40>

One important property of each ``ListDict`` is that it is *mutable*: the content
of each instance can be modified, which means when you flatten out a nested
dict, you have the ability to add and/or remove content from it as needed.

.. code-block:: python
    
    # Example
    # -------
    #
    #   modifying and looping ListDict

    # continuing from above example...

    # appending a new path/value
    ld.append((('a', 'b', 'x'), object()))
    # [DictItem(path=('a', 'b', 'c'), value=<object object at 0xf7692d00>), 
    #  DictItem(path=('a', 'b', 'e'), value=<object object at 0xf7692f40>),
    #  DictItem(path=('a', 'b', 'x'), value=<object object at 0xf7692ea8>)]

    # looping through
    for i in ld:
        print(i)
    # DictItem(path=('a', 'b', 'c'), value=<object object at 0xf7692d00>)
    # DictItem(path=('a', 'b', 'e'), value=<object object at 0xf7692f40>)
    # DictItem(path=('a', 'b', 'x'), value=<object object at 0xf7692ea8>)

    # etc..

.. hint::

    the whole point of ``ListDict`` and breaking information down to path/value
    is so that users can easily loop through the whole original datastructure
    and do ...stuff... not having to write recursive functions.

At the end, each ``ListDict`` object can also be re-constructed from its special
path/value format, back to its represented ``dict`` format by calling the
``reconstruct()`` api.

.. code-block:: python

    # Example
    # -------
    #
    #   reconstructing a dict from ListDict
    
    # continuing from above example...
    new_dict = ld.reconstruct()
    # {'a': {
    #     'b': {
    #         'x': <object object at 0xf7716ce8>, 
    #         'c': <object object at 0xf7716f40>, 
    #         'e': <object object at 0xf7716ea8>}
    #     }
    # }

    # id(new_dict) is not the same as id(suggest)
    id(new_dict) == id(suggest)
    # False

The creation of a ``ListDict`` object and reconstructing a ``dict`` object is
the easiest way to take nested ``dict`` formats, flatten it, operate on it, and
return it to original state. However, keep in mind that the process is 
*destructive*: the newly created dictionary is a new object.

