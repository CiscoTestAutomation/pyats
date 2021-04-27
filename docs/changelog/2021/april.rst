March 2021
==========

March 30, 2021
--------------

.. csv-table:: New Module Versions
    :header: "Modules", "Version"

    ``pyats``, v21.4
    ``pyats.aereport``, v21.4
    ``pyats.aetest``, v21.4
    ``pyats.async``, v21.4
    ``pyats.cisco``, v21.4
    ``pyats.connections``, v21.4
    ``pyats.datastructures``, v21.4
    ``pyats.easypy``, v21.4
    ``pyats.kleenex``, v21.4
    ``pyats.log``, v21.4
    ``pyats.reporter``, v21.4
    ``pyats.results``, v21.4
    ``pyats.robot``, v21.4
    ``pyats.tcl``, v21.4
    ``pyats.topology``, v21.4
    ``pyats.utils``, v21.4

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Make sure you are using the latest pip package
    bash$ pip install --upgrade pip

    # DevNet Community
    bash$ pip install --upgrade pyats

    # Cisco Internal Developers
    bash$ pip install --upgrade ats

Known Issues
^^^^^^^^^^^^

On MacOs we have observed issues with the `requests` package used for REST API calls,
the workaround is to set the environment variable `no_proxy` to a value,
e.g. domain.com. Without this, we have seen crashes that halt the script execution.
This issue seems to be related to a bug in MacOS python https://bugs.python.org/issue31818

--------------------------------------------------------------------------------
                                      Fixes
--------------------------------------------------------------------------------

* Cisco
    * Added devAT.use_lib API:
      * To support versioned external libraries such as ixia, trex, etc.
      * Allows multiple versions of the same package to coexist

* pyats
    * Modified configuration:
      * Added new --pyats-configuration argument to specify an additional
        configuration file to be loaded
