RobotFramework Support
======================

`RobotFramework`_ is generic Python/Java test automation framework that focuses
on acceptance test automation by through English-like keyword-driven test
approach.


.. sidebar:: Section Index

    .. toctree::
        :maxdepth: 2

        easypy
        native

    - `pyATS Keywords`_


.. _RobotFramework: http://robotframework.org/
.. _pyATS Keywords: ../robot.html


You can now freely integrate pyATS into RobotFramework, or vice versa:

1. running RobotFramework scripts directly within Easypy, saving runtime logs
   under runinfo directory, and aggregating results into Easypy report.

2. leverage pyATS infrastructure and libraries within RobotFramework scripts.

However, as **RobotFramework support is an optional component** under pyATS, you
must install the package explicitly before being able to leverage it:

.. code-block:: bash

    # Installing RobotFramework support for pyATS
    # -------------------------------------------

    # DevNet Community
    bash$ pip install --upgrade pyats.robot

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.robot
