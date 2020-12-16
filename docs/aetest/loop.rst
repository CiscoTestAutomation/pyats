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

As an integral extension of :ref:`test_parameters` data-driven testing concept, 
``aetest`` also supports section looping: reusing section code body by providing
it with different parameters during each loop iteration. 

The following describes each section and their loop capability and behaviors:

``CommonSetup``/``CommonCleanup``
    Common setup and cleanup sections are unique within each testscript. They
    are run only once per testscript execution, and are not loopable.

    ``subsection``
        Subsections within ``CommonSetup`` and ``CommonCleanup`` are loopable.
        When a ``subsection`` is marked for looping, each of its iterations is 
        reported as a new subsection.

``Testcase``
    Testcases are loopable. Each iteration of a looping ``Testcase`` is reported 
    individually as new testcase instances with different ``uid``. When a 
    ``Testcase`` is looped, all of its contents (setup, tests and cleanup) are
    run fully per each iteration.

    ``setup``/``cleanup``
        Setup and cleanup sections within each testcase is unique, and are run
        only once per ``Testcase``. They cannot be looped individually, but
        if their parent ``Testcase`` is looped, then they are run once per
        ``Testcase`` iteration.

    ``test``
        Test sections within ``Testcase`` are loopable individually. Each
        iteration has its own unique id, and is reported as a new test 
        section. When a looping ``test`` section's parent ``Testcase`` is also 
        looped, the resulting loops are multiplicative. Eg: if a testcase is 
        looped ``2x``, and contains a test that is also looped ``2x``, that 
        test would loop ``2x`` per testcase loop iteration.

.. hint::

    in other words, ``subsection``, ``Testcase`` and ``test`` sections are the
    only loopable sections.


Defining Loops
--------------

Sections are marked for looping when they are decorated with ``@loop``, and its
looping parameters provided as decorator arguments. During runtime, when 
``aetest`` infrastructure detects looped section code, their corresponding 
section object is then instantiated once for each of its iterations.

.. code-block:: python

    # Example
    # -------
    #
    #   defining loops on sections

    from pyats import aetest

    # defining a common setup section
    # contains a subsection that is looped twice.
    class CommonSetup(aetest.CommonSetup):

        # defining a subsection
        # this subsection is marked to be looped twice
        # the first time having a uid of "subsection_one", and 
        # the second time having a uid of "subsection_two"
        @aetest.loop(uids=['subsection_one', 'subsection_two'])
        @aetest.subsection
        def looped_subsection(self):
            pass

    # defining a testcase that loops
    # this testcase also contains a test section that is looped twice
    @aetest.loop(uids=['testcase_one', 'testcase_two'])
    class Testcase(aetest.Testcase):

        # setup section of this testcase is run once
        # every time the testcase is looped.
        @aetest.setup
        def setup(self):
            pass

        # looped test section
        # both iterations are run per testcase iteration
        @aetest.loop(uids=['test_one', 'test_two'])
        @aetest.test
        def test(self):
            pass

        # cleanup section of this testcase is run once
        # every time the testcase is looped.
        @aetest.cleanup
        def cleanup(self):
            pass

    # this testscript's resulting sections would look like this below
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

As shown above, the minimum requirement to loop a section (eg, to run its code 
1+ times) is to decorate the section with ``@loop``, and provide a list of loop 
iteration uids using ``uids`` argument. This controls the number of iterations
this section is looped: each unique item in the ``uids`` list generates to
a new section with that uid.

When ``@loop`` is used on a ``@subsection`` or ``@test``, the section method
is effectively decorated twice, and even though the order does not matter, it 
make more sense to use ``@loop`` as the outermost decorator, signifying that
this method is first marked as a section, then this section is looped.

.. tip::

    decorators are executed in the order of "innermost" to "outermost".

In addition, in an effort to make the script more aesthetically pleasing, 
``aetest`` also features a shortcut to avoid the double decorators: 
``@subsection.loop`` and ``@test.loop``.

.. code-block:: python
    
    # Example
    # -------
    #
    #   demonstration the double decorator shortcut for test and subsections

    from pyats import aetest

    class CommonSetup(aetest.CommonSetup):

        # marking this as both a subsection, and being looped
        @aetest.subsection.loop(uids=['subsection_one', 'subsection_two'])
        def looped_subsection(self):
            pass

    class Testcase(aetest.Testcase):

        # marking this as both a test section and being looped
        @aetest.test.loop(uids =['test_one', 'test_two'])
        def test(self):
            pass

.. note::

    ``@subsection.loop`` and ``@test.loop`` are convenience features. They are
    not a python decorator compression technique. ``.loop`` is an attribute to 
    ``subsection``/``test`` that are implemented in ``aetest``. It is 
    effectively a new decorator that shoots two birds with one stone.

.. tip::

    python ``@decorators`` are evaluated at import time. Thus, decorator
    arguments may only be static. If you need to reference runtime and/or
    dynamic information information as part of your loop declaration, eg,  
    accessing parameters & etc, refer to :ref:`dynamic_looping`.


Loop Parameters
---------------

Looping the same section again and again is not very useful. Even if each
section has a unique uid as demonstrated above, the usefulness of a test
that repeatedly perform the same actions is questionable. This is where **loop
parameters** comes in.

Loop parameters feature allows each loop iteration to receive new, distinct
:ref:`test_parameters`. These parameters are specified as part of the ``@loop``
decorator, processed and propagated to each section instance as their 
*local parameters*. Combined with :ref:`parameters_as_funcargs` feature, each
looped section is then driven to potentially do something different.

.. code-block:: python
    
    # Example
    # -------
    #
    #   loop parameters demonstration

    from pyats import aetest

    # loop this testcast with a loop parameter named "a"
    # and set it to value 2 for the first iteration, 
    # and 3 for the second iteration
    @aetest.loop(a=[2, 3])
    class Testcase(aetest.Testcase):

        # loop this test with loop parameter named "b"
        # and set it to 8 for the first iteration, 9 for the second.
        @aetest.test.loop(b=[8, 9])
        def test(self, a, b):
            # this test prints the exponential of two inputs, a and b
            print("%s ^ %s = %s" % (a, b, a**b))


    # the output of the testcase would look like this:
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

In effect, loop parameters allows users to create and/or modify the looped
section's local parameters on the fly, per iteration. It is an extension of the
dynamic parameter concept, where section parameters are being generated and fed
to each section during runtime. 

The use of loop parameters also makes ``uids`` argument optional: if ``uids``
are not provided, the infrastructure generates unique section uids by combining
the original section name with each of its current loop parameters as postfix 
in square backets. Otherwise, the provided ``uids`` are used as section uids.

There are two methods of providing loop parameters to the ``@loop`` decorator:

    - by providing a list of parameters, and a list of parameter values for
      each iteration (eg, using ``args`` and ``argvs``)

    - by providing each parameter as a keyword argument, and a list of its
      corresponding argument values. (eg, ``a=[1, 2, 3], b=[4, 5, 6]``)

.. code-block:: python

    # Example
    # -------
    #
    #   providing loop parameters

    from pyats import aetest

    class Testcase(aetest.Testcase):

        # loop this test with arguments "a", "b", and "c"
        # provide all of its iteration arguments together using method one
        # the positions of each value in argvs corresponds to its args name
        @aetest.test.loop(args=('a', 'b', 'c'), 
                          argvs=((1, 2, 3),
                                 (4, 5, 6)))
        def test_one(self, a, b, c):
            print("a=%s, b=%s, c=%s" % (a, b, c))

        # loop this test with the same arguments as above, but
        # provide each of its iteration arguments independently using method two
        @aetest.test.loop(a=(1,4),
                          b=(2,5),
                          c=(3,6))
        def test_two(self, a, b, c):
            print("a=%s, b=%s, c=%s" % (a, b, c))

    
    # testcase output:
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

As shown above, there were no difference in the outcome of the results. The only
difference was how the loop parameters were provided. One method may be superior
to the other depending on the situation, the number of arguments, etc. 

When using loop parameters, the following rules determines the actual number
of iterations:

    - if ``uids`` were provided, the number of iterations is equal to the number
      of ``uids`` provided.

      - if the number of parameter values exceeds the number of ``uids``, all
        extra values are discarded.

    - if ``uids`` are not provided, the number of iterations is equal to the 
      number of loop parameter values. Eg, if ``@loop(a=[1,2,3])``, then there 
      would be 3 loop instances, each taking on one distinct value: ``a=1``, 
      ``a=2``, ``a=3``.

      - if there are multiple parameters and the number of their values do not
        agree, or if the number of parameter values is less than the number of 
        provided ``uids``, a ``filler`` is used to fill empty spots. 
        ``filler`` defaults to ``None``, and only 1 filler can be provided.

.. code-block:: python

    # Example
    # -------
    #
    #   loop parameter combinations
    #   (pseudo code for demonstration only)

    from pyats.aetest import loop

    # loop with 2 iterations using uids argument
    # ------------------------------------------
    #   iteration 1: uid='id_one'
    #   iteration 2: uid='id_two'
    @loop(uids=['id_one', 'id_two'])

    # loop with 2 iterations using parameters argument
    # ------------------------------------------------
    #   iteration 1: a=1, b=4
    #   iteration 2: a=2, b=5
    @loop(a = [1, 2], b = [4, 5])
    # same as above, using args and argvs
    @loop(args=['a', 'b'], argvs=[(1, 4), (2, 5)])

    # loop with 2 iterations, and extra arguments are discarded due to uids
    # ---------------------------------------------------------------------
    #   iteration 1: uid='id_one', a=1, b=2
    #   iteration 2: uid='id_two', a=3, b=4
    # extra argument values 5/6 are discarded because there are no matching uids
    @loop(uids=['id_one', 'id_two'],
          args=['a', 'b'],
          argvs=[(1, 2),
                 (3, 4),
                 (5, 6)])
    # same example as above but using per-parameter values
    @loop(uids=['id_one', 'id_two'],
          a=[1, 3, 5], b=[2, 4, 6])

    # loop with 3 iterations, and their number of parameters values do not agree
    # --------------------------------------------------------------------------
    #   iteration 1: a=1, b=4
    #   iteration 2: a=2, b=5
    #   iteration 3: a=3, b=None ---> default filler comes in to fill the blanks
    @loop(a=[1, 2, 3], b=[4, 5])
    # same as above, using args and argvs
    @loop(args=['a', 'b'],
          argvs=[(1, 4),
                 (2, 5),
                 (3, )])

    # loop with more uids than parameters, and custom filler
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
`generator`_. The infrastructure is able to distinguish and treat each as you
would normally expect it to:

    - if an argument value is a `callable`_, it is called, and its returns
      are then used as the actual loop argument value.

    - if an argument value is an `iterable`_ or a `generator`_, the loop engine
      picks only one element from it at a time to build the next iteration,
      until it is exhausted.

.. _callable: https://docs.python.org/3.4/library/functions.html#callable
.. _iterable: https://docs.python.org/3.4/glossary.html#term-iterable
.. _generator: https://docs.python.org/3.4/glossary.html#term-generator

.. code-block:: python

    # Example
    # -------
    #
    #   demonstrating advanced loop parameter behaviors

    from pyats import aetest

    # defining a function
    # functions are callable
    def my_function():
        value = [1, 2, 3]
        print("returning %s" % value)
        return value

    # defining a generator
    def my_generator():
        for i in [4, 5, 6]:
            print('generating %s' % i)
            yield i

    class Testcase(aetest.Testcase):

        # creating test section with parameter "a" as a function
        # note that the function object is passed, not its values
        @aetest.test.loop(a=my_function)
        def test_one(self, a):
            print("a = %s" % a)

        # creating a test section with parameter "b" as a generator
        # note that the generator is a result of calling my_generator(), not
        # the function itself.
        @aetest.test.loop(b=my_generator())
        def test_two(self, b):
            print('b = %s' % b)

    # the output of the testcase would be:
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

This behavior enables the use of custom generator as input values to your loop
parameters. For example, a generator state machine that queries the current
testbed device status and creates iterations based on that information. Since 
the generator is not polled until right before the next iteration, your custom 
function is only run in-between test sections, thus dynamically generating the
loop iterations based current test environments.


.. _dynamic_looping:

Dynamic Loop Marking
--------------------

So far, all loop examples focused on defining ``@loop`` directly within the 
testscripts. Eg, the ``@loop`` decorators are coded as part of the testscript. 
In addition, it is also possible to dynamically mark sections for looping during
runtime, eg, creating loops based on information that is only available during
a script run. To do this, use the ``loop.mark()`` function.

.. code-block:: python
    
    # Example
    # -------
    #
    #   dynamically marking sections for looping

    from pyats import aetest

    class Testcase(aetest.Testcase):

        @aetest.setup
        def setup(self):
            # mark the next test for looping
            # provide it with two unique test uids.
            # (self.simple_test is the next test method)
            aetest.loop.mark(self.simple_test, uids=['test_one', 'test_two'])

        # note: the simple_test section is not directly marked for looping
        # instead, during runtime, its testcase's setup section marks it for
        # looping dynamically.

        @aetest.test
        def simple_test(self, section):
            # print the current section uid
            # by using the internal parameter "section"
            print("current section: %s" % section.uid)


    # output of this testcase
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

``loop.mark()`` arguments & behaviors (including loop parameters & etc) are 
exactly identical to its sibling ``@loop`` decorator, with the only exception 
that its first input argument must be the target section method/class. Eg: 
``loop.mark(Testcase_Two, a=[1,2,3])``.

The benefit of this approach is simple: dynamic information, parameters and
variables such as :ref:`script_args`, :ref:`parent` etc, are only available 
during runtime. This information and its corresponding variables are not
available when the script is written, and delaying variable references (while
using ``@loop`` decorator) in Python is very difficult, if not impossible.

--------------------------------------------------------------------------------


Loop Internals
--------------

.. sidebar:: Confucius Say...

    The information here onwards is for users interested in ``aetest``
    internals & extensions only. 

    If you are new to this, do not read on. These advanced topics may
    further fuel your confusion.

The previous sections focused on the "how to use" aspect of ``aetest`` looping
functionality. From here onwards, we'll dig deeper into loop internals, look at 
how it functions, and how to deviate from its default behaviors.

The ``aetest`` looping behavior & how its arguments are processed is actually
highly customizable. This was not highlighted in previous sections for the sake
of serializing the training & simplifying the learning curve.

In reality, consider ``@loop`` decorator and ``loop.mark()`` function as only
markers: they only mark the given section for looping. The details (parameters)
of each iterations is actually generated from **loop generators**, where all 
arguments to ``@loop`` and ``loop.mark()`` propagates to. Eg:

.. code-block:: python

    # Example
    # -------
    #
    #   pseudo code demonstrating @loop decorator functionality

    # what the loop decorator definition sort-of looks like
    # note where the generator defaults to "DefaultLooper"
    def loop(generator=DefaultLooper, *args, **kwargs):

        # the actual loop generator gets called with all of the arguments
        # to loop decorator, and generates each section iteration
        return generator(*args, **kwargs)

    # pseudo code here onwards, demonstrating internals
    # -------------------------------------------------
    #   
    # during runtime, the looped is expanded to create each iteration

    for iteration in loop(*args, **kwargs):
        # create a section from iteration information and run it
        # ...

        # eg, instantiate Subsection
        subsection = Subsection(uid=iteration.uid, 
                                parameters=iteration.parameters)
        
        # and add to common setup's subsections list
        common_setup.subsections.append(subsection)

        # etc ...


Behind the scenes, **loop generators** are the actual classes that does the
heavy lifting: creating each iteration based on ``@loop`` and ``loop.mark()``
decorator arguments. Loop generators are `iterable`_. Each of its returned
member is an instance of  ``Iteration`` class, containing the uid & parameters 
information unique to this loop, and used by the infrastructure to create the 
next section instance.

.. csv-table:: Iteration class (collections.namedtuple)
    :header: "Attribute", "Description"
    :widths: 30, 70
    :stub-columns: 1

    ``uid``, iteration uid
    ``parameters``, "a dictionary of :ref:`test_parameters` to be applied to
    the next looped section"

In other words, **loop generator** is the object that ultimately controls how
loops are generated, and what parameters each iteration is associated with. The
looping behavior and arguments described in topics above are actually that of 
``DefaultLooper``, the default **loop generator** provided by ``aetest`` loop
infrastructure. Its features are sufficient for most use cases. However, if you
wish to customize loop behavior, it is possible to extend and/or override it.

.. code-block:: python

    # Example
    # -------
    #
    #   demonstrating how to write and pass your own loop generator
    
    # loop generators must return Iterations
    from pyats import aetest
    from pyats.aetest.loop import Iteration

    # let's write a custom loop generator
    # it generates integers between a and b as loop iterations
    # and pass the integer as "number" parameter of the executed section.
    # each iteration uid is named "iteration_uid" + number
    class DemoGenerator(object):

        # at minimum, the loop generator needs to accept an argument called
        # "loopee", which is the actual object being looped. This allows the
        # loop generator to know what it is looping on, and build information
        # based on it.
        # in this example, we're ignoring that argument, as our loop genrator
        # is simple and straightforward.
        def __init__(self, loopee, a, b):
            self.numbers = list(range(a, b))

        def __iter__(self):
            for i in self.numbers:
                # each generated member is an instance of Iteration
                # each Iteration must have a unique id
                # and all of its parameters stored in a dictionary
                yield Iteration(uid='iteration_uid_%s' % i,
                                parameters={'number': i})

    
    # this loop generator can be used as @loop and loop.mark() argument.
    # let's define a looped testcase with it.

    # looping this testcase with custom generator, and a=1, b=5
    @aetest.loop(generator=DemoGenerator, a=1, b=5)
    class Testcase(aetest.Testcase):

        # since our generator generates a parameter named "number"
        # let's print it in this simple test.
        @aetest.test
        def test(self, number):
            print('current number: %s' % number)

    # output of this testcase
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
    
    the above examples may be simple, the demonstrated underlying principles 
    are not.
    
    *"Do not try and bend the spoon. That's impossible. Instead... only try to
    realize the truth..."*

And voila. Custom **loop generators** like above is immensely powerful: by 
extending and/or overriding the default loop generation behavior, and defining
custom test sections entirely driven by parameter inputs, users can effectively
overload the loop functionality into a dynamic generator of highly abstracted
test executor. 

--------------------------------------------------------------------------------

    *Looking for loop definition? Refer to the top of this section.*
