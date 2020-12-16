November 2014
=============


November 24, 2014
-----------------

* Fix for cleaning up and removing job directory after the run

* Fix for logging issue when sending the email report

--------------------------------------------------------------------------------


November 21, 2014
-----------------

* removed AEreport logging to screen

* Fix for the missing Csccon and other log msgs

* Better control on debug vs. info logging mode

* Astlog banner syntax bug with ``[:end]``

* Fix for displaying error msgs in case of exception for script execution

--------------------------------------------------------------------------------

November 20, 2014
-----------------

* Remove dependency from TCL ATS, there is no need to source a Tcl tree if you 
  aren't using it.

* Enhancement for AEtest [skip|run]_run_ids 

* skip logging environment variables with non-supported encoding

* Remove DEBUG msg for ``easypy`` and ``aetest`` logs, unless -D is passed as 
  an argument.

* Fixed issue with importing csccon

* Fixed issue with AEtest ``script_args``


--------------------------------------------------------------------------------


Official Release
----------------

Official release of pyATS project on  November 17, 2014

+-------------------------------+-------------------------------+
| Module                        | Versions                      |
+===============================+===============================+
| ``ats``                       | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.aereport``              | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.aetest``                | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.atslog``                | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.attrdict``              | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.connections``           | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.easypy``                | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.pda``                   | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.results``               | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.tcl``                   | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.tgn``                   | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.topology``              | v1.0.0                        |
+-------------------------------+-------------------------------+
| ``ats.utils``                 | v1.0.0                        |
+-------------------------------+-------------------------------+

Highlights
^^^^^^^^^^

We are pleased to announce the release of pyATS - Cisco Python Automated Test 
Systems, a joint effort collaboration between ASG & ATS team. 

pyATS is the next-generation, Python-based, Cisco mainstream test automation 
ecosystem. Built with Agile software methodologies in mind, it is engineered
for rapid development iterations, with the ability to handle a wide variety of
testing scenarios & requirements, bridging the gap between tradition DE/DTs, 
promoting team-oriented development cultures.

pyATS is highly extensible. It is compatible with existing Cisco ATS 
infrastructure & tooling, enables the reuse of existing scripts, packages and
libraries, featuring a high-degree of familiarity with current ATS 
infrastructure whilst maintaining all the perks Python has to offer. 

+------------------------------------------------------------------------------+
| Infrastructure Features                                                      |
+==============================================================================+
| Python 3.4 development with Python 2.7 support                               |
+------------------------------------------------------------------------------+
| Internal PyPI distribution of pyATS modules/packages                         |
+------------------------------------------------------------------------------+
| Git-based, distributed software version control repository                   |
+------------------------------------------------------------------------------+
| Seamless Tcl integration: reuse existing scripts, libraries & etc.           |
+------------------------------------------------------------------------------+
| Object Oriented AEtest with Python unittest & dynamic testcase/object support|
+------------------------------------------------------------------------------+
| YAML standard format                                                         |
+------------------------------------------------------------------------------+
| SSR/EARMs/TRADe/TIMS/Clean support & compatibility                           |
+------------------------------------------------------------------------------+
| Dedicated engineering team for enhancements, TOIs, support & etc.            |
+------------------------------------------------------------------------------+


+------------------------------------------------------------------------------+
| Design Abstract                                                              |
+==============================================================================+
| Abstract classes: modular, easy to extend & enhance, plugin-support          |
+------------------------------------------------------------------------------+
| Clean-cut dependencies with individual package releases under PyPI           |
+------------------------------------------------------------------------------+
| Exception-driven flow control                                                |
+------------------------------------------------------------------------------+
| Similar look and feel to Tcl ATS whilst leveraging Python core concepts &    |
| OOP designs                                                                  |
+------------------------------------------------------------------------------+
| Auto documentation                                                           |
+------------------------------------------------------------------------------+


Differences vs. Beta
^^^^^^^^^^^^^^^^^^^^

* YAML schema: ``mgmt`` and ``consoles`` consolidated into ``connections``.

* YAML schema: ``tbname`` to just ``name``

* Tcl module: global interpreter changed: ``ats.tcl`` module itself is now the
  global interpreter. 

* Job files: ``ats_run`` renamed to just ``run``

* Job files: removed ``script_args`` argument to ``run``. Now all additional
  arguments will be passed through as script arguments

* AETest: removed ``SCRIPT_ARGS``, and changed the mechanism for script
  arguments to ``self.script_args`` dictionary in each test section body.




