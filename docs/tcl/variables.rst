Variables & Typecasting
=======================

Tcl is string based: from code to variables to returns, they are all evaluated
as strings. Technically speaking, the getting & setting of all Tcl variables
can be done strictly by evaluating the ``set`` API, and typecasting it yourself.
But that's a lot of overhead to be typed every time:

.. code-block:: python
    
    # Example
    # -------
    # 
    #   setting & getting variables with Tcl and typecasting them.

    from pyats import tcl

    # setting variables
    tcl.eval('set myVar 1')

    # getting variables
    value = tcl.eval('set myVar')

    # typecasting to int
    value = int(value)

The goal of this ``tcl`` module is to make Tcl feel more integrated with Python
and to make two way data-type conversions easier. Keep reading :-)

Variable Dictionary
-------------------

In an effort to streamline setting & getting Tcl variables, the ``Interpreter``
class features a dictionary style quick set/get mechanism.

.. code-block:: python

    # Example
    # -------
    # 
    #   dict style setting & getting variables

    from pyats import tcl

    # setting variables
    tcl.vars['myVar'] = 1

    # getting variables
    value = tcl.vars['myVar']

    # this also works with array elements
    tcl.vars['myArray(ironman)'] = 'tony stark'
    tcl.vars['myArray(mk1,color)'] = 'steel silver'
    # myArray(ironman)   = tony stark
    # myArray(mk1,color) = steel silver

    # reading array elements
    name = tcl.vars['myArray(ironman)']

This allows users to read/set variables on the Tcl side as if it was a Python
style dictionary, with each key being the variable name. You can also use full
namespace qualifiers with this mechanism.

.. code-block:: python

    # Example
    # -------
    # 
    #   dict style setting & getting variables using full qualifiers

    from pyats import tcl

    # setting variables
    tcl.vars['::aGlobalVar'] = 999

    # getting variables
    tcl_auto_path = tcl.vars['::auto_path']


Automatic Tcl Typecasting
-------------------------

The ``Interpreter`` class provides a ``cast_any`` API to make *best-effort* 
typecasting of Tcl returns to Python object types. This can also be done per
evaluate call if users pass in ``typecast=True`` to ``eval()``.

``Interpreter.cast_any(value)``
    takes a Tcl string value and perform a best-effort attempt at converting it
    into its equivalent Python object.

.. code-block:: python
    
    # Example
    # -------
    # 
    #   casting anything from Tcl by guesstimating

    from pyats import tcl

    # setting a variable in tcl and returning its value to Python also
    # note that Tcl set API always return the content of the variable as well
    result = tcl.eval('set var %s' % 1)

    # assert that number 1 has been turned into string
    assert type(result) is str

    # now try typecasting
    result = tcl.cast_any(result)

    # it becomes an int
    assert type(result) is int

    # now try the direct evaluation typecasting
    direct_result = tcl.eval('set var %s' % 1, typecast=True)

    # it's an int already
    assert type(direct_result) is int

The functionality of this *best-effort* typecasting is limited. It currently 
supports the following only:

* Integer

* Float

* Boolean

* KeyedLists

* String

.. note::

    arrays and lists are not supported by ``cast_any`` because arrays in the 
    form of ``[array get arrayName]`` is just another list (with even elements, 
    key followed by value), and it lists are just strings in Tcl. It is 
    impossible to guess whether a string return is a list, or a string, and thus
    arrays in list formats are also subsequently not supported.


Specific Tcl Typecasting
------------------------

It is also possible to do specific typecasting of the above types as opposed to
making letting the code to guesstimate the data type. There are various casting
methods ``cast_*`` featured in the Interpreter class. This is probably the safer
method to do casting. The following methods are available:

``Interpreter.cast_int(value)``
    takes a Tcl string form integer numbers and converts it to Python ``int`` 
    object.

``Interpreter.cast_double(value)``
    takes a Tcl string form double/float numbers and converts it to Python 
    ``float`` object.

``Interpreter.cast_boolean(value)``
    takes a Tcl string form boolean and convert it to Python ``bool``. Note that
    in Tcl, 0 is False, and all other integers are True.

``Interpreter.cast_list(value)``
    takes a Tcl list and converts it into a Python ``tuple``.

``Interpreter.cast_array(value)``
    takes a Tcl list of key/value pairs (eg. the output of ``[array get]``) and
    convert it to ``Tcl.Array`` class object.

``Interpreter.cast_keyed_list(value)``
    takes a Tcl keyed list and convert it to ``Tcl.KeyedList`` class object.

.. code-block:: python
    
    # Example
    # -------
    # 
    #   performing specific casting of returns from Tcl

    from pyats import tcl

    # Tcl Integers
    # ------------
    tcl.cast_int('9999')
    9999

    # Tcl Doubles
    # -----------
    tcl.cast_double('3.1415926')
    3.1415926

    # casting Tcl Booleans
    # --------------------
    tcl.cast_boolean('1')
    True
    tcl.cast_boolean('0')
    False

    # Tcl Lists
    # ----------
    #   casting a Tcl list into Python tuple
    tcl.cast_list('a b c')
    ('1', '2', '3')
    tcl.cast_list('a b c {1 2 3}')
    ('a', 'b', 'c', '1 2 3')
    # casting Tcl list and also convert list element into Python objects
    tcl.cast_list('1 2 3', item_cast=int)
    (1, 2, 3)

    # Tcl Arrays
    # ----------
    #   casting a Tcl array into ats.tcl.Array class
    #   note that this expects an array in the form of [array get name], eg.
    #   a list of key/value pairs.
    tcl.eval('set myArray(a) 1')
    tcl.eval('set myArray(b) 2')
    array_string = tcl.eval('array get myArray')
    tcl.cast_array(array_string)
    Array({'a': '1', 'b': '2'})
    # casting arrays and also converting array content into Python objects
    tcl.cast_array(array_string, int)
    Array({'a': 1, 'b': 2})

    # Tcl Keyed Lists
    # ---------------
    #   casting Tcl keyed lists into ats.tcl.KeyedList class
    tcl.eval('keylset klist a 1 b.c 2 d.e.f 3')
    klist_string = tcl.vars['klist']
    tcl.cast_keyed_list(klist_string)
    KeyedList({'a': '1', 
               'b': KeyedList({'c': '0'}), 
               'd': KeyedList({'e': KeyedList({'f': '1'})})})
    # casting keyed lists and converting their content into Python objects
    tcl.cast_keyed_list(klist_string, bool)
    KeyedList({'a': True, 
               'b': KeyedList({'c': False}), 
               'd': KeyedList({'e': KeyedList({'f': True})})})

.. tip::

    there is no such thing as Array typecasting, as there's no such thing
    as "returning an Array" in Tcl. ``return [array get myArray]`` returns a 
    list in the format of "key value key value ..." and is indifferent from 
    any other list, and thus cannot be guessed.

.. tip::

    Tcl does not have a boolean type. All integers can be safely evaluated as a
    boolean (0 is False, everything else is True including negative numbers).
    Since we cannot safely assume whether an integer string in Tcl is a boolean
    or a number, its automated guess-typecasting is not supported. All integer
    type strings are simply returned as ``int``


Automatic Python Typecasting
----------------------------

To cast Python objects to Tcl, the ``tcl`` module features ``tclstr()``, an API 
with functionality similar to Python ``str()``:

* call an object's ``__tclstr__()`` attribute if it has one.

* attempt to convert that object into is equivalent Tcl string format.

and return the string format result.

``tclstr(obj)``
    returns the most appropriate Tcl string format of the given object.

We only need this one API to convert Python objects to Tcl string 
representations due to the ability to determine the class type of the input 
object.

.. code-block:: python

    # Example
    # -------
    # 
    #   using tclstr() API

    from pyats import tcl
    from pyats.tcl import tclstr

    # casting list of list to Tcl format
    list_of_list = [1, 2, [3, 4]]
    tclstr(list_of_list)
    '1 2 {3 4}'

    # casting a dict into a tcl array. note the usage
    dictionary = {'my key': 'my value', 'a': 'b'}
    tclstr(dictionary)
    '{my key} {my value} a b'
    tcl.eval('array set myArray {%s}' % tclstr(dictionary))

    # call an object's __tclstr__ attribute and return its Tcl format.
    array = tcl.Array(a = 1, b = 2, c = 3)
    tcl.eval('array set myArray {%s}' % tclstr(array))
    # myArray(a) = 1
    # myArray(b) = 2
    # myArray(c) = 3

    klist = tcl.KeyedList()
    klist['key.subkey'] = 'value'
    tcl.vars['klist'] = tclstr(klist)
    '{key {{subkey value}}}'

Because of the specific behavior of ``tclstr()`` where it tries to always
call an object's ``__tclstr__()`` attribute (if any) to convert it to Tcl string
format, users can create Python classes that can be direct translatable to Tcl
by implementing that class's ``__tclstr__`` attribute to do custom conversions.

.. code-block:: python
    
    # Example
    # -------
    # 
    #   creating a tcl compatible dictionary

    from pyats import tcl
    from pyats.tcl import tclstr

    # define my custom class by inhering Python dict
    class TclDict(dict):

        def __tclstr__(self):
            '''converts this dictionary to Tcl array format'''
            
            return ' '.join(['%s {%s}' % (k,v) for k, v in self.items()])

    # let's test it by creating a dictionary
    obj = {'a': 1,
           'b': 2,
           'c': 3,}

    # convert the dictionary to TclDict type
    obj = TclDict(obj)

    # call tclstr on it
    tclstr(obj)
    'a {1} c {3} b {2}'

    # does it work with Tcl?
    tcl.eval('array set myArray {%s}' % tclstr(obj))
    # myArray(a)         = 1
    # myArray(b)         = 2
    # myArray(c)         = 3


More Shortcuts: All-In-One
--------------------------

So far we covered how to read/set variables as strings, and then casting those
strings into their respective Python objects. But what about reading a Tcl 
variable and cast it to type in one shot? What about setting a Tcl variable 
directly from a Python object? 

``Interpreter`` class also provides short-cut APIs that does things in one shot:
set/get variables by name and do the data typecasting together.

``Interpreter.set_int(name, value)``
    equivalent to ``tcl.eval('set %s %s' % (name, str(value)))``

``Interpreter.get_int(name)``
    reads a Tcl variable ``name`` and cast its values into an ``int`` object.

``Interpreter.set_double(name, value)``
    equivalent to ``tcl.eval('set %s %s' % (name, str(value)))``

``Interpreter.get_double(name)``
    reads a Tcl variable ``name`` and cast its values into a ``float`` object.

``Interpreter.set_boolean(name, value)``
    sets Tcl variable ``name`` with 1 for ``True``, 0 for ``False``.

``Interpreter.get_boolean(name)``
    reads a Tcl variable ``name`` and cast its values into a ``bool`` object.

``Interpreter.set_array(name, value)``
    sets Tcl array ``name`` with values from a Python ``Tcl.Array`` object.

``Interpreter.get_array(name)``
    reads a Tcl array ``name`` and cast its values into a ``Tcl.Array`` object.

``Interpreter.set_keyed_list(name, value)``
    sets Tcl array ``name`` with values from a Python ``Tcl.KeyedList`` object.

``Interpreter.get_keyed_list(name)``
    reads a Tcl keyed list ``name`` and cast its values into a ``Tcl.KeyedList``
    object.

.. code-block:: python

    # Example
    # -------
    # 
    #   getting & setting Tcl variables and typecasting all-in-one

    from pyats import tcl

    # Tcl Integers
    # ------------
    tcl.set_int('myInteger', 9999)
    tcl.vars['myInteger']
    '9999'
    intVar = tcl.get_int('myInteger')
    9999

    # Tcl Doubles
    # -----------
    tcl.set_double('myDouble', 3.1415926)
    tcl.vars['myDouble']
    '3.1415926'
    intVar = tcl.get_int('myDouble')
    3.1415926

    # casting Tcl Booleans
    # --------------------
    tcl.set_boolean('myBool', True)
    tcl.vars['myBool']
    '1'
    intVar = tcl.get_boolean('myBool')
    True

    # Tcl Lists
    # ----------
    tcl.set_list('myList', [1, 2, 3, 4, 5])
    tcl.vars['myList']
    '1 2 3 4 5'
    listVar = tcl.get_list('myList')
    ('1', '2', '3', '4', '5')


    # Tcl Arrays
    # ----------
    tcl.set_array('myArray', tcl.Array(a = 1, b = 2, c = 3))
    tcl.eval('parray myArray')
    # myarray(a) = 1
    # myarray(b) = 2
    # myarray(c) = 3

    # reading tcl arrays by name and typecasting
    array = tcl.get_array('myArray)')
    Array({'c': '3', 'b': '2', 'a': '1'})

    # Tcl Keyed Lists
    # ---------------
    tcl.set_keyed_list('myKlist', tcl.KeyedList(a = 1, b = 2, c = 3))
    tcl.vars['myKlist']
    '{c 3} {b 2} {a 1}'

    # reading tcl arrays by name and typecasting
    klist = tcl.get_keyed_list('myKlist')
    KeyedList({'c': '3', 'b': '2', 'a': '1'})

