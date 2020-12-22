Introduction
============

Did you know that Python is natively compatible with Tcl?

As a matter of fact, Tk is the de-facto language used for Python GUI front-ends:
for example, IDLE is entirely written using Tk calls from within Python.

The native Python module that enables Tcl integration is called ``tkinter``:

.. code-block:: python

    # import the Tcl object
    from tkinter import Tcl

    # create a new Tcl interpreter
    tcl = Tcl()

    # example Tcl calls
    tcl.eval('set myTclVariable {%s}' % 1)


This module effectively enables you to make Tcl calls in the current Python
process, and is 100% embedded: there's no child Tcl process; the actual Tcl
interpreter is embedded within the current Python process, and the ``pid`` of
both Python and Tcl is the same. 

.. tip::
    
    making Tcl calls within Python is in effect, passing a string (``str``)
    object to the ``eval`` attribute of Tcl instance object. Therefore string
    operations (such as substitution) is perfectly supported/legal.

However, the raw functionality provided by this module is rather crude. Crude
in the sense that whilst it does provides the basic fundamental infrastructure,
allowing users to practically make any and all calls to Tcl (including loading
other packages), it does not provide an additional layer on top of the Tcl
language to make it more user friendly. Example:

.. code-block:: python

    from tkinter import Tcl

    tcl = Tcl()

    # load up Tclx
    tcl.eval('package require Tclx')

    # create a keyed list
    tcl.eval('keylset myKlist key_a value_a key_b value_b')

    # wouldn't it be nice to be able to cast the tcl keyed list to a python
    # object, instead of having to do this?
    key_a_value = tcl.eval('keylget myKlist key_a')
    key_b_value = tcl.eval('keylget myKlist key_b')


Documentation to ``tkinter`` can be found at:

* https://wiki.python.org/moin/TkInter

* https://docs.python.org/3.4/library/tkinter.html


Tcl Enhanced
------------

Part of pyATS goal is to enable the testing community to leverage existing
Tcl-based scripts and libraries. In order to make the integration easier, the
``tcl`` module was created to extend the native Python-Tcl interaction:

* **Interpreter class:** extends the native Tcl interpreter by providing access
  to ATS-tree packages & libraries.

* **Two-Way Typecasting:** APIs and Python classes, enabling typecasting Tcl 
  variables to its appropriate Python objects and back. Including but not 
  limited to: ``int``, ``list``, ``string``, ``array``, ``keyed lists`` etc.

* **Call history:** maintaining a historical record of Tcl API calls for 
  debugging purposes.

* **Callbacks:** callbacks from Tcl to Python code, enabling closer coupling

* **Dictionary Access:** accessing Tcl variables as if accessing a python
  dictionary.

* **Magic Q Calls:** calling Tcl APIs as if calling a python object method, with
  support for Python ``*args`` and ``**kwargs`` mapping to Tcl positional and 
  dashed arguments.


Requirements
------------

The following is required for this module to function:

#. ``tkinter`` module compiled and working

When Python is first compiled, it looks up the current environment to determine
what modules can be compiled & linked, and what is missing. This information
is printed out at the end of ``make``.

The base Python ``tkinter`` module is compiled only when Python detects the
presence of Tcl header files, and can link the compiled module against Tcl
``*.so`` files. This is step automatically done if you are using the 
``build_python`` script supplied with pyATS installation. You can verify 
whether ``tkinter`` was compiled and linked properly in Python by importing the
module and trying to create an interpreter instance as shown in introduction
above.
