March 2015
==========

March 17
--------

+-------------------------------+-------------------------------+
| Changed Modules               | Versions                      |
+===============================+===============================+
| ``ats.connections``           | 1.0.9                         |
+-------------------------------+-------------------------------+


Bug Fixes
^^^^^^^^^
* Fixed ssh protocol issue with Vty connections.
* Minor fix in set_csccon_xxx APIs

March 13
--------

+-------------------------------+-------------------------------+
| Changed Modules               | Versions                      |
+===============================+===============================+
| ``ats.topology``              | 1.1.1                         |
+-------------------------------+-------------------------------+

* Added alias access to ``topology``. See alias section under topology usage
  documentation. (this feature is expected to be backwards compatible)


March 11
--------

+-------------------------------+-------------------------------+
| Changed Modules               | Versions                      |
+===============================+===============================+
| ``ats.aereport``              | 1.0.4                         |
+-------------------------------+-------------------------------+
| ``ats.aetest``                | 1.0.5                         |
+-------------------------------+-------------------------------+
| ``ats.atslog``                | 1.0.7                         |
+-------------------------------+-------------------------------+
| ``ats.attrdict``              | REMOVED                       |
+-------------------------------+-------------------------------+
| ``ats.clean``                 | 1.0.6                         |
+-------------------------------+-------------------------------+
| ``ats.connections``           | 1.0.8                         |
+-------------------------------+-------------------------------+
| ``ats.datastructures``        | 1.0.0                         |
+-------------------------------+-------------------------------+
| ``ats.easypy``                | 1.0.9                         |
+-------------------------------+-------------------------------+
| ``ats.results``               | 1.0.3                         |
+-------------------------------+-------------------------------+
| ``ats.tcl``                   | 1.0.4                         |
+-------------------------------+-------------------------------+
| ``ats.tims``                  | 1.0.2                         |
+-------------------------------+-------------------------------+
| ``ats.topology``              | 1.1.0                         |
+-------------------------------+-------------------------------+
| ``ats.utils``                 | 1.0.4                         |
+-------------------------------+-------------------------------+


Highlights
^^^^^^^^^^

* added ``__init__`` to ``TestResult`` object, and added unittest coverage for
  ``results`` module.

* Renamed ``attrdict`` module to ``datastructures`` module, enabling it to
  contain more than the attribute dictionary datastructures.

* The runinfo directory will contains taskresults directory which allows
  at runtime to see the result of each section, subtest, testcase and so on.
  The directory is deleted after the run is completed.

* Tims result file is always created even when post information is not
  provided. It then can be uploaded manually later on.

* Loop ids are retrieved with an extra ``str()`` call.
  Example updated to provide an example (eg, int to str)

* ``topology`` module completely refactored, with documentation updated. See
  below for details on changes

* ``aetest`` internally refactored. See below for details

* Testbed schema change: removed ``servers:`` section from devices, consolidated
  into ``servers:`` section under ``testbed:``.

* Loop can be now declared directly in the @test decorator.
  @aetest.test(ids=[1,2]) or @aetest.test(variants=[1,2]). However,
  @aetest.loop still exists and can be used.

* A new naming convention is followed for CLI arguments:

    * All infra arguments use the single dash format (e.g. -tf, -testbed)

    * All infra arguments use underscore separated words for multi-word arguments

    * All user defined arguments should use the double dash format
      (e.g. --my_arg)

* Argument -user is now -submitter

* Loop can be now declared directly in the @test decorator.
  @aetest.test(ids=[1,2]) or @aetest.test(variants=[1,2]). However,
  @aetest.loop still exists and can be used.

* ``Easypy`` now allows ``ios_commands_file``, ``folder``, ``importer_options``
  to be passed to tims via the control file.

* When connecting using ``Device.connect()`` and ``via='..'`` argument, ``via``
  now no longer requires the prefix ``connections.``. Eg:

    .. code-block:: python

        # before:
        device.connect(via = 'connections.alt')

        # now:
        device.connect(via = 'alt')

Example
^^^^^^^

    * To replace the default email subject with a custom one:

        .. code-block:: bash

            easypy /path/to/job/file -mail_subject "my subject here"

AEtest Changes
^^^^^^^^^^^^^^

* ``incl_common_result`` which defaulted to ``True`` is now changed to
  ``exclude_common_results``, defaulting to ``False``. This is to be more inline
  with the command line argument. The behavior is not changed.

* Changed the following arguments to AEtest run script:

    * ``mode``: removed. (no user impacting)

    * ``testReport``: renamed to ``testreporter``

    * ``runinfo_dir``, ``task_id``, ``log_per_testcase``, ``verbose``,
      ``quiet``: all removed. (no user impacting)

    * ``script_args``: removed. all user arguments to script automatically
      gets stored in ``**kwargs``.

    * ``unittest``: removed. engine automatically figures out if the script
      is unittest.

* Changed the following ``python -m ats.aetest`` command line arguments:

    * using ``-`` single dash style arguments instead of ``--``.

    * added ``-submitter`` argument (changes the CES user)

    * beefed ``-h`` help info

* Added ``aetest.runtime`` module to enable querying runtime information by
  the user.


Topology Changes
^^^^^^^^^^^^^^^^

* Topology documentation fully updated with schema & etc. All details covered
  in this section is covered in the documentation with details.

* All internal references of parent object (eg, ``Device.testbed``) is now done
  using weak references, allowing proper python garbage collection behavior.

    * all ``delete`` APIs removed from all objects

* Topology objects singleton behavior (eg, Device) is gone, users are free to
  create and re-create testbeds and devices.

* ``Mgmt`` and ``Console`` classes removed altogether. Connections will now
  solely be stored as dictionaries support kwargs internally.

* all ``delete`` APIs removed

* Topology creation using testbed file now is done via ``topology.loader``, and
  no longer through instantiating ``Testbed`` object.

* ``Link`` object changes:

    * ``get_link()`` removed, links are no longer singletons

    * ``add_interface()`` -> ``connect_interface()``

    * ``remove_interface()`` -> ``disconnect_interface()``

    * new properties ``connected_devices``, ``connected_interfaces``

    * ``Link.interfaces`` is now a ``WeakList``

    * added alias property

* ``Interface`` object changes:

    * ``Interface.device`` is now a weakref to device object

    * ``get_remote_interfaces()`` API -> ``remote_interfaces`` property

    * new properties ``remote_devices``

    * added alias property

* ``Device`` object changes:

    * added alias property

    * ``Device.testbed`` is now a weakref to testbed object

    * modified how ``ConnectionManager`` integrates with ``Device`` object

    * removed ``get_device()`` api. Devices are no longer unique.

    * ``get_links()`` api -> ``links`` property

    * ``get_interfaces()`` api removed

    * new properties: ``remote_devices``, ``remote_interfaces``

    * ``get_connections()`` -> ``find_links()``

* ``Testbed`` object changes

    * no longer instantiates with a YAML testbed file (do this with loader
      instead). ``Testbed`` is now a proper container top-level class.

    * ``get_links()`` api -> ``links`` property

    * ``get_devices`` removed. use ``Testbed.devices`` dict

* New: ``topology.loader``

    * loads a YAML testbed file and returns the corresponding topology objects
      contained within a ``Testbed`` object.

    .. code-block:: python

        from ats.topology import loader
        testbed = loader.load('/path/to/yaml')

* New feature: providing alternative subclasses of ``Testbed``, ``Device``,
  ``Link``, ``Interface`` through testbed yaml loading.


Datastructures & AttrDict
^^^^^^^^^^^^^^^^^^^^^^^^^

Attribute Dictionary ``AttrDict`` module ``ats.attrdict`` is now consolidated
into a new module named ``ats.datastructures``, where overtime we will introduce
new datastructures that will help with the community.

* ``ats.attrdict`` removed

* ``ats.datastructures`` added

* New datastructures: ``WeakList``, ``ListDict``
