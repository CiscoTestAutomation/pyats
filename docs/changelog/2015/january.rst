January 2015
============

January 30, 2015 
----------------

+-------------------------------+-------------------------------+
| Module                        | Versions                      |
+===============================+===============================+
| ``ats.connections``           | 1.0.6                         |
+-------------------------------+-------------------------------+
| ``ats.topology``              | 1.0.6                         |
+-------------------------------+-------------------------------+

Features:
^^^^^^^^^
* Linux connection support
* Linux services

    * connect 
    * disconnect 
    * execute 
    * get_platform_family 
    * get_platform_type 
    * get_os_type 
    * get_state
    * set_state 
    * add_prompt 
    * delete_prompt

User Impacting Changes 
^^^^^^^^^^^^^^^^^^^^^^

``ats.connections`` has been refactored and it will continue till next few 
releases. Due to this few imports may break in case you are directly refering 
to classes inside the ``ats.connections``. In practice it is neither required 
nor recommended to import anthing from ``ats.connections`` till we send 
notification about the same.

It may happen that you are using some pre release example code which used to 
have such references. In case of any import errors generating from 
``ats.connections`` simply delete the line of code.

.. warning:: 

    Please do not subclass anything from ``ats.connections`` till we send 
    notification.

January 29, 2015
----------------

+-------------------------------+-------------------------------+
| Module                        | Versions                      |
+===============================+===============================+
| ``ats.aereport``              | 1.0.3                         |
+-------------------------------+-------------------------------+
| ``ats.aetest``                | 1.0.4                         |
+-------------------------------+-------------------------------+
| ``ats.atslog``                | 1.0.6                         |
+-------------------------------+-------------------------------+
| ``ats.attrdict``              | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.clean``                 | 1.0.5                         |
+-------------------------------+-------------------------------+
| ``ats.connections``           | 1.0.4                         |
+-------------------------------+-------------------------------+
| ``ats.easypy``                | 1.0.8                         |
+-------------------------------+-------------------------------+
| ``ats.pda``                   | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.result``                | 1.0.2                         |
+-------------------------------+-------------------------------+
| ``ats.tcl``                   | 1.0.3                         |
+-------------------------------+-------------------------------+
| ``ats.tgn``                   | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.tims``                  | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.topology``              | 1.0.5                         |
+-------------------------------+-------------------------------+
| ``ats.utils``                 | 1.0.3                         |
+-------------------------------+-------------------------------+

Highlights
^^^^^^^^^^

* Install script now checks for CEL package dependencies

* Removed bug with ``topology`` where it required ``Csccon``, which further
  required ``tcl``, causing the whole thing to fail when ``_tkinter`` is not
  available on target machine. 

* Ubuntu 12.04 and 14.04 LTS support

* Steps are now available! Use them to further divide Testcases. Find
  documentation in AETest Steps

* Exposed some runtime info to the user script such as runtime (logs) 
  directory, jobname, jobid. (Beta)
 
* The subject of the report email now contains some useful info such as
  jobname, submitter, pass/fail, etc

* Added -i, -r, and -user CLI arguments for easypy to enable passing image,
  release, and alternative user info

* Enabled tracking of Python3 vs Python2 usage on CES website

* Modification to result rolled up logic; Skipped + Passed is now = Passed.

* Added dynamic device connection example 

* Fixed issue with ``topology`` and ``connections.csccon`` for support for 
  multiple devices with the same hostname. Added device.hostname to schema.

* In AETEST testcase attributes ID, DESCRIPTION, EXECUTION_GROUP, SEQUENCE is
  is renamed to , id , description, execution_group and sequence in order to be
  inline with PEP8.

* Topology schema change, servers (such as ntp, tftp) now falls under servers:
  field

* Topology schema changes, custom keywords can go under custom.

* New flags are supported in execute and config services which allow user to 
  provide answers to router interactive-prompts 
  
Beta : Feature that has a high chance to be modified in the near future. Though
can be used for people that really needs it.   

User Impacting Changes
^^^^^^^^^^^^^^^^^^^^^^

* In AETEST testcase attributes ID, DESCRIPTION, EXECUTION_GROUP, SEQUENCE is
  is renamed to , id , description, execution_group and sequence in order to be
  inline with PEP8.

.. code-block:: python

    class my_tc_one(aetest.Testcase):
        execution_group = 'group2'

* Topology schema change, servers (such as ntp, tftp) now falls under servers:
  field. Yaml example below.

.. code-block:: text

    testbed:
        servers:
            ntp:
                address: <...>
            tftp:
                username: <...>
                password: <...>
                address: <...>

* Topology schema changes, custom keywords go under custom. Yaml example
  below:

.. code-block:: text

    testbed:
        custom:
            <anything1>: <anyValue1>
            <anything2>: <anyValue2>
            <anything3>: <anyValue3>

* Modification to result rolled up logic; Skipped + Passed is now = Passed.

Example
^^^^^^^

* Retrieving runtime info:

.. code-block:: python

    from ats.easypy import runtime

    print("Logs dir: {}".format(runtime.directory))
    print("Job id: {}".format(runtime.jobid))
    
* How to pass additional arguments to execute and config service:

.. code-block:: python

    from ats.topology import Testbed
    import collections

    t = Testbed(config_file='conf.yaml')
    rtr1 = t.devices['Router1']
    rtr1.connect()

    result = rtr1.execute("show clock", timeout = 600)
    result = rtr1.execute("show andndnk", 'fail_invalid' )

    # Execute command on standby
    result = rtr1.execute("show redundancy state", 'stadby')

    # To provide answers to router interactive-prompts exec commands
    response = collections.OrderedDict()
    response["Confirm [y/n]"] = "send y ; expect_continue"
    response["Confirm "] = "send n ; expect_continue"
    rtr1.execute("show clock", "fail_invalid", saveto = 'var', reply = response)

    #Config command with additional csccon flags
    rtr1.config("hostname 7200-28-41", "no logging con", "line con 0",\
                 "fail_invalid", saveto = 'var')
                 
    # Config command  with interactive-prompts
    response = collections.OrderedDict()
    response["Confirm [y/n]"] = "send y ; expect_continue"
    response["Confirm "] = "send n ; expect_continue"
    rtr1.config("hostname halib-65", "no logging console", "line con 0".\
                      "fail_invalid", saveto = 'var', reply = response)

.. note:: response pattern to reply flag must be a Ordered Dictionary, in roder to
          avoid maintain the exact pattern order.

For more details about the default flags supported refer Link_

.. _Link: https://wiki.cisco.com/display/ATS/CSCCON+SubCommand+Enhancement

