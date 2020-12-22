Result Objects
==============

.. warning::

    Results are no longer singletons. Any comparisons using ``is`` will no
    longer be valid.

``Passed``
    indicating that a test was successful, passing, result accepted... etc.

``Failed``
    indicating that a test was unsuccessful, fell short, result unacceptable...
    etc.

``Aborted``
    indicating something was started but was not finished, was incomplete and/or
    stopped at an early or premature stage. E.g. a script was killed by hitting
    CTRL-C.

``Blocked``
    used when a dependency was not met and the following event could not start.
    Note that a "dependency" doesn't strictly mean order dependency and set-up
    dependency. It could also mean cases where the next event to be carried out
    is no longer relevant.

``Skipped``
    used when a scheduled item was not executed and was omitted. The difference
    between skipped and blocked is that skipping is voluntary, whereas blocked
    is a collateral.

``Errored``
    a mistake or inaccuracy. E.g. an unexpected ``Exception``. The difference
    between failure and error is that failure represents carrying out an event
    as planned with the result not meeting expectation, whereas errored means
    something gone wrong in the course of carrying out that procedure.

``Passx``
    short for "passed with exception". Use with caution: you are effectively
    re-marking a failure to passed, even thought there was an exception.

.. note::

    ``pass`` is a reserved keyword in python, so we opted to standardize on
    capitalized past tense verbs to indicate results instead. Eg,
    ``pass -> Passed``, ``fail -> Failed``, etc.


Import & Usage
--------------

There are 7 base result objects with no associated data that can be imported
into your code to be used directly. As simple as:

.. code-block:: python

    # Example
    # -------
    #
    #   importing result objects

    # import each result object individually
    from pyats.results import (Passed, Failed, Aborted, Errored,
                               Skipped, Blocked, Passx)

    # or you can also import them altogether using * wildcard
    # the module has code that specifically limits this to be the same as
    # the localized import statement above
    from pyats.results import *

These base result objects can also be used to spawn unique result object with
associated data. For example:

.. code-block:: python

    # Example
    # -------
    #
    #   distinct result objects

    from pyats.results import Passed

    # we can make our own passed result from the base one. Both are "Passed",
    # but the new result now contains relevant information.
    mypassed = Passed.clone(reason = 'reason for passing',
                            data = {'numbers': [1,2,3,4,5]})

    mypassed == Passed # True
    mypassed is Passed # False
    mypassed.reason # 'reason for passing'
    Passed.reason # None



Object Attributes
-----------------

``TestResult`` objects have the following attributes:

code
    Integer equivalent of this result type

value
    The string equivalent of this result type

reason
    The reason for this result

data
    Any relevant data for this result


.. code-block:: python

    # Example
    # -------
    #
    #    using pyATS results objects

    # import all of them
    from pyats.results import Passed, Errored

    # getting the result equivalent code
    Passed.code
    # 1

    # or get the code by typecasting
    int(Passed)
    # 1

    # getting the resuilt name string
    Passed.value
    # passed

    # or typecast into str
    str(Passed)
    # passed

    # can have a reason for this particular result
    new_passed = Passed.clone(reason = 'the test was successful')
    new_passed.reason
    # the test was successful
