Introduction
============

.. sidebar:: Quick References

    - :ref:`Testbed Topology <testbed-index>`

*In the beginning, there were fixed, physical testbeds. Each testbed device had
its own uniquely implemented clean procedures, and there was chaos...*

*As test automation technologies advanced, virtual & physical dynamic testbeds were added
to the mix. Each operated differently, and chaos prospered...*

*And then came...* **Kleenex**, a framework designed to standardize the process
and implementation of the provisioning and cleaning of testbed topologies
and devices.




Clean
-----

Device cleaning (a.k.a. **Clean**) defines the process of preparing physical
testbed devices by loading them with appropriate images (recovering from bad
images), removing unnecessary configurations and returning devices to their
default initial state by applying basic configurations such as
console/management ip addresses, etc.

Kleenex offers the base infrastructure required by all clean implementations:

    - integration with :ref:`easypy` and :ref:`Testbed Objects <testbed-index>`
    - structured input format & information grouping through a
      :ref:`clean_file`
    - automatic asynchronous device cleaning
    - runtime, exception & logging handling

...and all the necessary guidelines and information required for users to
develop their platform specific clean methods.

*Kleenex Clean* standardizes how users implement platform-specific clean
methods, providing the necessary entry points and subprocess management.


Installation
------------

The Kleenex module ``kleenex`` is installed by default as part of pyATS
installation. It is also a pre-requisite to installing the ``easypy`` module.
This package is featured on the PyPI server.

.. note::

    The ``kleenex`` module is part of the ``pyats`` namespace, and therefore,
    users should always refer to the full namespace when installing & using it.


.. code-block:: bash

    pip install pyats.kleenex

To upgrade an existing installation of the Kleenex package in your environment,
do:

.. code-block:: bash

    pip install pyats.kleenex --upgrade

.. note ::

    always read the :ref:`changelog` first before you upgrade.


Glossary
--------

.. glossary::
    :sorted:

    Orchestration
        The automated arrangement, coordination, and management of complex
        computer systems, middleware and services. Eg: provisioning dynamic
        testbed topologies, allocating resources, etc.

    Clean
        The process and procedures required to bring a physical
        router/device to a testable steady state.
        Includes but not limited to:

            - loading new images
            - returning to default/initial states
            - configuring the bare-minimum required for console/mgmt
              connections
            - etc

    Cleaner
        A particular clean implementation inheriting the 
        `BaseCleaner<pyats.kleenex.bases.BaseCleaner>` class.

    Clean File
        A YAML_ based input file containing details of how to prepare and clean
        the testbed, used by Kleenex.

    Logical Testbed File
        A YAML_ file that describes a topology of logical devices and their
        interconnections. Logical testbed files are not loadable, they may be
        seen as a set of constraints that must be passed to an orchestration
        backend in order to be transformed into an actual loadable testbed
        file.

    Testbed
        The sum of all actual devices (routers, switches, TGNs)
        interconnected together. In pyATS, the testbed is represented using
        :ref:`Topology Module<testbed-index>`.

    Dynamic Testbeds
        Testbeds defined using logical device requirements, and provisioned
        through orchestrators. Typically, a dynamic testbed is a sum of
        hardware and virtual devices allocated & prepared through a
        cloud infrastructure.

    Logical Device
        A set of constraints that contain enough information for an
        orchestrator to bind the requested logical device to an actual
        device.

    Actual Device
        A live device that can be connected to, for example, via a
        console connection.


.. _YAML: http://www.yaml.org/spec/1.2/spec.html
