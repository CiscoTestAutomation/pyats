April 2015
==========

April 9
---------

+-------------------------------+-------------------------------+
| Changed Modules               | Versions                      |
+===============================+===============================+
| ``ats.connections``           | 1.0.10                        |
+-------------------------------+-------------------------------+


Highlights
^^^^^^^^^^

* Dialogs for Linux connections.
* ``-reply`` option with ``execute`` for Linux connections.
* transmit/receive for Linux connections.
* adminconfig service for XR platforms
* adminexec service for XR platforms.

.. note::

    Tcl ATS should be running Csccon 5.6.0 for --reply feature to work

April 1
-------

+-------------------------------+-------------------------------+
| Changed Modules               | Versions                      |
+===============================+===============================+
| ``ats``                       | 1.0.4                         |
+-------------------------------+-------------------------------+
| ``ats.aereport``              | 1.0.5                         |
+-------------------------------+-------------------------------+
| ``ats.aetest``                | 1.0.6                         |
+-------------------------------+-------------------------------+
| ``ats.easypy``                | 1.0.10                        |
+-------------------------------+-------------------------------+

Highlights
^^^^^^^^^^

- Fixed unittests distribution with PyPI packages. Now all the unittests should
  be executable within user environments. This could serve as development helper
  as an in-depth demonstration of some of the design & implementation decisions.

    .. code-block:: shell

        cd $VIRTUAL_ENV/lib/python3.4/ats/topology/tests/

        python -m unittest discover

- Description can now be passed to the report file for all section. Simply add
  a ``__doc__`` to to your section. Trade however supports only Tc/Subtest. A CDET
  has been raised to support all section CSCut60575.

    .. code-block:: python

        class common_setup(aetest.CommonSetup):
            """ Common Setup section """
            @aetest.subsection
            def check_env(self):
                """ Common Setup subsection """

- Fixed a few issue with Loader for python 3 and python2.

- Internal modification to AEReport. It now fork a process for the server.

- Easypy now returns a return code. 0 if all went fine, and 1 is there was an
  issue/failure.

- Fixed a bug with Step. Now will returns fail if a step fails.

- Added a bit more awesomeness.
