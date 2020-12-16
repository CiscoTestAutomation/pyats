June 2015
=========

June 30, 2015
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v2.0.2
    ``ats.tcl``, v2.0.3
    ``ats.tgn``, v2.0.3
    ``ats.topology``, v2.0.2

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

- if you are upgrading from v2.0.1+, it's pretty straightforward.
 
  .. code-block:: bash

      bash$ pip install --upgrade ats

- if you are upgrading from a lower version, refer to v2.0.0 and v2.0.1 upgrade
  instructions for details.

Bug Fixes
^^^^^^^^^

- ``aetest.TestScript`` class now handles built-in objects properly and no 
  longer crashes in rare conditions.

- ``tcl.Interpreter.Q`` magic Q function received some minor tune-ups.

- ``tcl.Interprter`` class now displays errors & ``AUTOTEST`` requirements a bit
  more clearer.

- ``tgn`` module received minor tune-ups w.r.t. how Q function is called.

- ``topology.loader`` now properly processes markups defined in YAML lists.

- ``topology.loader`` now properly checks for mal-formed string type inputs.

Misc
^^^^

- :ref:`testbench` is now updated with ``aetest`` v2.0.0 content.


June 29, 2015
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats``, v2.0.2
    ``ats.easypy``, v2.0.2
    ``ats.tcl``, v2.0.2
    ``ats.tgn``, v2.0.2

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

- if you are upgrading from v2.0.1+, it's pretty straightforward.
 
  .. code-block:: bash

      bash$ pip install --upgrade ats

- if you are upgrading from a lower version, refer to v2.0.0 and v2.0.1 upgrade
  instructions for details.


Install Changes
^^^^^^^^^^^^^^^

- install script now checks for your network connectivity and prints warnings
  when proxy is required.


Easypy
^^^^^^

- fixed a minor problem with test code that could raise suspicion to users
  during installation (compile error, though it is an intended error)

Tgn
^^^

- updated Tgn module to use Tcl module's Q functionality (does not impact users)

- added custom argument ``raise_ = False`` to all hltapi calls for disabling 
  raising exception when the keyed-list return ``status`` is 0.

  .. code-block:: python

      # provide raise_ = False argument to make sure no exceptions are raised
      ixia.traffic_stats(port_handle='1/1/3', raise_ = False)

- added support for Ixia and Pagent ``connect()`` api to also accept a Topology
  ``Device`` object. ``connect()`` will automatically pull required information
  from the ``Device`` object in order to connect.

  .. code-block:: yaml
      
      # Example
      # -------
      #    example pagent and ixia yaml
      devices:
          mypagent:
              type: pagent
              connections:
                  a:
                      protocol: 'telnet'
                      ip: '1.1.1.1'
                      port: 1000
              passwords:
                  enable: lab
          ixia:
              type: ixia
              connections:
                  ixia:
                      protocol: ixia
                      ip: 1.1.1.1
                      tcl_server: 1.2.2.2
                      username: ixiausername


  .. code-block:: python

      # Example
      # -------
      #  and be able to do this in your code

      from ats.tgn.hltapi import Pagent, Ixia

      pagent = Pagent()
      ixia = Ixia()

      pagent.connect(device=testbed.devices['mypagent'])
      ixia.connect(device=testbed.devices['ixia'])

Tcl
^^^

- added Q magic flag ``cast_ = False`` to disable the auto-casting behavior.

  .. code-block:: python

      from ats import tcl

      tcl.eval('keylset klist a 1 b 2 c 3')

      tcl.q.set('klist')
      # KeyedList({'a': '1', 'c': '3', 'b': '2'})

      tcl.q.set('klist', cast_ = False)
      # '{a 1} {b 2} {c 3}'

- Added Tcl ``::errorInfo`` stacktrace to ``TclError`` exceptions. This will
  provide a bit more debug information for Q and ``eval`` functionalities.


June 24, 2015
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats``, v2.0.1
    ``ats.aereport``, v2.0.1
    ``ats.aetest``, v2.0.1
    ``ats.atslog``, v2.0.1
    ``ats.clean``, v2.0.1
    ``ats.connections``, v2.0.1
    ``ats.datastructures``, v2.0.1
    ``ats.easypy``, v2.0.1
    ``ats.examples``, v2.0.1
    ``ats.results``, v2.0.1
    ``ats.tcl``, v2.0.1
    ``ats.templates``, v2.0.1
    ``ats.tgn``, v2.0.1
    ``ats.tims``, v2.0.1
    ``ats.topology``, v2.0.1
    ``ats.utils``, v2.0.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

- before you upgrade, please remove your pyATS instance's ``examples`` and
  ``templates`` folder altogether. All new templates & examples will be 
  packaged and installed through ``pip``.

  .. code-block:: bash

      bash$ cd $VIRTUAL_ENV
      # note - this will delete it. If you modified examples/templates,
      # make sure to make local backups
      bash$ rm -rf templates examples

- if you are currently running Python-3 version of pyATS, upgrade directly as:

  .. code-block:: bash

      bash$ pip install --upgrade ats

- if you are currently running Python-2 version of pyATS, due to the new
  wheels_ packaging, you will have to uninstall all ``-py2`` packages and 
  reinstall with ``ats`` directly. 

  .. note:: 

      this is an inconvenience just for this time... from here onwards you will
      be able to directly update using the name ``ats`` and not having to deal
      with ``-py2`` postfix.


  .. code-block:: bash

      # uninstall everything
      bash$ pip uninstall ats 
      bash$ pip uninstall ats.aereport 
      bash$ pip uninstall ats.aetest 
      bash$ pip uninstall ats.atslog 
      bash$ pip uninstall ats.clean 
      bash$ pip uninstall ats.connections 
      bash$ pip uninstall ats.datastructures 
      bash$ pip uninstall ats.easypy 
      bash$ pip uninstall ats.examples 
      bash$ pip uninstall ats.results 
      bash$ pip uninstall ats.tcl 
      bash$ pip uninstall ats.templates 
      bash$ pip uninstall ats.tgn 
      bash$ pip uninstall ats.tims 
      bash$ pip uninstall ats.topology 
      bash$ pip uninstall ats.utils 

      # install just "ats" --> pip will automatically pick up python-2 wheels.
      bash$ pip install ats

      # or... you can just upgrade the instance altogether
      # note that this will RE-CREATE your entire pyATS instance
      bash$ /auto/pyats/bin/pyats-install --python2 --upgrade

- new versions of public PyPI package dependencies have been sanctioned. Feel 
  free to update your local versions of the following:

  .. code-block:: bash

      bash$ pip install --upgrade pip setuptools pyyaml psutil

      # due to a new requirement for PIP, also add the following to your env:
      # for env.sh, add the following after "BEGIN CUSTOM pyATS CONTENT"
      export PIP_TRUSTED_HOST=ats-pypi-server.cisco.com

      # for env.csh, add the following "BEGIN CUSTOM pyATS CONTENT"
      setenv PIP_TRUSTED_HOST ats-pypi-server.cisco.com


Installation
^^^^^^^^^^^^

- pyATS packages from this release on will be packaged using wheels_ instead of
  ``*.tar.gz`` source tarballs. This is transparent to the user when installing
  from ``pip``.
  
  - however, as a direct, positive impact, python-2 packages will no longer
    have ``-py2`` trailing postfix from here-onwards. ``pip`` will automatically
    install the correct version.

    .. code-block:: bash

        # installing python-3 pyats packages
        bash$ pip install ats

        # installing python-2 pyats packages (same as python-3)
        bash$ pip install ats

- a number of PyPI packages are now validated and updated in our repository. The
  install process will now automatically install the latest and greatest.
  
  .. code-block:: text
    
      alabaster (0.7.6)
      altgraph (0.12)
      astroid (1.3.6)
      Babel (1.3)
      bleach (1.4.1)
      coverage (3.7.1)
      docutils (0.12)
      html5lib (0.99999)
      httplib2 (0.9.1)
      ipdb (0.8)
      ipython (2.3.1)
      Jinja2 (2.7.3)
      logging-tree (1.6)
      logilab-common (0.63.2)
      MarkupSafe (0.23)
      nose (1.3.4)
      pip (7.0.3)
      pockets (0.2.4)
      psutil (3.0.1)
      py (1.4.29)
      Pygments (2.0.2)
      pylint (1.4.3)
      pytest (2.7.2)
      pytz (2015.4)
      PyYAML (3.11)
      readme (0.5.1)
      restview (2.4.0)
      setuptools (17.1.1)
      six (1.9.0)
      snowballstemmer (1.2.0)
      Sphinx (1.3.1)
      sphinx-rtd-theme (0.1.8)
      sphinxcontrib-napoleon (0.3.10)
      wheel (0.24.0)

- installation script now supports specifying a specific pyATS version.
  
  .. code-block:: python

      # installing version 1.0.4
      bash$ /auto/pyats/bin/pyats-install --version="1.0.4"

      # installing latest (default behavior)
      bash$ /auto/pyats/bin/pyats-install

.. _wheels: https://wheel.readthedocs.org/en/latest/

AEtest
^^^^^^

- ``DefaultLooper`` id generation based on loop parameters now automatically
  converts spaces to underscores.

- fixed an issue where ``TestScript`` parameter object is not preserved
  internally. The following should now work:

  .. code-block:: python

      # Example
      # -------
      #
      #   parameter dict updates reflects in TestScript

      from ats import aetest

      parameters = {}

      class Testcase(aetest.Testcase):

          @aetest.setup
          def setup(self):
              # add new stuff to parameters
              parameters['new'] = 1

              # propagates to parameters
              assert 'new' in self.parameters

          @aetest.test
          def test(self, new):
              # and useable
              assert new == 1

Easypy
^^^^^^

- ``env.txt`` now also contains tcl ``teacup`` package information
- ``run()`` api now returns the overall result of script run.

Results
^^^^^^^

- result objects now support boolean testing. ``Passed`` and ``Passx`` tests
  ``true``. All else tests ``False``.

  .. code-block:: python

      from ats.results import *

      bool(Passed)
      # True

      bool(Passx)
      # True

      bool(Failed)
      # False

Misc
^^^^

- Examples & templates are now PyPI packages instead of straight-up copies. They
  are installed using ``pip``, carries a version, but is still installed under
  the root instance folder as ``examples/`` and ``templates/``.

  .. code-block:: bash

      bash$ pip install ats.examples
      bash$ pip install ats.templates

- installation now logs a copy of user environment variables into 
  ``install.log``.

- all packages now contains metadata, eg:

  .. code-block:: python

      from ats import aetest

      aetest.__version__
      # 2.0.0

      aetest.__author__
      # ASG/ATS Team

      aetest.__contact__
      # pyats-support@cisco.com

- internal refactoring of pyATS source repositories. Should not impact users.

.. _v2.0.0:

June 15, 2015 - pyATS v2.0.0
----------------------------
 
pyATS release major milestone: ``v2.0.0``. 

    *Please take a moment to study this changelog.*

.. warning::

    major release versions are **not** backwards compatible. 

    Refer to pyATS pyats_package_versions conventions.

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats``, v2.0.0
    ``ats.aereport``, v2.0.0
    ``ats.aetest``, v2.0.0
    ``ats.atslog``, v2.0.0
    ``ats.clean``, v2.0.0
    ``ats.connections``, v2.0.0
    ``ats.datastructures``, v2.0.0
    ``ats.easypy``, v2.0.0
    ``ats.results``, v2.0.0
    ``ats.tcl``, v2.0.0
    ``ats.tgn``, v2.0.0
    ``ats.tims``, v2.0.0
    ``ats.topology``, v2.0.0
    ``ats.utils``, v2.0.0

To pick up these new changes, activate your pyATS instance and do:

.. code-block:: bash
    
    # note: uts ats-py2 if you are on using python-2 version of pyATS
    bash$ pip install --upgrade ats

Latest examples & templates have also been distributed as part of this release.
You may copy them to your pyATS instance:

.. code-block:: bash

    bash$ cd $VIRTUAL_ENV
    bash$ mv examples examples_bak
    bash$ mv templates templates_bak
    bash$ cp -r /auto/pyats/examples .
    bash$ cp -r /auto/pyats/templates .

Content
^^^^^^^

This release is sanctioned as v2.0.0 as it is a significant upgrade in terms of 
user-experience & test engine feature sets. As a result, testscripts will not
be backwards compatible and will require modifications in order to upgrade.

    *steps towards a better, more streamlined user experience*

- major revamp to ``aetest`` script engine

  - testscripts with data-driven parameters
  - section pre/post processors support
  - redesigned script argument propagation & referencing
  - redesigned run ids and testcase grouping feature
  - redesigned steps feature
  - redesigned test section looping, with parameters
  - user access to runtime & object model information
  - *removal of* ``CommonVerify`` *section*
  - *phasing out (obsoleting)* ``Subtest`` *support*

- ``easypy`` enhancements:

  - native jenkins integration
  - ``runtime`` information access
  - *obsoleted control files support*

    - a new clean-YAML file has been introduced to replcae the missing clean 
      parameter functionality.
    - to batch your job runs with reduced arguments, use shell scripts, do not
      use control files.

  - unified command-line argument look & feel

    - argument propagation scheme from command line to job file and to 
      testscript

- new & improved examples and advanced templates

- revised error & exception catching throughout the test engines

- 200+ pages of new, updated, self-explanatory documentation.

  - explaning internal object models for the first time
  - now also availabe in PDF format, intended to be used as the *pyATS bootcamp*
    training material.

- *many many other bugfixes & enhancements.*



Easypy Changes
^^^^^^^^^^^^^^

- Easypy now prints TRADe links in the log and at the end of your run.

- Jenkins! Find all the information here easypy_jenkins
 
- Improved error & exception handling.

- Directory ``atseasy`` is renamed to ``users``. ``atseasy/etc`` and
  ``atseasy/job`` are no-longer created. Existing logs will be moved over to
  this new directory structure, and ``atseasy`` will be left behind as a symlink
  until EARMs is about to cope with the new folders.

- ``users`` directory is created with 777 permission. This will make
  sharing of the virtual environment with other users much easier.

- ``JobLog`` now logs all Easypy outputs. (was not logging correctly before)

- New Easypy ``runtime`` variable that allows access to runtime information
  such as archive directory, archive file name, runinfo directory, job name
  and id.

- Arguments standardization:
  
  - All short form arguments are removed. (eg, ``-tb``)

  - ``-debug`` has been removed and replaced by ``-loglevel``

  - Many arguments have been renamed for consistency

    .. csv-table:: EasyPy Arguments Mappings
        :header: "Old arguments name", "New arguments name"

        ``-a`` ``-noarchive``, ``-no_archive``
        ``-archive_dir`` , ``-archive_dir``
        ``-control_file``, *removed*
        *N/A*, ``-clean_file``
        ``-d``, *removed*. Use ``-loglevel`` instead
        ``-dns_name`` , ``-tims_dns``
        ``-folder`` , ``-tims_folder``
        ``-h`` ``-help`` , ``-help``
        ``-i`` ``-image``, ``-image``
        ``-import_options`` , ``-tims_options``
        ``-ios_commands_file`` , *removed*
        ``-mailto`` , ``-mailto``
        ``-no_log_copy``, ``-no_log_copy``
        ``-nomail`` , ``-no_mail``
        ``-p`` , ``-tims_post``
        ``-r`` ``-release``, ``-release``
        ``-runinfo_dir`` , ``-runinfo_dir``
        ``-submitter``, ``-submitter``
        ``-tf``, ``-testbed_file``
        ``-t`` ``-testbed``, *removed.* Use ``-testbed_file`` instead
        ``-xunit_dir`` , ``-xunit_dir``
        ``-xunit`` , ``-xunit``
        *N/A*, ``-loglevel``
        *N/A* , ``-tims_custom_attrs``

AEtest Changes
^^^^^^^^^^^^^^

Major revamp to all ``aetest`` internals. New features & use cases, along with
documented functions/class headers and 100+ pages of user guides. 

.. tip::
    
    reading the new user guide :ref:`aetest_index` is the best way to bring
    yourself up-to-date with ``aetest`` changes.

- command line arguments & ``main()`` argument changes. Refer to documentation:
  :ref:`aetest_standard_arguments`.
  
  - all short form cli arguments are removed. (eg, ``-tb``) and standardized 
    to long arguments
  
  - ``-q/-quiet``, ``-v/-verbose`` have been removed and replaced by 
    ``-loglevel``.
  
  - ``-dependent_subsections`` has been removed. All subsections are now
    independent. Use :ref:`aetest_goto` if necessary.

  - ``-exclude_common_results`` has been removed. ``CommonSetup`` and
    ``CommonCleanup`` now counts as 1 each in the numbers of sections ran. Refer
    to: :ref:`aetest_section_results`.

  - ``-run_ids``, ``-skip_ids`` have been removed and consolidated into ``-ids``

  - ``-execution_groups`` has been renamed to ``-groups`` and is now a much
    more capable feature.

- data-driven testing support using :ref:`test_parameters`. This is a completely
  new feature. Allows for parameter propagation, function argument calling and
  more.

  - phasing out ``self.script_args`` usage in favor of test parameters. Defined
    a new set of script parameter/section parameter relationships

  - support for parameter relationships, parameters overwrite, dynamic and/or
    callable parameters.

- section :ref:`aetest_processors` support. This is a brand new feature.

  - support for running functions before & after each test section

  - support for dynamic section markings

- section looping features is significantly updated. Refer to 
  :ref:`aetest_looping` documentation for details.

  - removed ``variant=`` support. replaced with auto generation of section id
    using loop parameters

  - support for loop parametrization & passing loop parameters to test functions
    via function arguments.

  - support for arbitrary loop arguments

  - support for generators

  - support for dynamic section loop markings

- redesigned test script :ref:`aetest_control`.
    
  - consolidated ``-run_ids``, ``-skip_ids`` into ``-ids``, supporting callables
    and leveraging :ref:`logic_tests`.

  - redesigned ``-execution_groups`` to ``-groups``, supporting callables and
    leveraging :ref:`logic_tests`.

  - revamped & tidy'ed up :ref:`aetest_goto` logic. Goto signals for 
    ``Subtest`` features have been removed.
  
  - added new ``skip``, ``skipIf``, ``skipUnless`` decorators. See
    :ref:`aetest_skip_conditions`.

- simplified :ref:`aetest_steps` support.

  - removed ``steps.getChild()`` api call. Step objects can now create new 
    steps directly.

  - added step error, exception and signal handling.

  - new ``Step``/``Steps`` classe & documentation.

  - ``step.start()`` argument ``continueOnFail`` is now renamed to 
    ``continue_``.

- phasing out (obsoleting) ``Subtest`` altogether. Subtests adds more headaches 
  than their worth. With multiple tests within each testcase and finer steps
  breakdown, Subtests (class within class) are being phase out for good.

  - most subtest features/scripts will continue to work, but a large warning
    will be printed into your log. 

  - migrate all your testscripts from subtests to tests and/or steps.

- ``CommonVerify`` section has been completely removed. This section was useless
  with the introduction of subsections.

  - merge your subsections into ``CommonSetup`` instead. 

Clean Changes
^^^^^^^^^^^^^

- Clean parameter file format has been changed to YAML. Please go thrugh the 
  clean module documentation for more details.
  
- CLI option to invoke a clean with easypy 
  - easypy -clean_file <clean_file.yaml> -testbed_file <topology file> <jobfile>


Connections enhancements
^^^^^^^^^^^^^^^^^^^^^^^^

- New APIs added to enable and disable device prompt check.

  - ``-enable_prompt_check("exec/config")``

  - ``-disable_prompt_check("exec/config")``

- connection classes ``.is_connected()`` function is now ``.connected`` 
  property.

Misc Changes
^^^^^^^^^^^^

- Install script updates:

  - changed all arguments to ``--`` style. All ``-`` short forms have
    been removed.

  - added checks for install directory being valid and writable

  - now only installed ``ats`` package. All other PyPI packages should be
    installed automatically as dependencies.

- ``atslog.banner`` has new functionalities. See :ref:`log-banner`

- ``results`` module objects have been renamed from all CAPS to Capitalized to
  be more inline with PEP8.

  .. code-block:: python

      # Example
      # -------
      #
      #   result code object name change

      # old imports and name
      from ats.results import (PASSED, FAILED, ABORTED, ERRORED,
                               SKIPPED, BLOCKED, PASSX)

      # new names and imports
      from ats.results import (Passed, Failed, Aborted, Errored,
                               Skipped, Blocked, Passx)

- ``results`` module objects now has a few more perks:

  - ``.tims`` returning the tims equivalent result code

  - supports ``sum()`` calls for easier rollups, along with reverse add support.

  - anything rolled up with ``Aborted`` now results in ``Aborted``.

- new ``datastructures.logic`` module, handling boolean logic such as ``And``, 
  ``Or``, ``Not``.



.. figure:: wall_of_text.png
    :align: center
    
    *Exception: wall of text crits your testscript for over 9000.*
