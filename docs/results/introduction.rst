Introduction
============

In most test infrastructures, such as `pytest`_ and `unittest`_, test results
are only available as ``pass``, ``fail`` or ``error``. This works quite well in
unit and simplistic testing. However, the downside of having only three
result types is the inability to describe testcase result relationships, or 
distinguish a test's genuine failure, versus a failure of the test script caused
by mal-design/mal-coding (e.g. the testcase encountered a coding Exception).

In order to accomodate complex test environments, pyATS supports more
complicated result types such as "test blocked", "test skipped", "test code
errored" etc, and uses objects and object relationships to describe them. These
objects simplify the whole result tracking & aggregation infrastructure, and
grant the ability to easily roll-up results together.

.. code-block:: python
    
    # Example
    # -------
    #
    #   pyATS result objects

    from pyats.results import Passed, Failed

    # rolling up passed + failed yields failed
    Passed + Failed
    # Failed


.. _pytest: http://pytest.org/latest/
.. _unittest: https://docs.python.org/3.4/library/unittest.html

