Introduction 
============

The ``topology`` module is designed to provide an intuitive and standardized
method for users to define, handle and query testbed/device/interface/link
description, metadata, and their interconnections. 

There are two major functionalities to ``topology`` module:

#. defining and describing testbed metadata using YAML, standardizing the 
   format of the YAML file, and loading it into corresponding testbed objects. 

#. query testbed topology, metadata and interconnect information via testbed 
   object attributes and properties.


Installation
------------

``topology`` module is delivered as part of base pyATS installation in the form
of a Python Package, released via PyPI server.

.. code-block:: bash
    
    # Example
    # -------
    # 
    #   installing topology module from pypi server

    pip install pyats.topology


YAML
----

YAML (short for "YAML Ain't Markup Language" or "Yet Another Markup Language"),
is a human-readable data serialization format that is designed to be both
human readable and machine readable.

YAML is indentation & white space sensitive. Its syntax maps directly to most
common datastructures in Python, such ``dict``, ``list``, ``str`` etc.

.. code-block:: yaml
    
    # Example
    # -------
    #
    #   YAML testbed format example

    devices: 
        jarvis: 
            type: "Artificial Intelligence Computer"
            alias: "J.A.R.V.I.S"
            connections:
                voice:
                    protocol: english
            role: "Tony Stark's housekeeper"
            custom:
                appeared_in: 
                    - Iron Man
                    - Iron Man 2
                    - The Avengers
                    - Iron Man 3
                    - Avengers - Age of Ultron

The Python module called ``yaml`` (PyPI: PyYAML) is capable of reading & writing 
YAML files, as well as converting YAML data into Python datastructures.

For more information on YAML syntax, refer to: 
    
    http://yaml.org/
