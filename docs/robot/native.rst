RobotFramework Keywords
=======================

The ``pyats.robot`` module also features RobotFramework keywords_, enabling
users to leverage pyATS features and scripts.

.. _keywords: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#creating-user-keywords

Features
--------

- run pyATS AEtest testcases and converting results to Robot

- loading/using pyATS testbed topology YAML files

- connect/interact with testbed devices dynamically

Keywords
--------

For the complete set of keywords supported by this package, refer to
`pyATS Keywords`_.

.. _pyATS Keywords: ../robot.html


Example
-------

.. code-block:: robotframework

    # Example
    # -------
    #
    #   Demonstration of pyATS Robot Framework Keywords

    *** Settings ***
    # Importing test libraries, resource files and variable files.

    Library        ats.robot.pyATSRobot

    *** Variables ***
    # Defining variables that can be used elsewhere in the test data.
    # Can also be driven as dash argument at runtime

    ${datafile}     datafile.yaml
    ${testbed}      testbed.yaml

    *** Test Cases ***
    # Creating test cases from available keywords.

    Initialize
        # select the testbed to use
        use testbed "${testbed}"

        # connec to testbed device through cli
        connect to device "ios" as alias "cli"

    CommonSetup
        # calling pyats common_setup
        run testcase "basic_example_script.common_setup"

    Testcase pass
        # calling pyats testcase
        run testcase "basic_example_script.tc_one"
