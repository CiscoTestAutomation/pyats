.. _generic_find:

Find
====

Are you looking for a specific object with specific values in a list that
consists of thousands of items? Don't worry ``find`` API of ``pyATS`` is here to
help you to find your objects and even filter them depending on the given
requirements.

Once upon a time, ``find`` API of ``Genie`` package was doing its job happily,
finding some topology objects such as devices, interfaces and links with its
wrapper friends. But one day, it recieved a message: "Follow the white rabbit",
so trouble knocked on its door, action had to be taken and the red pill was
swallowed.

This new helper function is now way more powerful and generic. It doesn't need
the wrapper functions around it and therefore it's not only limited to topology
objects but also requires more accurate input parameters. Users can search any
kind of object in an iterable and filter the results as they want by providing
search requirements.

Let's see some examples that are using the topology objects just like Genie Find
API.

.. code-block:: text

    # Example Topology
    iol-one---------------------iol-two--------------------iol-three
                    n1                          n2

.. code-block:: python

    >>> from pyats.utils.objects import find
    >>> find(from_ = testbed.devices.values(), type_ = Device)
    [<Device iol-one at 0xf6a7008c>, <Device iol-three at 0xf6a05b4c>, <Device iol-two at 0xf6a708cc>]

.. note::

    In the example above the minimum information was given and there wasn't any
    specific requirements provided, so, find API just returned all the device
    objects as it was asked within the given iterable which is the devices list
    of the testbed object.

Parameters
----------

    - **from_:** Users need to provide an iterable so that the API goes through
      and picks up the objects that match the conditions.

    - ***requirements:** Sets of requirements that are grouped with R object

    - **type_:** It is optional that users can provide an object type that
      they are specifically looking for, in order to distinguish the required
      objects from the others. Otherwise all kind of objects that match the
      condition will be returned.

    - ****kwargs:** This parameter is used to provide requirements.

    - **filter_:** It is optional that users can filter on matching result. If
      True: Will return the particular matching object. If False: Will return
      the actual value which is matching. By default it's set to True.

    - **index:** It is optional that users can filter on which of the
      dictionary value to return. Can only be used with `filter_=False`. By
      default it's set to last element.

    - **all_keys:** It is optional that users can filter on matching result.
      If True: Will return all the particular matching objects with path to
      objects that matches to particular requirement. If False: Will return the
      particular matching objects with path to objects which is matching. Can
      only be used with `filter_=False`. By default it's set to False.

Some more examples on how to use these parameters with different arguments.

.. code-block:: python

    from pyats.utils.objects import find

    class Human():
        def __init__(self, name):
            self.name = name

            if self.name == "Morpheus":
                self.alive = False
            else:
                self.alive = True

            if self.name == "Neo":
                self.dict = {"bla": "hebele"}
            else:
                self.dict = {"bla": "hubele"}

        @property
        def friend(self):
            if self.name == "Neo":
                return Human("Friend1")
            else:
                return Human("Friend2")

    class The_One(Human):
        pass

    class Not_The_One(Human):
        pass

    class Rebels():
        def __init__(self):
            self.members = [The_One("Neo"), Not_The_One("Trinity"), Not_The_One("Morpheus")]

        def callable_func(self, *args):
            return True

    rebels = Rebels()

Here we just created a Rebels object that contains a list of Humans objects as
its members. So let's see how can we use the ``find`` API with different
arguments. Here are some simple find calls:

.. code-block:: python

    # let's provide the basic arguments and see all the members
    >>> find(from_ = rebels.members, type_ = Human)
    [<__main__.The_One object at 0xf75b67ac>, <__main__.Not_The_One object at 0xf75b680c>,
     <__main__.Not_The_One object at 0xf75b67ec>]

    # find the members that are also instance of The_One class, also realize
    # that from_ is a positional argument
    >>> find(rebels.members, type_ =The_One)
    [<__main__.The_One object at 0xf75b67ac>]

    # basic python data types
    >>> find(from_ = [{}, 1, 1.2, "string",{"key": "value"}, object()], type_ = dict)
    [{}, {'key': 'value'}]

    # No type_
    >>> find([1,2,3.1, "asdf", {"asdf":"asdf"}, [2,1], object()])
    [1, 2, 3.1, 'asdf', {'asdf': 'asdf'}, [2, 1], <object object at 0xf76eb518>]

All the examples above just finds the instance of a specific class in the given
iterable. But there is no requirements passed to the find API. Let's see the
examples of how to filter the results.

.. code-block:: python

    # Example of providing requirements, we will get a member but with a
    # specific name
    >>> members = find(rebels.members, type_ = Human, name = 'Morpheus')
    >>> len(members)
    1
    >>> members[0].name
    'Morpheus'

    # Dictionary example
    >>> find([{"bla": "bla"}, {}, {"bla": "bla"}, {}], type_ = dict, bla = "bla")
    [{'bla': 'bla'}, {'bla': 'bla'}]

.. note::

    If there is an object repeating multiple times in the iterable, results
    include that object only once. But keep that in mind, objects are
    distinguished by their object ids, so let's say if the iterable has two
    dictionaries with the same value, the results include both of them like
    in the example above. But if the iterable consists of the same dict object
    multiple times then that dictionary object is included only once in the
    results.

    .. code-block:: python

        # This example is to prove that same objects are not repeated in the result.
        >>> some_obj = object()
        >>> find([some_obj, some_obj, some_obj, some_obj], type_ = object)
        [<object object at 0xf76a3d30>]

        # Let's try the dictionaries again
        # But realize that there are 3 dictionaries in the list matching the
        # condition. some_dict twice and the inline defined dictionary. But the
        # result will include only the some_dict only once and then the inline
        # defined dictionary object.
        >>> some_dict = {"bla": "bla"}
        >>> find([some_dict, {}, some_dict, {"bla": "bla"}],
        ...      type_ = dict, bla = "bla")
        [{'bla': 'bla'}, {'bla': 'bla'}]

Find API supports pyATS logic objects, check the following examples:

.. code-block:: python

    # This call will return us the Human objects with the name of Trinity or Neo
    >>> from pyats.datastructures.logic import Or, Not, And
    >>> members = find(rebels.members, type_ = Human, name = Or("Trinity", "Neo"))
    [<__main__.Not_The_One object at 0xf75b680c>, <__main__.The_One object at 0xf75b67ac>,]

    # Get the object's that's name is different than Morpheus
    >> members = find(rebels.members, type_ = Human, name = Not("Morpheus"))
    [<__main__.Not_The_One object at 0xf75b680c>, <__main__.The_One object at 0xf75b67ac>,]


Callables are also supported, so that user can pass a callable to the find API
and depending on the result from the callable objects can be added to the
result. There are two different ways to use callables:

    - First one is using the ``callable_`` parameter which accepts a callable,
      and calls each object with it. If the callable returns ``True`` then the
      object will be included in the results, otherwise, it will be ignored. In
      this case, ``assert user_callable(user_object)`` is what happens on the
      background.

    - Instead of filtering via specific value, callable can be used. For
      example, if ``name = callable`` was provided to the find API, then each
      objects ``name`` attribute is passed to the user defined callable.
      ``assert user_callable(user_object.attr)`` is what happens on the
      background

.. code-block:: python

    # Here we created a callable
    >>> def call_me(obj):
    ...     try:
    ...         if obj['name']: "hebele":
    ...             return True
    ...         else:
    ...             return False
    ...     except:
    ...         return False

    # Passing the callable will return us the dictionaries only with the name
    # value as "hebele"
    >>> find(from_ = [{"name": "hebele"},
    ...               {"name": "hubele"}, 1, 2],
    ...      type_ = dict,
    ...      callable_ = call_me)
    [{"name": "hebele"}]

    >>> def call_me_value(value):
    ...     if value == "hebele":
    ...         return True
    ...     return False

    # Passing callable with an attribute name
    >>> find(from_ = [{"name": "hebele"},
    ...               {"name": "hubele"}, 1, 2],
    ...      type_ = dict,
    ...      name = call_me_value)
    [{"name": "hebele"}]

    >>> find(rebels.members, type_ = Human, callable_ = rebels.callable_func)
    [<__main__.The_One object at 0xf75b67ac>, <__main__.Not_The_One object at 0xf75b680c>,
     <__main__.Not_The_One object at 0xf75b67ec>]

.. note::

    If ``callable_`` key is used, objects are passed to the callable, so that
    meaningful structures can be created in the callables. In the first example
    above dictionary objects were passed to the callable and depending on "name"
    value result type were decided. Find API, passes the objects to the callable
    by itself.

.. note::

    If ``callable_`` is not used like in the second example above, the key that
    is used to provide the callable will be taken as an attribute of the object.
    The value of this attribute on each object is passed to the user defined
    callable.

Find calls can get pretty complicated especially if users want to reach multiple
levels of objects. But how can we have access to those objects? Check the
following example.

.. code-block:: python

    # Requirement is to get Human objects that has a friend who's name is
    # "Friend1"
    >>> members = find(rebels.members, type_ = Human, friend__name = "Friend1")
    [<__main__.The_One object at 0xf75ce32c>]
    # Realize that only Neo has a friend with the name "Friend1"
    >>> members[0].name
    'Neo'

    # let's find the objects that has a dictionary called dict, and inside that
    # dictionary has a "bla" key with the value of "hubele"
    # in this example Not_The_One class objects are matching
    >>> members = find(rebels.members, type_ = Human, dict__bla = "hubele")
    [<__main__.Not_The_One object at 0xf75b680c>, <__main__.Not_The_One object at 0xf75b67ec>]]

    # let's use dictionaries with even more levels
    # Also, realize that "__" syntax was used in order to reach deeper levels.
    >>> find([{"bla": {"hebele": [{"hubele": "blabla"}, {}]}},
    ...       {"bla": {"hebele": [{"hubele": "mlamla"}, {}]}},
    ...       {}],
    ...      type_ = dict,
    ...      bla__hebele__hubele = "blabla")
    [{'bla': {'hebele': [{'hubele': 'blabla'}, {}]}}]

.. note::

    "__" syntax is recognized by the find API in order to reach deeper levels.
    Also it works with all kind of data types such as list, dictionary or
    objects.

.. note::

    "__" syntax also comes with its limitation. For example if a dictionary key
    or an object attribute name ends with "_" find API fails. This is because
    it always splits the keys from the first "_".

    .. code-block:: python

        >>> my_object1.child._attribute = "value"
        >>> my_object2.child.__attribute = "value"
        >>> my_object3.child_.attribute = "value"
        >>> my_object4.child_._attribute = "value"
        >>> my_object5.child_.__attribute = "value"
        >>> my_object6.child__.attribute = "value"
        >>> my_object7.child__._attribute = "value"
        >>> my_object8.child__.__attribute = "value"
        >>> iterable = [my_object1, my_object2, my_object3, my_object4,
        ...             my_object5, my_object6, my_object7, my_object8]

        # This call is looking for child.attribute = "value"
        >>> find(from_ = iterable, child__attribute = "value")
        []

        # This call is looking for child._attribute = "value" which is pushing
        # the limits of find API and is not recommended
        >>> find(from_ = iterable, child___attribute = "value")
        [my_object1]

    The object names around the "__" syntax shouldn't start or end with "_".

.. note::

    Avoid using objects which have "_" at the beginning or end of their names,
    around the special "__" syntax of find API. R objects can be used in order
    to get rid of this limitation. Please keep reading

There is another way of providing these requirements and the reason for that
will be explained later in the documentation. There is an R object in the same
place with the find API that users can import in order to organize their sets
of requirements.

.. code-block:: python

    >>> from pyats.utils.objects import R
    # Requirements with R object, an object with name "Trinity" and alive
    >>> members = find(rebels.members, R(name = 'Trinity', alive = True), type_ = Human)
    >>> len(members)
    1
    >>> members[0].name
    'Trinity'

The reason that R object was created is to combine multiple find requests at
once and get their intersection.

.. code-block:: python

    # Requirements with multiple R objects.
    # Looking for members who is alive in one set of requirements
    # Looking for members whose friends name is "Friend2" in the second set
    # Have no requirements in the third set so all the objects
    # intersection of these lists will be empty
    >>> members = find(rebels.members,
    ...                R(alive = True),
    ...                R(friend__name = "Friend2"),
    ...                R(),
    ...                type_ = Human)
    # First set of requirements R(alive = True), should return Neo and Trinity
    # Second set of requirements R(friend__name = "Friend2"), shoud return
    # Morpheus and Trinity
    # Third set of requirements R(), should return Neo, Trinity and Morpheus
    # so that the intersection of these three lists will give us only Trinity
    >>> len(members)
    1
    >>> members[0].name
    'Trinity'

.. note::

    When R object is used to group requirements, kwargs parameters are ignored.
    Therefore, following call will not work as expected,

    >>> find(my_iterable,
             R(name = "name"),
             type_ = my_obj,
             number = 2)

    This returns only the objects that's name is "name" and ignore the number.
    Here is the correct way of using find in this situation:

    >>> find(my_iterable,
             R(name = "name"), R(number = 2),
             type_ = my_obj,)

.. note::

    Use only R objects or only kwargs, they don't work together. If both are
    provided at the same time, kwargs is ignored.

.. important::

    R objects are also using the kwargs structure of the objects but they also
    support args. Which let's users to provide lists as their requirements.
    Please check the following example

.. code-block:: python

    >>> find([object1, object2, object3], R(["child_", "name", "my_child"], ["number", 1]))
    [object1]

.. important::

    In the example above, R object recieved 2 sets of requirements as lists.

    First one is ["child\_", "name", "my_child"] which
    means, object's ``child_`` attribute's ``name`` attribute is equal to
    ``my_child``

    Second requirement is ["number", 1] means object's ``number`` attribute is
    equal to 1.

    Basically, last element of the list is taken as the value that is expected,
    against the attribute which is accessible through the other keys in the list

    >>> object1.child_.name
    "my_child"

    >>> object1.number
    1

    As explained above, users can get rid of "__" syntax limitation if they use
    R objects with args by providing their requirements in a list.

.. note::

    Multiple type_s can be provided as a list to the find API. This returns
    the objects which are instances of the classes that were provided in
    the list of type_s.

    .. code-block:: python

        >>> find(from_ = [1, 2, 1.2, "1.2", {"1": "2"}, [2,1]])
        [1, 2, 1.2, '1.2', {'1': '2'}, [2, 1]]

        >>> find(from_ = [1, 2, 1.2, "1.2", {"1": "2"}, [2,1]], type_ = dict)
        [{'1': '2'}]

        >>> find(from_ = [1, 2, 1.2, "1.2", {"1": "2"}, [2,1]], type_ = [dict, list])
        [{'1': '2'}, [2, 1]]

.. note::

    Multiple R objects can be provided the find API with `filter_=False`. This
    returns the matching objects which are logical And results of all the
    requirements.

    .. code-block:: python

        >>> bgp = Bgp()
        >>> find(bgp, R(['info', 'instance', '(.*)', 'vrf', '(.*)',
        ...     'neighbor', '(.*)', 'remote_as', '(.*)']), R(['info', 'instance',
        ...     '(.*)', 'vrf', '(.*)','neighbor', '(.*)', 'session_state',
        ...     'Established']), filter_=False)
        [('100', ['info', 'instance', 'default', 'vrf', 'default', 'neighbor',
        '2.2.2.2', 'remote_as'])]


    Multiple R objects can be provided the find API with `filter_=False` and
    `index`. This returns the desired dictionary value of the matching result.

    .. code-block:: python

        >>> some_dict = {"bla": {'second':5, 'third':5}, 'orange':5,
        ...              'blue':{'aa':5}}
        >>> find(some_dict, R(['bla', 'second', 5]), filter_=False, index=2)
        [(5, ['bla', 'second'])]
        >>> find(some_dict, R(['bla', 'second', 5]), filter_=False, index=1)
        [({'second': 5, 'third': 5}, ['bla', 'second'])]
        >>> find(some_dict, R(['bla', 'second', 5]), filter_=False, index=0)
        [({'orange': 5, 'blue': {'aa': 5}, 'bla': {'second': 5, 'third': 5}},
        ['bla', 'second'])]


    Multiple R objects can be provided the find API with `filter_=False` and
    `all_keys=True`. This returns the all matching values of the requirements.

    .. code-block:: python

        >>> bgp = Bgp()
        >>> find(bgp, R(['info', 'instance', '(.*)', 'vrf', '(.*)',
        ...     'neighbor', '(.*)', 'remote_as', '(.*)']), R(['info', 'instance',
        ...     '(.*)', 'vrf', '(.*)', 'neighbor', '(.*)', 'shutdown', True]
        ...     ), R(['info', 'instance','(.*)', 'vrf', '(.*)', 'neighbor',
        ...     '(.*)', 'session_state', '(.*)']), filter_=False, all_keys=True)
        [[('200', ['info', 'instance', 'default', 'vrf', 'default', 'neighbor',
        '2.2.2.5', 'remote_as']), (True, ['info', 'instance', 'default', 'vrf',
        'default', 'neighbor', '2.2.2.5','shutdown']), ('Shut (Admin)', ['info',
        'instance', 'default', 'vrf','default', 'neighbor', '2.2.2.5',
        'session_state'])]]

.. note::

    R object also accepts Find Operator such as Not and Contains. This returns
    the desired value of the matching result.

    .. code-block:: python

        >>> some_dict = {'a':5, 'b':7, 'c':{'ca':8, 'bc':[1,2,3,4,5,6,7,20]}}
        >>> find(some_dict, R(['c', Not('bc'),'(.*)']),filter_=False)
        [(8, ['c', 'ca'])]
        >>> find(some_dict, R(['c', Contains('c'),Contains(20)]),filter_=False)
        [([1, 2, 3, 4, 5, 6, 7, 20], ['c', 'bc'])]
        >>> find(some_dict, R(['c', Contains('c'),Not(Contains(20))]),
        ...      filter_=False)
        [(8, ['c', 'ca'])]
