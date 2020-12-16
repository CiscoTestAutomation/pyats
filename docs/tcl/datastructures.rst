Custom Data Structures
======================

``tcl`` module offers two custom datastructures: ``Array`` and ``KeyedList``. 
As you may have guessed, they are the Python counterparts of Tcl's array and
keyed list data structures. This is needed in order to fully map Tcl variables
into Python objects, maintaining a Pythonic programming experience.

.. note::
    ``Array`` and ``KeyedList`` implementations are simply to enable users to
    deal with Tcl outputs (eg, parser returns). They should not be used 
    in Python code, since there are... better datastructure native to Python.

.. _tcl-array:

Array
-----

Class ``Array`` was created to offer direct typecasting of a whole Tcl Array 
type variable to a single Python object whilst feature the same look-and-feel.

.. code-block:: python
    
    # Example
    # -------
    #
    #   creating Tcl arrays in Python

    from pyats import tcl
    from pyats.tcl import tclstr, Array

    # create an array in Tcl
    # using one liner array set instead of ().. for less typing
    tcl.eval('array set testArray "a 1 b 2 c 3"')

    # copy it to Python
    array = tcl.get_array('testArray')

    # notice how we have an Array variable
    assert type(array) is Array

Python ``Array`` class implementation extends the base ``dict``. The resulting
object features the same concept as Tcl - but think Pythonic. There's no
``array names`` API, but rather:

.. code-block:: python

    # continuing from last code...

    # check that array contains index 'a'
    assert 'a' in array

    # check all array index are in the array
    assert set(['a','b','c']) == set(array.keys())

    # accessing the array
    # note that the value is still string - not typecasted
    assert array['a'] == '1'

    # adding more to the array
    # note that this only adds to the local variable
    array['zzz'] = 999

When a Tcl Array is typecasted into ``Array`` object, it gets its content and
copies it to Python - that is, the Python object is stand-alone and not linked
to the Tcl source variable. Any modifications to one variable does not affect
the other. In addition, the value of each array index value is not typecasted. 
If those values (which remains in string format) needs to also be typecasted, 
user should loop through the index and typecast each value individually.

The reverse operation is also possible. To convert an ``Array`` object back 
to its Tcl form, call the ``tclstr()`` function. This API returns a list - 
a form accepted by ``array set <arrayName> <valueList>`` call, which creates an 
array from a list of key-value pairs. 

.. code-block:: python
    
    # continuing where we left off...
    
    # calling tclstr() to get a glimpse of the output
    tclstr(array)
    # output: 'a 1 c 3 b 2 zzz 999'
    # note how it's a Tcl [array get <arrayName>] format

    # setting it back to Tcl using native commands
    tcl.eval('array set newArray {%s}' % (tclstr(array),))
    
    # checkout the content
    tcl.eval('parray newArray')
    # newArray(a) = 1
    # newArray(b) = 2
    # newArray(c) = 3
    # newArray(zzz) = 999

    # of course, you can always call the set_array API
    tcl.set_array('newArray', array)

.. warning::
    calling ``array set <arrayName> <valueList>`` on an existing array does 
    NOT replace it. This merely update it (add new keys-values, replace 
    existing key-values). This is similar in concept as ``dict.update()``.
    If you want to fully replace an existing array, delete the old one first!

.. _tcl-keyedlist:

Keyed Lists
-----------

Tcl Keyed-List is really just a string/list that follows a particular
syntax. When using the right keyed list APIs, the following properties of 
keyed-lists are observed:

- A key may be associated to a value, or another keyed-list
- If a key is associated to another keyed-list, then associated keyed-list's 
  keys are called a sub-keys of a that first key.
- Key and subkeys are separate by the special ``.`` character

Our ``KeyedList`` class is a Python implementation of the above Tcl keyed-list
behavior, with enhanced APIs more natural to those of Python design patterns.

.. code-block:: python
    
    # Example
    # -------
    #
    #   creating Tcl keyed lists in Python

    from pyats import tcl
    from pyats.tcl import KeyedList

    # create a keyed-list in Tcl
    tcl.eval('keylset myKeyedList a.x 1 a.y 2 b 3')
    # the content is now:
    # {'a': {'y': '2', 'x': '1'}, 'b': '3'}

    # now read it to Python
    klist = tcl.get_keyed_list('myKeyedList') 
    
    # note the behaviors:
    #  - keys and subkeys separator via .
    #  - the content of a keyed list can be also another keyed list
    assert 'a' in klist
    assert 'a.y' in klist
    assert type(klist['a']) is KeyedList

    # getting values
    sub_klist_a = klist['a']
    # this returns another keyed-list
    # with content: {'y': '2', 'x': '1'}

    # getting key.subkey values
    assert klist['a.x'] == '1'

    # because key a contains sub-keyedlist with x and y
    # in Python we can chain the index [] behavior without using .
    assert klist['a']['x'] is klist['a.x']
    # note that it's probably easier to use .
    # but the idea here is to show how the objects work

In effect, keyed-lists are kind of like Python dictionaries, except if a ``.``
is used then the content should be another keyed-list - e.g. nested dictionary.

Therefore, notice above how when a key's associated value is also a keyed list, 
then you can access it directly using ``.`` separator, instead of having to 
chain ``[ ]`` index operator. Our implementation of ``KeyedList`` class takes 
care of the nested nature of keyed-lists for the user.

You can also create ``KeyedLists`` on the fly:

.. code-block:: python
    
    # Example
    # -------
    #
    #   creating KeyedList content on the fly in Python

    from pyats.tcl import KeyedList
    
    # create a blank object
    klist = KeyedList()
    
    # add some keys and subkeys
    klist['a.x'] = 1
    klist['b.y.z'] = 2
    klist['c'] = 3
    
    # let's see the output.
    # note how sub-keys were automatically created into keyed lists.
    klist
    # {'b': {'y': {'z': 2}}, 'a': {'x': 1}, 'c': 3}

    # you can also create a klist from kwargs
    # but this limits you to one key only, as Python does not support
    # kwargs keys to contain .
    KeyedList(a = 1, b = 2)
    # output: {'b': 2, 'a': 1}
    # hence this isn't really the best way of creating a python keyed list.

.. note::
    
    ``KeyedList`` class was created for ease-of using Tcl code in Python. If
    writing original Python code, there's no point in using this class - use 
    native Python classes instead.
    
    Just because you're familiar with it doesn't mean you should use it. 
    Bringing Tcl concepts into Python is not recommended.

Similarly to ``Array`` class, to save back to Tcl, call the ``tclstr()``
function.

.. code-block:: python

    # continuing from above section

    # let's see some output
    tclstr(klist)
    # '{b {{y {{z 2}}}}} {a {{x 1}}} {c 3}

    # set it back to Tcl
    tcl.eval('set newKlist {%s}' % (tclstr(klist),))

    # let's see the keys
    tcl.eval('keylkeys newKlist')
    # 'b a c'

    # alternatively, use set_keyed_list API
    tcl.set_keyed_list('altKList', klist)
    tcl.eval('keylkeys altKList')
    # 'b a c'


