Runtime Behavior
================

.. sidebar:: Helpful Reading

    - `Classes Remarks`_

    - `Weak References`_

.. _Classes Remarks: https://docs.python.org/3.4/tutorial/classes.html#random-remarks
.. _Weak References: https://docs.python.org/3/library/weakref.html

This section covers native runtime behaviors of your testscript. It is an
addendum to the :ref:`object_model` chapter, focusing on the behavior of class 
instances, and how to benefit the most from the object model relationships.

The word **runtime**, in this context, refers to the behavior and/or objects 
available when ``aetest`` scripts are executed via one of the two official ways
described in :ref:`running_aetest_script`. 


.. _aetest_runtime:

runtime
-------

``aetest.runtime`` object provides users access to runtime and ``aetest`` input
argument information that are normally not accessible via script test objects. 
To access, import ``runtime`` as a module, and simply query runtime information
via object attributes.

.. code-block:: python
    
    # Example
    # -------
    #
    #   querying runtime information inside testscripts

    from pyats import aetest

    class CommonSetup(aetest.CommonSetup):

        # this common setup subsection validates 
        # uids and groups input arguments default to empty
        @subsection
        def validate_skip_uids(self):
            assert not aetest.runtime.uids
            assert not aetest.runtime.groups

The following variables are currently accessible through ``runtime``:

    - ``uids``: current script execution :ref:`aetest_uids` configuration

    - ``groups``: current script :ref:`aetest_groups` configuration

In time, we'll expand this access list as needed.

.. important::

    ``runtime`` is the only official way to query runtime environment info in
    ``aetest``. There are other inconspicuous methods, but they are unsupported
    and may go away and/or be changed as part of internal refactorings.


.. _self_behavior:

self
----

Within container classes such as ``CommonSetup``, ``Testcase`` and 
``CommonCleanup``, ``self`` refers to the instance of that class, and remains
consistent throughout the execution of that container. 

.. code-block:: python

    # Example
    # -------
    #
    #   self, consistency explained

    from pyats import aetest

    # define a testcase where its tests
    # expects self.value to be set by the setup section,
    # and continues to be carried throughout
    class Testcase(aetest.Testcase):
        @aetest.setup
        def setup(self):
            self.value = 1

        @aetest.test
        def test_one(self):
            self.value += 1
            assert self.value == 2

        @aetest.test
        def test_one(self):
            self.value += 1
            assert self.value == 3

    # run the Testcase
    tc = Testcase()
    print(tc())
    # passed

As demonstrated in the above example, ``self.value``, initially created within
the ``setup`` section, was carried throughout the testcase, and each ``test``
was able to add to it and check that the expected values are consistent.

.. important::
    
    in other words, each container class is only instantiated once, and every
    section (method) within it shares the same instance object, and can 
    influence each other's behaviors. 

This enables linear relationships within container classes, where users can 
carry objects & values around by setting & getting attributes on instance object
``self``, and where the next section's behavior can be influenced by a previous
section's values and result.

.. note::
    
    this behavior is drastically different vs. python ``unittest`` and
    ``pytest``, where each test method (starting with ``test_``) has its own
    class instance, and is independent of all other test methods.

.. note::

    ``self`` is not a keyword in Python. It is merely a `convention`_ where the
    first argument to a method is always named ``self`` for readability & 
    consistency. This section intends to focus on the class instance object 
    that it represents, and thus, for the sake of consistency and simplicity,
    we are just referring to it as ``self``.

.. _convention: https://docs.python.org/3.4/tutorial/classes.html#random-remarks


.. _parent: 

parent
------

``aetest`` testscripts follow a tree-style parent-child object relationship. The
following provides a graphical view.

.. code-block:: text

                                +--------------+
                                |  TestScript  |
                                +-------+------+
                                        |
           +----------------------------+---------------------------+
           |                            |                           |
    +------+------+            +--------+-------+           +-------+-------+ 
    | CommonSetup |            |   Testcases    |           | CommonCleanup |
    +------+------+            +--------+-------+           +-------+-------+
           |                            |                           |
    +------+------+                     |                    +------+------+
    | subsections |          +----------+-----------+        | subsections | 
    +-------------+          |          |           |        +-------------+     
                         +---+---+  +---+---+  +----+----+
                         | setup |  | tests |  | cleanup |
                         +-------+  +-------+  +---------+
                                               
                                   
This relationship can be observed and accessed during runtime via the object
``parent`` attribute:

    - in ``CommonSetup``, ``Testcase`` and ``CommonCleanup``, ``self.parent``
      refers to the ``TestScript`` instance.

    - in each test method (subsection/setup/tests/cleanup), its parent is 
      naturally accessed with ``self`` (the method parent instance). This is
      a trivial Python behavior.

    - subsection/setup/test/cleanup section's internal corresponding 
      ``Subsection``, ``SetupSection``, ``TestSection`` and ``CleanupSection``
      class objects also has ``parent`` attribute, pointing to their 
      container. This is an FYI - these objects are normally not referenced by
      the user.

    - ``TestScript`` instance's ``parent`` is ``None``, because it is the root
      of all other objects.

.. code-block:: python

    # Example
    # -------
    #
    #   parenthood is not easy
    #
    #   note that the same relationships described below
    #   also applies to CommonSetup & CommonCleanup

    import sys
    from pyats import aetest

    class Testcase(aetest.Testcase):
        @aetest.setup
        def setup(self):
            # within a method (subsection/setup/test/cleanup)
            # self refers to its parent. (trivial)
            assert isinstance(self, aetest.Testcase)

        @aetest.test
        def test(self):
            # within a method (subsection/setup/test/cleanup)
            # self.parent refers to the Testcase parent
            # note that Object Models: TestScript.module refers to this module
            # so let's test this.
            assert self.parent.module is sys.modules[__name__]


In order to avoid circular references, ``parent`` is internally implemented as
`Weak References`_, but returns the actual object to the end user when accessed. 

.. note::

    ``parent`` defaults to ``None`` when ``aetest`` objects are instantiated
    outside of the runtime environment. For example, during
    :ref:`testbench` scenarios. 

.. _aetest_section_ordering:

Section Ordering
----------------

``aetest`` script content runs in a logical, reproducible order. This ensures
that repeated runs of the same scripts in the same environment yields the same
execution order, a property much needed in feature testing.

The following rules are applied when the top-level ``TestContainer`` classes
are discovered and run:

    - ``CommonSetup`` section always runs first

    - ``Testcase`` runs in order as they are defined/appear in the script

    - ``CommonCleanup`` section always runs last

Within each ``TestContainer``, the following rules applies to child sections
(methods):

    - ``setup`` section always runs first (if applicable)

    - ``subsection`` and ``test`` order is slightly more complicated:

      - section methods defined in parent classes (through inheritance) are
        run first (parents first)

      - otherwise, run in the order as they are defined/appear in the script

    - ``cleanup`` section always runs last (if applicable)

.. code-block:: python

    Example
    # -------
    #
    #   section ordering example

    from pyats import aetest
    
    # assume that we are importing another testcase from a base_script
    # and inheriting it to create a new, extended testcase
    from base_script import BaseTestcase

    # pretend that the BaseTase looks like this
    # class BaseTestcase(self):
    #
    #     @aetest.test
    #     def test_one(self):
    #         print('i am test 1')
    #
    #     @aetest.test
    #     def test_two(self):
    #         print('i am test 2')

    # the local testcase inherits it
    class LocalTestcase(BaseTestcase):

        @aetest.test
        def test_three(self):
            print('i am test 3')

    # when this local test is run,
    # the two tests from parent class runs first.
    tc = LocalTestcase()
    print(tc())
    # i am test 1
    # i am test 2
    # i am test 3

These rules enables the "what you see is what you get" behavior, where the order
of script sections ran is the same as the order they appear in the testscript,
except for special conditions such as inheritances and setup/cleanup sections.

This is important because each ``test`` section could potentially be dependent
on a previous one, due to the specific behavior of :ref:`self_behavior`.

.. note:: 

    this behavior is drastically different vs. python ``unittest`` and
    ``pytest``, where the infrastructure does not attempt to sort run-order at
    all, and leaves them in whatever order they were discovered.
    
