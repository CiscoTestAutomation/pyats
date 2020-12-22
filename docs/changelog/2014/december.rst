
December 9, 2014
----------------

+-------------------------------+-------------------------------+
| Module                        | Versions                      |
+===============================+===============================+
| ``ats.aereport``              | 1.0.2                         |
+-------------------------------+-------------------------------+
| ``ats.aetest``                | 1.0.3                         |
+-------------------------------+-------------------------------+
| ``ats.atslog``                | 1.0.5                         |
+-------------------------------+-------------------------------+
| ``ats.attrdict``              | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.clean``                 | 1.0.3                         |
+-------------------------------+-------------------------------+
| ``ats.connections``           | 1.0.3                         |
+-------------------------------+-------------------------------+
| ``ats.easypy``                | 1.0.6                         |
+-------------------------------+-------------------------------+
| ``ats.pda``                   | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.results``               | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.tcl``                   | 1.0.2                         |
+-------------------------------+-------------------------------+
| ``ats.tgn``                   | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.tims``                  | 1.0.1                         |
+-------------------------------+-------------------------------+
| ``ats.topology``              | 1.0.3                         |
+-------------------------------+-------------------------------+
| ``ats.utils``                 | 1.0.2                         |
+-------------------------------+-------------------------------+

Highlights
^^^^^^^^^^

* Logging mechanism revamped completely. 

* Job file now features a ``main()`` function block.

* Removed Tcl ``cast_<type>_of_()`` APIs and consolidated their
  functionality into base ``cast_<type>`` APIs

* Added Tcl Q magic function

* Tcl ``Array.keys`` API now can also accept Tcl ``[array names]`` style args.

* Keeping ``runinfo`` directory if ``-a`` argument is used.

* Revamped ``atslog`` and ``tcl`` documentation

* Execution group support in AEtest

* Csccon enhancements & etc

* Fix for assertions. AssertError now causes the test to fail

* `Bug#CSCus06696`_: Easypy mailto CLI argument now supports usernames without
  domain name in the email e.g. -mailto "<user1> <user2> <user3>@cisco.com"

* `Bug#CSCus03217`_: Fix for multiple creation of Testbed objects

* `Bug#CSCus00577`_: Fix for closing all logging handlers when trying to
  removing runinfo directory

.. _Bug#CSCus00577: https://cdetsng.cisco.com/webui/#view=CSCus00577
.. _Bug#CSCus06696: https://cdetsng.cisco.com/webui/#view=CSCus06696
.. _Bug#CSCus03217: https://cdetsng.cisco.com/webui/#view=CSCus03217

User Impacting Changes
^^^^^^^^^^^^^^^^^^^^^^

* ``banner`` API is now part of ``ats.atslog.utils`` and no longer performs the
  actual logging. It returns a pre-formatted text to be logged instead.

    .. code-block:: python
        
        import logging

        from ats.atslog.utils import banner

        logger = logging.getLogger()

        # printing a banner
        logger.info(banner('this is a banner text'))

* job file now defines a ``main()`` method. When the job file is imported, the
  ``main()`` method will be invoked, which would start the actual execution of
  the job file. All ``run`` calls should go inside this new ``main()`` method.

    .. code-block:: python
        
        import os
        from ats.easypy import run

        # process environment variables here
        script_arg_a = os.environ['script_arg_a']

        # all script runs goes into main()
        def main():

            run('/path/to/my/script.py', script_arg_a = script_arg_a)

* Tcl code can now be called via a Q magic function, making them appear like 
  Python methods and objects. See Tcl documentation for details.

    .. code-block:: python

        from ats import tcl

        tcl.q.info('exists', 'auto_path')

        tcl.q.package('require', 'cAAs')

        tcl.q.load_lib(file = '/path/to/file.tcl', 
                       os = 'NXOS',
                       functional = 1)
