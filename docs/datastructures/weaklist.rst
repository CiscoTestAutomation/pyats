Weak List References
====================

A standard ``list`` object stores every internal object as a direct reference.
That is, if the ``list`` exists, then its internally stored objects exist.

A ``WeakList`` instance is the exact same as a python ``list``, except that it
only stores weak references (using ``weakref.ref()``) of the objects. All access
(add/delete/comparison/slicing) is still the same as native ``list``, done with 
the actual objects. This gives it a specific behavior where if an object it
references is no longer alive (eg, cleaned up by ``gc``), it is cleaned up and
removed from the ``WeakList``.

.. code-block:: python

    # Example
    # -------
    #
    #   WeakList use case

    from pyats.datastructures import WeakList

    # create a class for demo (base object cannot be weakref'ed)
    class NewObject(object): 
        pass

    # create a couple instances
    a = NewObject()
    b = NewObject()
    c = NewObject()

    # create a list and its weaklist
    l = [a, b, c]
    # [<NewObject object at 0xf76d65ec>, 
    #  <NewObject object at 0xf76d664c>, 
    #  <NewObject object at 0xf76d654c>]

    wl = WeakList(l)
    # WeakList([<NewObject object at 0xf76d65ec>, 
    #           <NewObject object at 0xf76d664c>, 
    #           <NewObject object at 0xf76d654c>])

    # comparison between a weaklist and a list is the exact same
    l == wl
    # True

    # access also yields the same, normal objects
    wl[0]
    # <NewObject object at 0xf76d65ec>
    wc[0] is l[0]
    # True

    # removing the actual objects (ref counter = 0) 
    # removes the object from weaklist
    # (deleting l as well so that no references to a exists)
    del a
    del l

    # note now that wl only has 2 items left (b and c)
    wl 
    # WeakList([<NewObject object at 0xf76d664c>, 
    #           <NewObject object at 0xf76d654c>])

.. tip::
    
    this can be extremely useful when you need to build a list of something
    without incrementing its reference counters.

.. note::
    
    you can mimic this entire behavior by creating a list and add only weakref
    objects to it. This just eliminates that overhead.

Creation
--------

Create a ``WeakList`` the same way as creating your typical ``list`` objects by
providing the constructor any iterable.

.. code-block:: python

    # Example
    # -------
    #
    #   WeakList creation

    from pyats.datastructures import WeakList

    # assuming we had a list of objects called 'l'

    # create using another list
    wl = WeakList(l)

    # create using an iterable
    wl = WeakList(iter(l))

Access
------

All ``list`` usage patterns & APIs work also on ``WeakList``. From a usability
perspective, all access appears as if you are dealing with a standard ``list``
object, except that the internally stored references are weak references.

.. code-block:: python
    
    # Example
    # -------
    #
    #   WeakList access

    # assuming we had a list of objects called 'l'
    # create using another list
    wl = WeakList(l)

    # everything is the same
    wl[0] is l[0]
    # True

    wl == l
    # True

    wl[1:2] == l[1:2]
    # True

.. hint::

    essentially, the sole difference between a ``list`` and ``WeakList`` is how
    reference to objects are stored internally. There are no external apparent
    differences.

Limitations
-----------

The only requirement is that objects stored into a ``WeakList`` must be able to
have its weak reference objects created by ``weakref.ref()`` api. Eg, objects
such as ``str`` and ``int`` cannot have weak references, and thus cannot be
added to a ``WeakList``
