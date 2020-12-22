February 2015
=============

February 20
-----------

+-------------------------------+-------------------------------+
| Module                        | Versions                      |
+===============================+===============================+
| ``ats.connections``              | 1.0.7                      |
+-------------------------------+-------------------------------+


Features:
^^^^^^^^^

 * transmit/receive for ha and non-ha devices
 * econ API's:
    - econ_state_get
    - econ_state_set
    - econ_set_process
    - econ_prepare_state
    - get_econ_state_array
 * expect internal logs
    - exp_internal
 * APIs for changing state patterns.
    - add_state_pattern
    - restore_default_state_pattern 
 * APIs for manupilating HA platform variables.
    - ha_set_platform
    - ha_get_platform  

.. note:: 

    You must be running Csccon 5.5.7 in Tcl ATS for above features 
    and Universal Console to work.

February 12
-----------

+-------------------------------+-------------------------------+
| Module                        | Versions                      |
+===============================+===============================+
| ``ats.topology``              | 1.0.8                         |
+-------------------------------+-------------------------------+

Features:
^^^^^^^^^

* Topology/loader returns exception if file is not valid

February 11
-----------

+-------------------------------+-------------------------------+
| Module                        | Versions                      |
+===============================+===============================+
| ``ats.topology``              | 1.0.7                         |
+-------------------------------+-------------------------------+

Features:
^^^^^^^^^

* Typo in exception files has been fixed.

February 2
----------

+-------------------------------+-------------------------------+
| Module                        | Versions                      |
+===============================+===============================+
| ``ats.pda``                   | 1.0.2                         |
+-------------------------------+-------------------------------+

Features:
^^^^^^^^^

* Redistributing ``ats.pda`` package with a new version. Previous distribution
  on Jan 29 did not bump up version #.
