.. _object_model:

Object Model
============

.. sidebar:: Helpful Reading

    - `Data Model`_

    - `Modules Tutorial`_

    - `Classes Tutorial`_

    - `The Import System`_

    - `Docstring Conventions`_

.. _Data Model: https://docs.python.org/3.4/reference/datamodel.html
.. _Modules Tutorial: https://docs.python.org/3.4/tutorial/modules.html
.. _The Import System: https://docs.python.org/3/reference/import.html
.. _Classes Tutorial: https://docs.python.org/3.4/tutorial/classes.html
.. _Docstring Conventions: https://www.python.org/dev/peps/pep-0257/

In ``aetest`` scripts, sections are defined via the use of Python classes and
class methods. During runtime, ``aetest`` infrastructure discovers these
sections based on their class inheritance & decorator markers, sorts them to
their appropriate run order, and instantiates them into their corresponding
instance objects.

This section provides insight on how this delicate process is carried out.


TestScript Class
----------------

``aetest`` testscripts are simply standard python files with ``.py`` extension.
They are called ``aetest`` testscripts because they import the AEtest module
(``from pyats import aetest``), and has section definitions such as
``CommonSetup``, ``Testcase``, and ``CommonCleanup``.

In Python, ``.py`` files are imported into Python as module objects. During
``aetest`` execution, the infrastructure internally wraps the running testscript
module into a ``TestScript`` class instance.

.. code-block:: python

    # Example
    # -------
    #
    #   what this means...
    #   assuming there's a script called l3vpn_traffic.py

    # importing some helper modules for demonstration
    import types

    # import the script as a module
    import l3vpn_traffic

    # l3vpn_traffic is a module
    assert isinstance(l3vpn_traffic, types.ModuleType)
    # True

    # TestScript is created with the module as input:
    from pyats.aetest.script import TestScript
    testscript = TestScript(module = l3vpn_traffic)

This class and its object instance during execution is not normally directly
accessible by the user (unless through :ref:`reserved_parameters`). However, it
is still important for users to know about this class, as its instances enables
testscripts to have an overall result, where :ref:`script_args` are stored as
``TestScript`` parameters, and is where all major script section's ``parent``
attribute points to (eg, ``Testcase.parent``).

.. code-block:: text

    +--------------------------------------------------------------------------+
    | TestScript (base cls: TestItem)                                          |
    +==========================================================================+
    | attribute       | description                                            |
    |-----------------+--------------------------------------------------------|
    | module          | testscript module object                               |
    | source          | full path/name of the testscript file                  |
    +==========================================================================+
    | properties      | description                                            |
    |-----------------+--------------------------------------------------------|
    | uid             | name of the testscript                                 |
    | description     | testscript header (module docstring)                   |
    | result          | rolled-up result of entire testscript                  |
    | parameters      | dictionary of parameters relative to this testscript   |
    +--------------------------------------------------------------------------+


Container Classes
-----------------

``CommonSetup``, ``Testcase`` and ``CommonCleanup`` are the 3 different
container classes in ``aetest``. They are called container classes because they
"house" other test sections, and all inherit from the base ``TestContainer``.

.. code-block:: text

    +--------------------------------------------------------------------------+
    | CommonSetup, CommonCleanup, Testcase (base cls: TestContainer)           |
    +==========================================================================+
    | attribute       | description                                            |
    |-----------------+--------------------------------------------------------|
    | source          | file/line information where the class was defined      |
    +==========================================================================+
    | properties      | description                                            |
    |-----------------+--------------------------------------------------------|
    | uid             | common_setup/common_cleanup, or uid of Testcase        |
    | description     | class header (docstring)                               |
    | parent          | TestScript object                                      |
    | result          | rolled-up result of this section                       |
    | parameters      | dictionary of parameters relative to this section      |
    +--------------------------------------------------------------------------+

Container classes are seen directly in the user script: they are inherited
directly within testscripts to define their corresponding sections.

.. code-block:: python

    # Example
    # -------
    #
    #   defining container classes

    from pyats import aetest

    # inheriting CommonSetup
    # contains subsections
    class MyCommonSetup(aetest.CommonSetup):
        '''
        this is the description for CommonSetup
        '''

        @aetest.subsection
        def subsection_one(self):
            self.a = 1
            print('hello world')

        @aetest.subsection
        def subsection_two(self):
            assert self.a == 1

    # inheriting Testcase
    # contains setup/test/cleanup
    class MyTestcase(aetest.Testcase):
        '''
        this is the description for Testcase
        '''

        @aetest.test
        def test_one(self):
            print('inside testcase: %s' % self.uid)


Container classes instances are `iterables`_. Iterating through them yields each
of its enclosed sections. This could be useful during iterative script
development and testing.

.. code-block:: python

    # Example
    # -------
    #
    #   looping on container class instances

    from pyats import aetest

    # define a container & some inhabitants
    class MyCommonSetup(aetest.CommonSetup):
        @aetest.subsection
        def subsection_one(self):
            self.a = 1
            print('hello world')

        @aetest.subsection
        def subsection_two(self):
            assert self.a == 1

    # let's instantiate the class
    common_setup = MyCommonSetup()

    # loop through to see what we get:
    for i in common_setup:
        print(i)
    # subsection_one
    # subsection_two

Container class instances are `callable`_. Calling a container class
instance effectively runs it, and the result object is returned.

.. code-block:: python

    # Example
    # -------
    #
    #   calling container class instance

    # continuing from last example..

    # run the common setup section instance
    # save into result variable
    result = common_setup()
    # hello world

    # print the result variable
    print(result)
    # passed

.. _iterables: https://docs.python.org/3.4/glossary.html#term-iterable
.. _callable: https://docs.python.org/3.4/library/functions.html#callable

.. _aetest_function_classes:

Function Classes
----------------

``Subsection``, ``SetupSection``, ``TestSection`` and ``CleanupSection`` classes
are function classes: they carry out a specific test function, and inherits
from the base ``TestFunction`` class.

Function classes and their object instances during execution is not normally
directly accessible by the user (unless through :ref:`reserved_parameters`).
However, they are still important because they correspond directly to ``aetest``
decorators. Their object instances are short-lived: they are created internally
during runtime, right before the execution of the section it represents, and
only lives until the end of that test section.

.. code-block:: text

    +--------------------------------------------------------------------------+
    | Subsection, [Setup|Test|Cleanup]Section (base cls: TestFunction)         |
    +==========================================================================+
    | attribute       | description                                            |
    |-----------------+--------------------------------------------------------|
    | function        | function/method that was decorated to be this section  |
    | source          | file/line information where the method was defined     |
    +==========================================================================+
    | properties      | description                                            |
    |-----------------+--------------------------------------------------------|
    | uid             | name of the function/method                            |
    | description     | function header (docstring)                            |
    | parent          | container (CommonSetup/Testcase/CommonCleanup)         |
    | result          | rolled-up result of this test function                 |
    | parameters      | dictionary of parameters relative to this function     |
    +--------------------------------------------------------------------------+

Internally, when any class method is decorated with ``aetest`` section
decorators, they are instantiated into their corresponding function class. This
allow the infrastructure to open & close each section's reporting context,
enables result tracking, and a multitude of of other feature sets specific to
test section methods.

.. code-block:: python

    # Example
    # -------
    #
    #  peeking into function class internals

    from pyats import aetest


    class MyCommonSetup(aetest.CommonSetup):
        # subsection corresponds to Subsection cls
        @aetest.subsection
        def subsection_one(self):
            pass

    class MyTestcase(aetest.Testcase):

        # setup corresponds to SetupSection cls
        @aetest.setup
        def setup(self):
            pass

        # test corresponds to TestSection cls
        @aetest.test
        def test_one(self):
            pass

        # cleanup corresponds to CleanupSection cls
        @aetest.cleanup
        def cleanup(self):
            pass

    # when container instances are iterated,
    # the returned objects are function class instances
    tc = MyTestcase()
    for obj in tc:
        print(type(obj))
        print(obj.function)
    # <class 'pyats.aetest.sections.SetupSection'>
    # <bound method MyTestcase.setup of <class 'MyTestcase' uid='MyTestcase'>>
    # <class 'pyats.aetest.sections.TestSection'>
    # <bound method MyTestcase.test_one of <class 'MyTestcase' uid='MyTestcase'>>
    # <class 'pyats.aetest.sections.CleanupSection'>
    # <bound method MyTestcase.cleanup of <class 'MyTestcase' uid='MyTestcase'>>

--------------------------------------------------------------------------------

Base Classes
------------

The following are a description of internal, base classes within ``aetest``.
You are not required to know any of these for normal script development. They
are here for power-user references only.


TestItem Class
^^^^^^^^^^^^^^

``TestItem`` is the base class of all other classes within ``aetest``: all other
classes inherit from it, thus establishing the basic properties of all
``aetest`` object/classes:

    - objects must have ``uid`` and ``description``

    - objects may have a ``parent``: the container where this object is housed
      in

    - objects must have ``result``

    - objects have ``parameters``: a dictionary of key-value pairs that
      affects the behavior of testing. This includes parameters that are
      specific to this ``TestItem``, and all of its parent's parameters.


.. code-block:: text

    +--------------------------------------------------------------------------+
    | TestItem Objects                                                         |
    +==========================================================================+
    | properties      | description                                            |
    |-----------------+--------------------------------------------------------|
    | uid             | item unique id string, cannot contain spaces           |
    | description     | item descriptive text                                  |
    | parent          | parent object where this object is contained in        |
    | result          | item test result object                                |
    | parameters      | dictionary of parameters related to this TestItem,     |
    |                 | a summation of parameters specific to itself, and all  |
    |                 | of its parent's parameters                             |
    +--------------------------------------------------------------------------+


TestContainer Class
^^^^^^^^^^^^^^^^^^^

``TestContainer`` class extends the base ``TestItem`` and serves as a base class
to all testscript's major sections such as ``Testcase``. The only technical
difference between ``TestContainer`` and ``TestItem`` is at the implementation
level:

- ``TestContainer`` may contain other ``TestItem``
- iterating a ``TestContainer`` instance yields its child ``TestItem``
- executing a ``TestContainer`` executes all child ``TestItem``.

All other model behavior should be the exact same.
