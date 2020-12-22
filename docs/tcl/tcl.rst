Tcl & Interpreter
=================

``Interpreter`` class is an extension of ``tkinter.Tk`` class, inhering all of 
Python's native Tcl integration whilst providing extended APIs for ease
of use.


Creating Local Interpreters
---------------------------

Users are free to create instances of ``Interpreter`` class and make Tcl calls
anywhere in their script and/or library code:

.. code-block:: python

    # import Interpreter
    from pyats.tcl import Interpreter

    # create an instance
    tcl = Interpreter()

    ats_tcl_tree_path = tcl.eval('set ::env(AUTOTEST)')

    # getting tcl version
    tcl.eval('info patchlevel')

.. hint::
    
    Note the object-orientedness of this approach: each time an ``Interpreter``
    class is instantiated, a different object/interpreter is returned. This
    enables the creation of distinct Tcl instances, but also is fundamentally
    different from how a typical Tcl script is executed: always within the same 
    interpreter.


The Global Interpreter
----------------------

Python is object oriented: everything is an object. And therefore in Python,
when an ``Interpreter`` class instance is created, it is simply another object, 
and there could be an arbitrary number of such instances. Each of them would
be independent and holds their own variables, procedures namespaces & etc.

And thus arises the issue: in Tcl, everything assumed that it was always running
under the same interpreter.

To follow the same behavior, and load libraries, functions, and connection 
handles in the same interpreter instance, we need to maintain the usage of a 
single instance ``Interpreter``. The most pythonic way would be to create an
instance of it and carry it throughout your script/code, and passed around as
argument. However, this creates a huge amount of overhead and unnecessary 
coding.

This module features a special mechanism that offers a similar concept of
*global* ``Interpreter`` instance:

.. code-block:: python
    
    # import the tcl module
    from pyats import tcl

    # use the module directly to make tcl calls
    tcl.eval('set myVar 1')

The ``tcl`` module itself is also the global instance of ``Interpreter`` class.
Within the same Python process, the ``tcl`` module always refers to the same
``interpreter`` instance. This eliminates user's need to explicitly create
new ``Interpreter`` instances and having to pass them around, drastically 
reducing code complexity & time to market.

.. code-block:: python
   
   # import the tcl module
   from pyats import tcl

   # tcl module is also an instance of Interpreter class
   assert isinstance(tcl, tcl.Interpreter)

   # however/wherever/whenever the tcl module is imported,
   # the same global Interpreter instance object is always returned
   import pyats.tcl
   assert ats.tcl is tcl
   assert id(ats.tcl) == id(tcl)

.. tip::
    
    unless you have a specific need to create a local ``Interpreter`` instance
    to encapsulate some Tcl code, always use this global instance.

.. note::
    
    as the ``tcl`` module is also a global ``Interpreter`` instance, all of its
    features/APIs & etc are also inherited. Therefore,  documentations w.r.t.
    ``Interpreter`` instance is also applicable to this global instance. For
    variety's sake, examples are given using either.


Making Tcl Calls
----------------

Any and all Tcl commands can be called directly within the ``Interpreter``
instance (and similarly, through the global instance).

As Tcl is a string-interpreted language where everything is a string, evaluating
Tcl calls within Python is effectively the same as evaluating a string object
containing Tcl code using the interpreter's ``eval()`` function.

.. code-block:: python
    
    # import the global tcl instance
    from pyats import tcl

    # make tcl calls
    tcl.eval('info global')
    tcl.eval('proc testProc {args} {puts $args}')

    # load packages from ATS tree
    tcl.eval('package require Tclx')

You can pass Python information to Tcl commands via string substitution. 
However, note that you have to be careful in using braces ``{ }`` to contain 
the information into a single list/string. This is due to string substitution
occurring first in Python, and if the brace was not present, you'd get a nasty 
error:

.. code-block:: python
    
    # let's try a local interpreter instead
    from pyats.tcl import Interpreter

    # instantiate a local interpreter
    tcl = Interpreter()

    # for the sake of demonstration, let's prove that this
    # instance is not the same as the global instance
    import pyats.tcl
    assert tcl is not ats.tcl

    # moving on with our demo

    # variable to be passed to substitution
    info = 'list information'

    # make a tcl call.. without {}. 
    # see the error
    try:
        tcl.eval('set var %s' % info)
    except e:
        print(e)
    
    # The error would be:
    #
    #   Traceback (most recent call last):
    #     File "<stdin>", line 1, in <module>
    #     File "ats/tcl/interpreter.py", line 221, in eval
    #       return self.tk.eval(code)
    #   _tkinter.TclError: wrong # args: should be "set varName ?newValue?"
    #
    # as after the substitution the command became invalid:
    # tcl.eval('set var list information')
    
    # now do it properly.
    tcl.eval('set var {%s}' % info)

    # this would've translated to
    # tcl.eval('set var {list information}')

    # test that it worked
    asset tcl.eval('set var') == info


Getting Raw Returns
-------------------

All returns from Tcl is in the form of a string (``str`` object). This is
inline with how Tcl treats everything as strings, where even lists are only 
strings with spaces as separators and braces as sub-list containers.

.. code-block:: python

    from pyats import tcl

    # create a tcl variable, storing a number
    tcl.eval('set myVariable %s' % 9999)
    
    # read out the variable to a python object
    myVar = tcl.eval('set myVariable')

    # note that the obj type is str
    assert type(myVar) is str

    # create a procedure in Tcl, returning its called arguments
    tcl.eval('proc myTestProcedure {args} {return $args}')

    # call it
    ret = tcl.eval('myTestProcedure -argA 1 -argB 2')

    # and the string would be returned
    assert ret == '-argA 1 -argB 2'

.. hint::
    
    ``set`` API reads and returns a variable's content if no value was
    provided. This is needed because you need to *return* a variable from Tcl
    to Python. Using ``puts`` will not suffice, because that only prints to 
    screen (STDIO)



Things To Know
--------------

#. When ``Interpreter`` or ``tkinter`` is loaded inside Python, it exists as 
   a native Tcl environment within Python, running Tcl C code internally. Thus 
   there is no separate Tcl PID inside Unix. Tcl ``pid`` call returns the
   same PID as the Python process.

#. If ``debug`` or ``interpreter`` call is made within Tcl, the Tcl process 
   takes over STDIO, pauses and gives user the typical ``expect>`` or ``dbg>`` 
   prompt. This is the same behavior as in native Tcl. Exiting 
   debug/interpreter mode continues the script execution.

#. If Tcl opens up a communication port, it acts as if it had native
   controls. Python passes the handle to Tcl.

#. If a process fork is made within Tcl, a child Python process is created 
   with the same Tcl interpreter loaded at the point of forking. In Linux this
   looks as if the parent Python process has many child Python processes.

#. Arguments to Tcl has to be in the form of strings. If you want to pass an
   object, convert it to its string form.

#. Interpreter always evaluates at the global scope. To access namespaces, fully
   qualify your namespace/API names with namespace qualifiers.

#. If you exited a Python/Tcl process and your shell prompts are messed up with
   the following symptoms: no newlines when hitting enter and typing yields
   invisible characters, type ``stty sane`` and hit enter. This will fix it. 
   This is a known issue (although we don't know what's causing it), and will 
   eventually be looked into.


There is still much to be discovered in terms of Python-Tcl interactions. Basic
testing suggests that everything seems to work correctly - but there might be
corner conditions. Unfortunately ``tkinter``'s Tcl side is poorly documented (as
the original focus from Python was on Tk portability), so if there's something
puzzling you, contact the support team, and maybe we can sort it out.
