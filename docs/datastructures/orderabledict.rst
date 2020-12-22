.. _orderabledict:

Orderable Dictionary
====================

Python's built-in ``collections.OrderedDict`` only remembers the order of which
keys were inserted into it, and does not allow users to re-order the keys and/or
insert new keys into arbitrary position in the current key order. 

``OrderableDict``, Orderable Dictionary, is almost exactly the same as python
``collections.OrderedDict`` with the added ability to order & re-order the keys
that are inserted into it.

.. code-block:: python

    # Example
    # -------
    #
    #   using OrderableDict

    from pyats.datastructures import OrderableDict

    # create a blank OrderableDict
    obj = OrderableDict()

    # all added keys are remembered in the order as they are added
    obj['A'] = 1
    obj['B'] = 2
    obj['C'] = 3
    # OrderableDict([('A', 1), ('B', 2), ('C', 3)])

    # use move() api to move an existing key to a new positions
    # eg, moving 'C' key and value to first position
    obj.move('C', 0)
    # OrderableDict([('C', 3), ('A', 1), ('B', 2)])

    # use insert() to insert new keys into arbitrary positions
    # eg, insert 'D' key into 2nd position
    obj.insert('D', 4, position = 1)
    # OrderableDict([('C', 3), ('D', 4), ('A', 1), ('B', 2)])


``OrderableDict`` behavior is normally exactly identical to those of python
``collections.OrderedDict``, except that it comes with two new APIs:

``move(key, position)``
    moves an existing key in the datastructure to just before ``position``.

``insert(key, value, position)``
    insert a new key/value pair into the datastructure just before ``position``.

When using ``OrderableDict``, the ``position`` argument refers to the 
corresponding index value of the list of all currently ordered keys. That is,
if you create a list from the ordered keys of the current datastrucuture, each
key's ``position`` is exactly its list index value.

Known Limitations
-----------------

The implementation of ``OrderableDict`` is not as efficient as ``dict`` and
``OrderedDict``. A separate list is used internally to store the current 
order of keys, and thus can lead to a larger memory footprint. This problem may
be further exacerbated if the keys are very large.