.. _aetest_looping:

Looping Sections
================

.. sidebar:: Helpful Reading

    - `Classes Tutorial`_
    - `Decorators`_
    - `Scopes and Namespaces`_
    - `Iterator Types`_
    - `Yield Expressions`_
    - `Factory Design`_

.. _Decorators: https://wiki.python.org/moin/PythonDecorators
.. _Classes Tutorial: https://docs.python.org/3.4/tutorial/classes.html
.. _Scopes and Namespaces: https://docs.python.org/3.4/tutorial/classes.html#python-scopes-and-namespaces
.. _Iterator Types: https://docs.python.org/3.4/library/stdtypes.html#typeiter
.. _Yield Expressions: https://docs.python.org/3.4/reference/expressions.html#yieldexpr
.. _Factory Design: http://en.wikipedia.org/wiki/Factory_%28object-oriented_programming%29

    *What are loops? Refer to the end of this section.*

As an integral extension of the :ref:`test_parameters` data-driven testing concept, 
``aetest`` also supports section looping. Section looping means reusing a section's code body by providing
it with different parameters during each loop iteration. 

The following describes each section and their loop capability and behaviors:

``CommonSetup``/``CommonCleanup``
    Common setup and cleanup sections are unique within each test script. They
    are run only once per test script execution, and are not loopable.

    ``subsection``
        Subsections within ``CommonSetup`` and ``CommonCleanup`` are loopable.
        When a ``subsection`` is marked for looping, each iteration is 
        reported as a new subsection.

``Testcase``
    Testcases are loopable. Each iteration of a looping ``Testcase`` is reported 
    individually as new test case instances with a different ``uid``. When a 
    ``Testcase`` is looped, and all of its contents (setup, tests, and cleanup) are
    run fully per each iteration.

    ``setup``/``cleanup``
        Setup and cleanup sections within each test case is unique, and are run
        only once per ``Testcase``. They cannot be looped individually, but
        if their parent ``Testcase`` is looped, then they are run once per
        ``Testcase`` iteration.

    ``test``
        Test sections within ``Testcase`` are loopable individually. Each
        iteration has its own unique id and is reported as a new test 
        section. When a looping ``test`` section's parent ``Testcase`` is 
        looped, the resulting loops are multiplicative. E.g.: if a test case is 
        looped ``2x``and contains a test that is also looped ``2x``, that 
        test would loop ``2x`` per test case loop iteration.

.. hint::

    In other words, ``subsection``, ``Testcase`` and ``test`` sections are the
    only loopable sections.

Defining Loops
--------------

Sections are marked for looping when decorated with ``@loop``, and its
looping parameters are provided as decorator arguments. During runtime, when 
``aetest`` infrastructure detects looped section code, their corresponding 
section object is then instantiated once for each iteration.

.. code-block:: python

    # Example
    # -------
    #
    #   Defining loops on sections

    from pyats import aetest

    # Defining a common setup section
    # The CommonSetup section contains a 
    # subsection that is looped twice.
    class CommonSetup(aetest.CommonSetup):

        # Defining a subsection
        # ------------------------
        # This subsection is marked to be looped twice.
        # The first time having a uid of "subsection_one", and 
        # the second time having a uid of "subsection_two"
        @aetest.loop(uids=['subsection_one', 'subsection_two'])
        @aetest.subsection
        def looped_subsection(self):
            pass

    # Defining a test case that loops
    # ----------------------------------
    # This test case also contains a test section that is looped twice
    @aetest.loop(uids=['testcase_one', 'testcase_two'])
    class Testcase(aetest.Testcase):

        # Setup section of this test case is run once
        # every time the test case is looped.
        @aetest.setup
        def setup(self):
            pass

        # Looped test section
        # both iterations are run per test case iteration
        @aetest.loop(uids=['test_one', 'test_two'])
        @aetest.test
        def test(self):
            pass

        # Cleanup section of this test case is run once
        # every time the test case is looped.
        @aetest.cleanup
        def cleanup(self):
            pass

    # This test script's resulting sections would look like this below
    #
    # SECTIONS/TESTCASES                                             RESULT   
    # ----------------------------------------------------------------------
    #  .
    #  |-- CommonSetup                                               PASSED
    #  |   |-- subsection_one                                        PASSED
    #  |   `-- subsection_two                                        PASSED
    #  |-- testcase_one                                              PASSED
    #  |   |-- setup                                                 PASSED
    #  |   |-- test_one                                              PASSED
    #  |   |-- test_two                                              PASSED
    #  |   `-- cleanup                                               PASSED
    #  `-- testcase_two                                              PASSED
    #      |-- setup                                                 PASSED
    #      |-- test_one                                              PASSED
    #      |-- test_two                                              PASSED
    #      `-- cleanup                                               PASSED

As shown above, the minimum requirement to loop a section (e.g., to run its code 
1+ times) is to decorate the section with ``@loop``and provide a list of loop 
iteration uids using the ``uids`` argument. This controls the number of iterations
this section is looped: Each unique item in the ``uids`` list generates
a new section with that uid.

When the ``@loop`` decorator is used on a ``@subsection`` or ``@test``, the section method
is effectively decorated twice, and even though the order does not matter, it 
make more sense to use ``@loop`` as the outermost decorator, signifying that
this method is first marked as a section; then this section is looped.

.. tip::

    Decorators are executed from "innermost" to "outermost."

Additionally, to make the script more aesthetically pleasing, 
``aetest`` also features a shortcut to avoid the double decorators: 
``@subsection.loop`` and ``@test.loop``.

.. code-block:: python
    
    # Example
    # -------
    #
    #   Demonstrating the double decorator shortcut for tests and subsections

    from pyats import aetest

    class CommonSetup(aetest.CommonSetup):

        # Marking this as both a subsection and being looped
        @aetest.subsection.loop(uids=['subsection_one', 'subsection_two'])
        def looped_subsection(self):
            pass

    class Testcase(aetest.Testcase):

        # Marking this as both a test section and being looped
        @aetest.test.loop(uids =['test_one', 'test_two'])
        def test(self):
            pass

.. note::

    ``@subsection.loop`` and ``@test.loop`` are convenience features. They are
    not a python decorator compression technique. ``.loop`` is an attribute to 
    ``subsection``/``test`` that are implemented in ``aetest``. It is 
    effectively a new decorator that shoots two birds with one stone.

.. tip::

    Python ``@decorators`` are evaluated at import time. Thus, decorator
    arguments may only be static. If you need to reference runtime and
    dynamic information information as part of your loop declaration, e.g.,  
    accessing parameters, etc., refer to :ref:`dynamic_looping`.

Loop Parameters
---------------

Looping the same section, again and again, is not very useful. Even if each
section has a unique uid, as demonstrated above, the usefulness of a test
that repeatedly performs the same actions is questionable. This is where **loop
parameters** comes in.

The loop parameters feature allows each loop iteration to receive new, distinct
:ref:`test_parameters`. These parameters are specified as part of the ``@loop``
decorator, processed and propagated to each section instance as their 
*local parameters*. Combined with the :ref:`parameters_as_funcargs` feature, each
looped section is then driven to potentially do something different.

.. code-block:: python
    
    # Example
    # -------
    #
    #   Loop parameters demonstration

    from pyats import aetest

    # Loop this test case with a loop parameter named "a"
    # and set it to value 2 for the first iteration, 
    # and 3 for the second iteration
    @aetest.loop(a=[2, 3])
    class Testcase(aetest.Testcase):

        # Loop this test with a loop parameter named "b"
        # and set it to 8 for the first iteration and 9 for the second.
        @aetest.test.loop(b=[8, 9])
        def test(self, a, b):
            # this test prints the exponential of two inputs, a and b
            print("%s ^ %s = %s" % (a, b, a**b))

    # The output of the test case would look like this:
    #   2 ^ 8 = 256
    #   2 ^ 9 = 512
    #   3 ^ 8 = 6561
    #   3 ^ 9 = 19683
    #
    # and since no uids were provided as part of the loop decorator, new uids
    # are generated based on the original section name and the input parameters
    #
    #  SECTIONS/TESTCASES                                               RESULT   
    # --------------------------------------------------------------------------
    #  .
    #  |-- Testcase[a=2]                                                PASSED
    #  |   |-- test[b=8]                                                PASSED
    #  |   `-- test[b=9]                                                PASSED
    #  `-- Testcase[a=3]                                                PASSED
    #      |-- test[b=8]                                                PASSED
    #      `-- test[b=9]                                                PASSED

In effect, loop parameters allow users to create and modify the looped
section's local parameters on the fly per iteration. It is an extension of the
dynamic parameter concept, where section parameters are generated and fed
to each section during runtime. 

The use of loop parameters also makes the ``uids`` argument optional: If the ``uids`` arguments
are not provided, the infrastructure generates unique section uids by combining
the original section name with each of its current loop parameters as postfix 
in square brackets. Otherwise, the provided ``uids`` are used as section uids.

There are two methods of providing loop parameters to the ``@loop`` decorator:

    - By providing a list of parameters, and a list of parameter values for
      each iteration (eg, using ``args`` and ``argvs``)

    - By providing each parameter as a keyword argument, and a list of its
      corresponding argument values. (eg, ``a=[1, 2, 3], b=[4, 5, 6]``)

.. code-block:: python

    # Example
    # -------
    #
    #   Providing loop parameters

    from pyats import aetest

    class Testcase(aetest.Testcase):

        # Loop this test with arguments "a", "b", and "c".
        # Provide all of its iteration arguments together using method one.
        # The positions of each value in argvs correspond to its args name.
        @aetest.test.loop(args=('a', 'b', 'c'), 
                          argvs=((1, 2, 3),
                                 (4, 5, 6)))
        def test_one(self, a, b, c):
            print("a=%s, b=%s, c=%s" % (a, b, c))

        # Loop this test with the same arguments as above, but
        # provide each of its iteration arguments independently using method two
        @aetest.test.loop(a=(1,4),
                          b=(2,5),
                          c=(3,6))
        def test_two(self, a, b, c):
            print("a=%s, b=%s, c=%s" % (a, b, c))

    
    # Testcase output:
    #   a=1, b=2, c=3
    #   a=4, b=5, c=6
    #   a=1, b=2, c=3
    #   a=4, b=5, c=6
    #
    #  SECTIONS/TESTCASES                                               RESULT   
    # --------------------------------------------------------------------------
    #  .
    #  `-- Testcase                                                     PASSED
    #      |-- test_one[a=1,b=2,c=3]                                    PASSED
    #      |-- test_one[a=4,b=5,c=6]                                    PASSED
    #      |-- test_two[a=1,b=2,c=3]                                    PASSED
    #      `-- test_two[a=4,b=5,c=6]                                    PASSED

As shown above, there were no differences in the outcome of the results. The only
difference was how the loop parameters were provided. One method may be superior
to the other depending on the use case, the number of arguments, etc. 

When using loop parameters, the following rules determine the actual number
of iterations:

    - If ``uids`` arguments were provided, the number of iterations is equal to the number
      of ``uids`` provided.

      - If the number of parameter values exceeds the number of ``uids``, all
        extra values are discarded.

    - If ``uids`` arguments are not provided, the number of iterations equals the 
      number of loop parameter values. Eg, if ``@loop(a=[1,2,3])``, then there 
      would be 3 loop instances, each taking on one distinct value: ``a=1``, 
      ``a=2``, ``a=3``.

      - If there are multiple parameters and the number of their values do not
        agree, or if the number of parameter values is less than the number of 
        provided ``uids``, a ``filler`` is used to fill empty spots. 
        ``filler`` defaults to ``None``, and only 1 filler can be provided.

.. code-block:: python

    # Example
    # -------
    #
    #   Loop parameter combinations
    #   (pseudo-code for demonstration only)

    from pyats.aetest import loop

    # Loop with 2 iterations using uids argument
    # ------------------------------------------
    #   iteration 1: uid='id_one'
    #   iteration 2: uid='id_two'
    @loop(uids=['id_one', 'id_two'])

    # Loop with 2 iterations using parameters argument
    # ------------------------------------------------
    #   iteration 1: a=1, b=4
    #   iteration 2: a=2, b=5
    @loop(a = [1, 2], b = [4, 5])
    # Same as above, using args and argvs
    @loop(args=['a', 'b'], argvs=[(1, 4), (2, 5)])

    # Loop with 2 iterations, and extra arguments are discarded due to uids
    # ---------------------------------------------------------------------
    #   iteration 1: uid='id_one', a=1, b=2
    #   iteration 2: uid='id_two', a=3, b=4
    # extra argument values 5/6 are discarded because there are no matching uids
    @loop(uids=['id_one', 'id_two'],
          args=['a', 'b'],
          argvs=[(1, 2),
                 (3, 4),
                 (5, 6)])
    # Same example as above but using per-parameter values
    @loop(uids=['id_one', 'id_two'],
          a=[1, 3, 5], b=[2, 4, 6])

    # Loop with 3 iterations, and their number of parameters values do not agree
    # --------------------------------------------------------------------------
    #   iteration 1: a=1, b=4
    #   iteration 2: a=2, b=5
    #   iteration 3: a=3, b=None ---> default filler comes in to fill the blanks
    @loop(a=[1, 2, 3], b=[4, 5])
    # Same as above, using args and argvs
    @loop(args=['a', 'b'],
          argvs=[(1, 4),
                 (2, 5),
                 (3, )])

    # Loop with more uids than parameters, and custom filler
    # ------------------------------------------------------
    #   iteration 1: uid='id_one', a=1, b=3
    #   iteration 2: uid='id_two', a=2, b=4
    #   iteration 1: uid='id_three', a=999, b=999  ---> custom filler
    @loop(uids = ['id_one', 'id_two', 'id_three'], 
          a = [1, 2], b = [3, 4], filler = 999)
    # same as above, using args and argvs
    @loop(uids=['id_one', 'id_two', 'id_three'], 
          args=['a', 'b'], argvs=[(1, 3), (2, 3)], filler=999)

Advanced Loop Usages
--------------------

Arguments to the ``@loop`` decorator may also be `callable`_, `iterable`_, or a
`generator`_. The infrastructure can distinguish and treat each as you
would normally expect it to:

    - If an argument value is a `callable`_, it is called, and its returns
      are then used as the actual loop argument value.

    - If an argument value is an `iterable`_ or a `generator`_, the loop engine
      picks only one element from it at a time to build the next iteration,
      until it is exhausted.

.. _callable: https://docs.python.org/3.4/library/functions.html#callable
.. _iterable: https://docs.python.org/3.4/glossary.html#term-iterable
.. _generator: https://docs.python.org/3.4/glossary.html#term-generator

.. code-block:: python

    # Example
    # -------
    #
    #   Demonstrating advanced loop parameter behaviors

    from pyats import aetest

    # Defining a function
    # Functions are callable
    def my_function():
        value = [1, 2, 3]
        print("returning %s" % value)
        return value

    # Defining a generator
    def my_generator():
        for i in [4, 5, 6]:
            print('generating %s' % i)
            yield i

    class Testcase(aetest.Testcase):

        # Creating test section with parameter "a" as a function
        # Note that the function object is passed, not its values
        @aetest.test.loop(a=my_function)
        def test_one(self, a):
            print("a = %s" % a)

        # Creating a test section with parameter "b" as a generator
        # Note that the generator is a result of calling my_generator(), not
        # the function itself.
        @aetest.test.loop(b=my_generator())
        def test_two(self, b):
            print('b = %s' % b)

    # The output of the test case would be:
    #   returning [1, 2, 3]
    #   a = 1
    #   a = 2
    #   a = 3
    #   generating 4
    #   b = 4
    #   generating 5
    #   b = 5
    #   generating 6
    #   b = 6

In the above example, pay close attention to the output lines:
    
    - Callable arguments are called and converted into their return values
      before their looped sections are created and run. 

    - Iterators and generators are only queried before the next section needs to
      be created.

This behavior enables using a custom generator as input values to your loop
parameters. For example, a generator state machine that queries the current
testbed device status and creates iterations based on that information. Since 
the generator is not polled until right before the next iteration, your custom 
function is only run in-between test sections, thus dynamically generating the
loop iterations based on current test environments.

.. _dynamic_looping:

Dynamic Loop Marking
--------------------

So far, all loop examples focus on defining the ``@loop`` decorator directly within the 
test scripts. E.g., the ``@loop`` decorators are coded as part of the test script. 
However, it is also possible to dynamically mark sections for looping during
runtime, e.g., creating loops based on information that is only available during
a script’s run. To do this, use the ``loop.mark()`` function.

.. code-block:: python
    
    # Example
    # -------
    #
    #   Dynamically marking sections for looping

    from pyats import aetest

    class Testcase(aetest.Testcase):

        @aetest.setup
        def setup(self):
            # Mark the next test for looping
            # Provide it with two unique test uids.
            # (self.simple_test is the next test method)
            aetest.loop.mark(self.simple_test, uids=['test_one', 'test_two'])

        # Note: the simple_test section is not directly marked for looping
        # instead, during runtime, its testcase's setup section marks it for
        # looping dynamically.

        @aetest.test
        def simple_test(self, section):
            # Print the current section uid
            # by using the internal parameter "section"
            print("current section: %s" % section.uid)

    # Output of this test case
    #   current section: test_one
    #   current section: test_two
    #
    #  SECTIONS/TESTCASES                                                RESULT   
    # --------------------------------------------------------------------------
    #  .
    #  `-- Testcase                                                      PASSED
    #      |-- setup                                                     PASSED
    #      |-- test_one                                                  PASSED
    #      `-- test_two                                                  PASSED

``loop.mark()`` arguments and behaviors (including loop parameters, etc.) are 
exactly identical to its sibling, the ``@loop`` decorator, with the only exception 
that its first input argument must be the target section method/class. E.g.: 
``loop.mark(Testcase_Two, a=[1,2,3])``.

The benefit of this approach is simple: Dynamic information, parameters and
variables such as :ref:`script_args`, :ref:`parent` etc., are only available 
during runtime. This information and its corresponding variables are not
available when the script is written, and delaying variable references (while
using the ``@loop`` decorator) in Python is very difficult, if not impossible.

--------------------------------------------------------------------------------

Loop Internals
--------------

.. sidebar:: Confucius Say...

    The information here onwards is for users interested in ``aetest``
    internals & extensions only. 

    **If you are new to this, do not read on. These advanced topics may
    further fuel your confusion.**

The previous sections focused on the "how to use" aspect of ``aetest`` looping
functionality. From here onwards, we'll dig deeper into loop internals, look at 
how it functions, and how to deviate from its default behaviors.

The ``aetest`` looping behavior and how its arguments are processed are 
highly customizable. This was not highlighted in previous sections for the sake
of serializing the training & simplifying the learning curve.

In reality, consider the ``@loop`` decorator and ``loop.mark()`` function as only
markers: They only mark the given section for looping. The details (parameters)
Each iteration is generated from **loop generators**, where all 
arguments to ``@loop`` and ``loop.mark()``propagate to. E.g.:

.. code-block:: python

    # Example
    # -------
    #
    #   Pseudo-code demonstrating @loop decorator functionality

    # What the loop decorator definition sort of looks like
    # Note where the generator defaults to "DefaultLooper"
    def loop(generator=DefaultLooper, *args, **kwargs):

        # The actual loop generator gets called with all of the arguments
        # to loop decorator, and generates each section iteration
        return generator(*args, **kwargs)

    # Pseudo-code here onwards, demonstrating internals
    # -------------------------------------------------
    #   
    # During runtime, the looped is expanded to create each iteration

    for iteration in loop(*args, **kwargs):
        # Create a section from iteration information and run it
        # ...

        #E.g., instantiate Subsection
        subsection = Subsection(uid=iteration.uid, 
                                parameters=iteration.parameters)
        
        # and add to common setup's subsections list
        common_setup.subsections.append(subsection)

        # etc.

Behind the scenes, **loop generators** are the actual classes that do the
heavy lifting: Creating each iteration based on the ``@loop`` and ``loop.mark()``
decorator arguments. Loop generators are `iterable`_. Each of its returned
members is an instance of the ``Iteration`` class, containing the uid & parameters 
information unique to this loop and used by the infrastructure to create the 
next section instance.

.. csv-table:: Iteration class (collections.namedtuple)
    :header: "Attribute", "Description"
    :widths: 30, 70
    :stub-columns: 1

    ``uid``, iteration uid
    ``parameters``, "a dictionary of :ref:`test_parameters` to be applied to
    the next looped section"

In other words, **loop generator** is the object that ultimately controls how
loops are generated and what parameters each iteration is associated with. The
looping behavior and arguments described in the topics above are that of 
``DefaultLooper``, the default **loop generator** provided by ``aetest`` loop
infrastructure. Its features are sufficient for most use cases. However, if you
wish to customize loop behavior, it is possible to extend and override it.

.. code-block:: python

    # Example
    # -------
    #
    #   Demonstrating how to write and pass your own loop generator
    
    # Loop generators must return Iterations
    from pyats import aetest
    from pyats.aetest.loop import Iteration

    # Let's write a custom loop generator
    # It generates integers between a and b as loop iterations
    # and pass the integer as the "number" parameter of the executed section.
    # Each iteration uid is named "iteration_uid" + number
    class DemoGenerator(object):

        # At a minimum, the loop generator needs to accept an argument called
        # "loopee", which is the actual object being looped. This allows the
        # loop generator to know what it is looping on and build information
        # based on it.
        # In this example, we're ignoring that argument, as our loop generator
        # is straightforward.
        def __init__(self, loopee, a, b):
            self.numbers = list(range(a, b))

        def __iter__(self):
            for i in self.numbers:
                # Each generated member is an instance of Iteration
                # Each Iteration must have a unique id
                # and all of its parameters stored in a dictionary
                yield Iteration(uid='iteration_uid_%s' % i,
                                parameters={'number': i})

    
    # This loop generator can be used as the @loop and loop.mark() argument.
    # Let's define a looped test case with it.

    # Looping this test case with a custom generator, and a=1, b=5
    @aetest.loop(generator=DemoGenerator, a=1, b=5)
    class Testcase(aetest.Testcase):

        # Since our generator generates a parameter named "number"
        # Let's print it in this simple test.
        @aetest.test
        def test(self, number):
            print('current number: %s' % number)

    # Output of this test case
    #   current number: 1
    #   current number: 2
    #   current number: 3
    #   current number: 4
    #
    #  SECTIONS/TESTCASES                                                RESULT   
    # --------------------------------------------------------------------------
    #  .
    #  |-- iteration_uid_1                                               PASSED
    #  |   `-- test                                                      PASSED
    #  |-- iteration_uid_2                                               PASSED
    #  |   `-- test                                                      PASSED
    #  |-- iteration_uid_3                                               PASSED
    #  |   `-- test                                                      PASSED
    #  `-- iteration_uid_4                                               PASSED
    #      `-- test                                                      PASSED

.. hint::
    
    The above examples may be simple, but the demonstrated underlying principles 
    are not.
    
    *"Do not try and bend the spoon. That's impossible. Instead... only try to
    realize the truth..."*

And voila. Custom **loop generators** like the above are immensely powerful: By 
extending and overriding the default loop generation behavior, and defining
custom test sections entirely driven by parameter inputs, users can effectively
overload the loop functionality into a dynamic generator of highly abstracted
test executor. 

--------------------------------------------------------------------------------

    *Looking for loop definition? Refer to the top of this section.*
