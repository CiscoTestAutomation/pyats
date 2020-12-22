.. _logic_tests:

Logic Testing
=============

.. sidebar:: Helpful Reading

    - `Boolean Algebra`_
    - `Regular Expressions`_

.. _Boolean Algebra: http://en.wikipedia.org/wiki/Boolean_algebra
.. _Regular Expressions: https://docs.python.org/3.4/library/re.html

`Boolean Algebra`_ is sometimes confusing when used in the context of 
English language. The goal of this module is to standardize on how to represent
and evaluate logical expressions within the scope of pyATS, and as well offer
standard APIs, classes and behaviors for users leverage.

.. csv-table:: Boolean Operators Offered in This Module
    :header: Name, Class, Description
    :widths: 20, 20, 60

    **Conjunction**, ``And``, "logical *And*: true if and only if 
    all operands are true"
    **Disjunction**, ``Or``, "logical *Or*: true if at least one of its
    operands is true"
    **Negation**, ``Not``, "logical *Not*: true only if all operands are false"

Logical operators offered in this ``logic`` module accepts two types of inputs,
and subsequently, has different behaviors depending on the input expressions.

``callable`` inputs
    when instantiated with callable input expressions, arguments supplied
    to the evaluation of the logic instance is fed directly to these callables. 
    The return values are then used as part of truth testing.

``str`` inputs
    when instantiated with strings, they are treated as regular expressions and
    compiled into python ``re`` regex objects. During evaluation, these regex
    objects are used to ``search`` the input argument (casted into strings) to
    determine whether matches are found. 

This will become clearer with examples from the following class usage and
behavior descriptions.

.. code-block:: python

    # Example
    # -------
    #
    #   operator using callables

    from pyats.datastructures.logic import And, Not, Or

    # creating some functions to be used for operation testing
    def is_int(value):
        # tests if value is a number
        return isinstance(value, int)

    def is_str(value):
        # tests if value is a string
        return isinstance(value, str)

    def greater_than_10(value):
        # tests if value is greater than 10
        return value > 10

    # create some operations using the function callables
    int_greater_than_10 = And(is_int, greater_than_10)
    int_or_str = Or(is_int, is_str)
    not_int = Not(is_int)

    # do some testing
    # ---------------
    
    # 1 is an integer, but less than 10
    int_greater_than_10(1)
    False

    # 999 is an integer and also greater than 10
    int_greater_than_10(999)
    True

    # "1" is str, not int.
    # note that the logic is built-around quick evaluations: if the first
    # expression is not True, the logic aborts and returns immediately.
    int_greater_than_10("1")
    False

    int_or_str("1")
    True

    not_int("1")
    True


Logical operator classes are instantiated with one or more expressions 
(``callable`` in the above examples), which are then evaluated individually 
against input values. The result of each expression is then used for the final
boolean logic testing.

In addition, if ``str`` type expressions are used, the logic operator classes
automatically compile them into regular expressions to be used to search whether
the input is string or not:

.. code-block:: python

    # Example
    # -------
    #
    #   operators using strings and regexes

    from pyats.datastructures.logic import And, Not, Or

    # regular expressions matching to a string that contains
    # both "sanity" and "traffic"
    sanity_and_traffic = And('.*sanity.*', '.*traffic.*')

    # regular expression matching to either "bgp" or "ospf"
    # note that this is the same as regex: "bgp|ospf"
    bgp_or_ospf = Or('bgp', 'ospf')

    # regular expressions that end with "regression"
    # note this is the same as regex lookahead: "(?!regression$)"
    not_regression = Not('regression$')

    # do some testing
    # ---------------
    sanity_and_traffic('bgp_sanity_traffic_testing')
    True

    bgp_or_ospf('bgp_traffic')
    True

    not_regression('l2vpn_regression')
    False

If a list input is provided during evaluation of the operator instance, the 
test is considered *true* as long as at least one of those input items satisfies
each logical expression:

.. code-block:: python

    # Example
    # -------
    #
    #   operators and list inputs

    from pyats.datastructures.logic import And, Not, Or

    test_expr = And(lambda x: bool(x), lambda y: isinstance(y, int))
    test_not_expr = Not("^bgp.*", "sanity$")

    # do some testing
    # ---------------
    test_expr(0, 1)
    True

    test_expr(0, None)
    False

    test_not_expr("bgp_sanity", "routing_regression")
    False

    test_not_expr("ospf_regression", "routing_regression")
    True

    # consider this as logical OR between the input lists for truth testing:
    # test_expr(0, None) is interpretered as:
    # test_expr(0) or test_expr(None)
    #
    # note that in the case of Not(), this is a logical AND
    # test_not_expr(0, 1) is the same as:
    # test_not_expr(0) and test_not_expr(1)

In summary:

.. code-block:: python
    
    And(*expressions):

        expression_1(inputs) and expression_2(inputs)  and ...

    Or(*expressions):

        expression_1(inputs) or expression_2(inputs) or ...

    Not(*expressions):
        
        not expression_1(inputs) and not expression_2(inputs) and not ...


.. _logic_from_str:

Logic String Inputs
-------------------

``logic`` module allows the convertion of string-format logic expressions into
objects. This allows command-line arguments to propagate into logical objects
for further evaluation.

.. code-block:: python

    # Example
    # -------
    #
    #   string to logic objects

    from pyats.datastructures.logic import logic_str

    # creating an And regex logic from string
    obj = logic_str("And('a', 'b')")

    type(obj)
    # <class 'pyats.datastructures.logic.And'>

    obj('ab')
    True

    obj('cd')
    False

In essence, the input string needs to be formatted the same as python code, with
proper string quotes & etc. It is then evaluated by the ``logic_str`` to be 
converted into python object expression.

.. note::

    ``logic_str`` conversion only supports ``str`` (regex) style inputs and
    lambda functions. 