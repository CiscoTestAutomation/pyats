.. _resources_debugging_python:

Debugging Python
================

The best way to debug Python is to use the built in ``pdb`` debugger. It
provides an interactive source code debugger for Python programs, including
setting breakpoints and stepping, etc.

PDB
---

Everything you need to know about ``PDB`` is here: 
`The Python Debugger <https://docs.python.org/3/library/pdb.html>`_.

Everyone should thoroughly read it. There is no better, native way to debug
python programs.

.. code-block:: python
    
    # Example
    # -------
    #   
    #   putting a break in your code

    # yourPythonCode.py
    
    # code ...
    # code ..
    # code .

    # import python debugger and start to trace
    import pdb; pdb.set_trace()

    # code .
    # code ..
    # code ...

When your code executes to ``import pdb; pdb.set_trace()``, it breaks and
goes into an interactive shell:

.. code-block:: text
    
    # output ...
    # output ..
    # output .

    (pdb) 

This is not the same as your typical python interactive shell. There are some
differences, for example, built-in commands like ``w(here)``, ``a(rgs)`` etc.
Refer to the above documentation for details.

.. hint::

    there is also a module called ``ipdb`` from IPython, which provides all
    the functionality of ``pdb`` along all of IPython's goodies.


Dynamic Code Modification & Evaluation
--------------------------------------

If you're asking this question, you are likely to be coming from a Tcl coding
background. Unfortunately, there's no equivalent support for Tcl commands like
``edprocs``, ``interpreter`` and etc. It's just not Python or Pythonic.

    Didn't they say you can ``reload`` a module?

Yes, but reloading has severe disadvantages and limitations. Checkout the 
documentation on ``importlib.reload`` 
(`Link <https://docs.python.org/3.4/library/importlib.html?highlight=reload#importlib.reload>`_):

* Existing class instances are not reloaded when their parent class module is 
  reloaded. They continue to use the old class methods.

* Modules that are designed to be instantiated once will be broken.

* Reloading a module does not reload its dictionary: it is retained. Only
  redefinition of names will override its old definitions.

Keep in mind that Python is all about classes and objects. You cannot change
an object's class after it's created. 

    Can't you use ``eval`` and ``exec`` to dynamically evaluate code?

Yes, but that's a **highly** unsuggested way to execute python code. If you're
using them, you're doing it wrong. Just because Python provides you a tool,
doesn't mean you should abuse it. There are many reasons why you shouldn't do 
it, and they are well covered from many sources.


Rapid Prototyping
-----------------

The trick with interpreted language is to use the interpreter: go into the 
interactive mode and try stuff.

.. code-block:: text
    
    $ python
    Python 3.4.1 (default, Nov 12 2014, 13:34:48) 
    [GCC 4.4.6 20120305 (Red Hat 4.4.6-4)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 

You can do anything and everything. Try to code rapidly in the interpreter, or
create your own stub environment in a lightweight Python script, before you put 
them into a big library/script and running the whole schebang. This method of
development will save you a ton of time.

.. code-block:: python

    # Example
    # -------
    #
    #   what a quick edit/test script could look like in pyATS

    # working with a testbed
    from pyats.topology import Testbed

    # working with tcl
    from pyats import tcl

    # import result codes
    from pyats.results import *

    # create a tb
    tb = Testbed(config_file = '/path/to/testbed.yaml')

    # grab a device
    d = tb.devices['uut']

    # connect it if needed
    d.connect()

    # now you can do whatever you want.
    # throw your testcode in here.
    def myTestcaseSetup(self):
        # code...

        pass

    # wait, what's this self thing, isn't it part of a class?
    # yes and no. :) read up on it.
    # http://stackoverflow.com/questions/2709821/what-is-the-purpose-of-self-in-python
    self = {'id': 'myTestcase',
            'description': '',
            'script_args': {
                'testbed': tb,
            }
            'result': Passed}

    # test it 
    myTestcaseSetup(self)

    # throw in a debugger for kicks
    import pdb; pdb.set_trace()


Now you have a quick-test environment where you can code and test.. without
running the whole test script, as long as your testbed is configured up front.
The only thing that might take a while is the device connection itself. However,
once you're paused at ``pdb``, you can interactively do more... sky's the limit.

Debugging in IDEs
-----------------

Some python IDEs, such as Visual Studio Code, PyCharm and Eclipse, comes with native support for
breakpoints and debugging. Use at your own discretion.
