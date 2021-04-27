Introduction
============

.. sidebar:: Quick References

    - `unittest`_
    - `pytest`_

AEtest (Automation Easy Testing) is the standard test engineering automation
harness. It offers a simple and straight-forward way for users to
define, execute and debug testcases and testscripts, serving as a basis for
other testscript templates & engines.

AEtest is available as a standard component (``aetest``) in pyATS in an effort
to standardize the definition and execution of testcases &
testscripts. Implemented fully in Python, pyATS ``aetest`` is designed to
leverage the full benefits of Python language's object-oriented capabilities.

.. code-block:: python

    # Example
    # -------
    #
    #   very simple aetest testscript

    from pyats import aetest
    from some_lib import configure_interface

    class CommonSetup(aetest.CommonSetup):
        @aetest.subsection
        def connect_to_device(self, testbed):
            # connect to testbed devices
            for device in testbed:
                device.connect()

    class SimpleTestcase(aetest.Testcase):
        @aetest.test
        def simple_test(self, testbed):
            # configure each device interface
            for device in testbed:
                for intf in device:
                    configure_interface(intf)

    class CommonCleanup(aetest.CommonCleanup):
        @aetest.subsection
        def disconnect_from_devices(self, testbed):
            # disconnect_all
            for device in testbed:
                device.disconnect()

    # for running as its own executable
    if __name__ == '__main__':
        aetest.main()


The architectural design of AEtest module drew inspiration from Python
`unittest`_, a native Python unit-testing infrastructure, and as well
`pytest`_, an open-source, community-supported Python testing tool. Those that
are familiar with the above should be able to quickly adopt AEtest with little
effort.

.. _unittest: https://docs.python.org/3.4/library/unittest.html
.. _pytest: http://pytest.org/latest/


High-Level Design Features
--------------------------
* straight-forward, pythonic user experience (object-oriented design)

* block-based approach to test section breakdowns

  * Common Setup with Subsections

  * Testcases with setup/tests/cleanup

  * Common Cleanup with Subsections

* highly modular and extensible

  * Testcase inheritance

  * dynamic testcase generation

  * custom runner for user defined testable objects

  * customizable reporter

* enhanced looping & testcase parametrization


AEtest: Core Concepts
---------------------

Main sections must be sub-divided
    all sections must be further divided into smaller sections, such as Common
    Setup being sub-divided into subsections. This promotes for better code
    legibility and practice.

Sections must be explicitly declared
    importing another test script's sections have no effect, unless the
    imported sections were inherited in this script.

    .. code-block:: python

        # this only imports it for inheriting options.
        # does not run it
        from another_script import AnotherTestcase

        # this includes it into this script
        class LocalTestcase(AnotherTestcase):
            pass

Import, inspect & run
    each test script is imported into Python using the standard ``import``
    mechanism, and then inspected for test sections. Discovered test sections
    (classes) are instantiated and run. This mechanism is inline with how
    ``pytest`` & ``unittest`` loads and discovers testcases.

    Therefore, consider Classes and Functions within a test script as only
    *boundaries* or *blocks* that define testcases, and tests. Eg. user has no
    control over the test object creation/init and only uses class/def
    statements to define the start and end of testcases & etc.

Installation & Updates
----------------------

AEtest module ``aetest`` is installed by default as part of pyATS installation.
The package is also featured in the PyPI server, and can be installed
separately.

Note that ``aetest`` module is part of the ``pyats`` namespace, and therefore,
users should always refer to the full namespace when installing & using:

.. code-block:: bash

    pip install pyats.aetest

To upgrade an existing installation of AEtest package in your environment, do:

.. code-block:: bash

    pip install pyats.aetest --upgrade

.. note ::

    always read the :ref:`changelog` first before you upgrade.
