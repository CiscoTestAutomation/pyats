.. _aetest_datafile:

Datafile Inputs
===============

.. sidebar:: Helpful Reading

    - `YAML`_

    - `PyYAML`_

.. _YAML: http://www.yaml.org/
.. _PyYAML: http://pyyaml.org/wiki/PyYAMLDocumentation

Whilst all your testcases, sections, data & AEtest features can be coded, set &
leveraged directly within your testscript, altering their values between runs
(aside from dynamic parameters and script arguments) require physical
script changes, which may not always be desirable.

The **datafile** feature in AEtest allows users to run their testscript with
an additional YAML_ based input file, allowing dynamic updates and/or overwrites
to the current test script module with more information. It is an optional
augmentation to regular script runs, allowing users to easily change script
values and various features without modifying the original testscript.


Usages & Behavior
-----------------

To leverage this feature, run your testscript and provide the ``datafile``
:ref:`aetest_standard_arguments` with full path/name to a YAML data file
written in accordance to the :ref:`aetest_datafile_schema` below.

.. code-block:: python

    # Example
    # -------
    #
    #   example usages of datafile input
    #   (pseudo-code, snippet)

    # as a standalone run argument
    if __name__ == '__main__':
        aetest.main(datafile = '/path/to/your/datafile.yaml')

    # through jobfile run/Task argument
    def main():
        run(script, datafile = '/path/to/your/datafile.yaml')

    # as command-line argument
    # python script.py -datafile=/path/to/your/datafile.yaml

Once loaded, the content of this YAML file is then used to dynamically update
your testscript objects. The following describes this behavior:

- The content of this datafile updates the script's **module** and **classes**
  directly, after the script is imported, before execution starts.

- Only **module & classes** level attributes and features may be provided via
  the datafile (eg, ``CommonSetup``, ``Testcases``, ``CommonCleanup``). Function
  based sections such as ``test``, ``subsection`` etc are not affected.

- Testcases & common sections defined in the datafile **must** each match up to
  a corresponding class: ``common_setup:`` and ``common_cleanup:`` to script's
  unique ``CommonSetup`` and ``CommonCleanup`` subclasses; testcases block's
  ``classname:`` to the actual testcase class definition name.

- If a testcase is looping (using :ref:`aetest_looping` feature), the base class
  definition that is being looped is updated. Datafiles cannot assign
  and/or remove testcase loop feature: it may only update the base class's
  attributes & parameters.

- Only a single datafile may be provided. However, each datafile may extend
  one or more datafiles, creating a chaining relationship effect. When a
  datafile extends another datafile, the other datafile forms the basis,
  and contents of the current datafile is then applied on top using *recursive
  dictionary update.*

- :ref:`test_parameters` provided via the various ``parameters:`` block in the
  YAML file are **updated** into corresponding section's base parameters
  using ``dict.update()`` mechanism.

- all other key/value pairs, including :ref:`aetest_processors` provided via
  the various ``processors:`` block in the YAML file **replace** any
  existing values & settings.

.. tip::

    to better understand this feature, see the datafile example script
    provided in `GitHub example repository<https://github.com/CiscoTestAutomation/examples/tree/master/datafiles>`_.

.. hint::

    as YAML naturally loads in Python nested dictionaries, it is possible to
    provide a dictionary that respects the :ref:`aetest_datafile_schema` instead
    of an input file. However, this only works for job file execution and/or
    standalone execution through ``aetest.main()``, and does not work over the
    command line.


.. _aetest_datafile_schema:

Datafile Schema
---------------

The input datafile must satisfy the following schema. Do not be discouraged by
this long structure: most likely you will only need few of these fields. Beware
of YAML's sensitivity to indentation and whitespaces.

.. code-block:: yaml

    # Datafile Schema
    # ---------------

    extends:    # Datafile(s) to extend/build on.
                # Use this field to extend an existing datafile.
                # Allows datafiles to be chained together in extension
                # relationships.
                # Supports full path/names or name of file in the same dir.
                # The content of the last file on the list forms the base and
                # is updated with the preceding file, and so on,
                # until the existing file content is updated last.
                # (optional)

    parameters:   # testscript parameters
                  # all key/values here becomes the testscript's base parameters
                  # (optional)

    processors:   # global processors
                  # pre/post processors to be used as part of this script run
                  # (optional)

        pre:      # list of global pre-processors
                  #   eg: mylib.mymodule.preprocessor_func
                  #
                  # or, list of global pre-processors with arguments
                  #   eg: - processor: mylib.mymodule.preprocessor_func
                  #         args: <list of positional arguments>
                  #         kwargs:
                  #           <key>: <value>
                  # (optional)


        post:     # list of global post-processors
                  #   eg: mylib.mymodule.postprocessor_func
                  #
                  # or, list of global post-processors with arguments
                  #   eg: - processor: mylib.mymodule.postprocessor_func
                  #         args: <list of positional arguments>
                  #         kwargs:
                  #           <key>: <value>
                  # (optional)

    common_setup:   # common_setup block
                    # everything related to script's common_setup section
                    # (optional)

        parameters:   # common_setup parameters
                      # key/values becomes parameters belonging to common_setup
                      # section.
                      # (optional)

        processors:   # common_setup local processors
                      # pre/post processors to be used on common_setup
                      # (optional)

            pre:      # list of pre-processors for common_setup section
                      #   eg: mylib.mymodule.preprocessor_func
                      #
                      # or, list of common_setup pre-processors with arguments
                      #   eg: - processor: mylib.mymodule.preprocessor_func
                      #         args: <list of positional arguments>
                      #         kwargs:
                      #           <key>: <value>
                      # (optional)

            post:     # list of post-processors for common_setup section
                      #   eg: mylib.mymodule.postprocessor_func
                      #
                      # or, list of common_setup post-processors with arguments
                      #   eg: - processor: mylib.mymodule.postprocessor_func
                      #         args: <list of positional arguments>
                      #         kwargs:
                      #           <key>: <value>
                      # (optional)

        # any custom key/value pairs to be set as data (attributes) to
        # your script's common_setup section
        <key>: <value>

    testcases:      # testcases block
                    # all testcase related info gets defined under here
                    # (optional)

        <name>:     # testcase class name
                    # this needs to match the testcase's class definition.
                    # do not confuse with the testcase's uid
                    #   eg: MyTestcase
                    # (mandatory)

            uid:    # testcase's string uid
                    # use this to alter the testcase's reported uid
                    # (optional)

            groups:     # testcase grouping
                        # list of groups this testcase belongs to. See testcase
                        # grouping feature under flow control documentation.
                        # (optional)

            name:       # testcase name
                        # define a testcase's descriptive name. Use this to
                        # give your testcase a more descriptive name
                        # (useful only when run in Easypy mode)
                        # (optional)

            description:    # testcase description
                            # string describing what this testcase does
                            # (optional)

            processors:   # testcase's local processors
                          # pre/post processors to be used in this testcase
                          # (optional)

                pre:      # list of pre-processors for this testcase
                          #   eg: mylib.mymodule.preprocessor_func
                          #
                          # or, list of testcase pre-processors with arguments
                          #   eg: - processor: mylib.mymodule.preprocessor_func
                          #         args: <list of positional arguments>
                          #         kwargs:
                          #           <key>: <value>
                          # (optional)

                post:     # list of post-processors for this testcase
                          #   eg: mylib.mymodule.postprocessor_func
                          #
                          # or, list of testcase post-processors with arguments
                          #   eg: - processor: mylib.mymodule.postprocessor_func
                          #         args: <list of positional arguments>
                          #         kwargs:
                          #           <key>: <value>
                          # (optional)


            # any custom key/value pairs to be set as data (attributes) to
            # this testcase class
            <key>: <value>

    common_cleanup:   # common_cleanup block
                      # everything related to script's common_cleanup section
                      # (optional)

        parameters:   # common_cleanup parameters
                      # key/values becomes parameters belonging to
                      # common_cleanup section.
                      # (optional)

        processors:   # common_cleanup local processors
                      # pre/post processors to be used on common_cleanup
                      # (optional)

            pre:      # list of pre-processors for common_cleanup section
                      #   eg: mylib.mymodule.preprocessor_func
                      #
                      # or, list of common_cleanup pre-processors with args
                      #   eg: - processor: mylib.mymodule.preprocessor_func
                      #         args: <list of positional arguments>
                      #         kwargs:
                      #           <key>: <value>
                      # (optional)

            post:     # list of post-processors for common_cleanup section
                      #   eg: mylib.mymodule.postprocessor_func
                      #
                      # or, list of common_cleanup post-processors with args
                      #   eg: - processor: mylib.mymodule.postprocessor_func
                      #         args: <list of positional arguments>
                      #         kwargs:
                      #           <key>: <value>
                      # (optional)

        # any custom key/value pairs to be set as data (attributes) to
        # your script's common_cleanup section
        <key>: <value>

    # any other key/value pairs to be set as variables/attributes directly
    # into your testscript module
    <key>: <value>


Example Datafile
----------------

.. code-block:: yaml

    # Example
    # -------
    #
    #   the following is an example datafile yaml file

    extends: sanity_data.yaml

    parameters:
        ip_seed: 1.1.1.1
        vlan: 4382
        traffic_streams: 50

    processors:
        pre:
            - cflow.init_instrumentation
            - router_health.reset

        post:
            - cflow.collect_results
            - router_health.collect_health_info

    testcases:
        MyTestcase_One:
            uid: alternative_uid_1
            groups: [sanity, regression, ha]

            parameters:
                input_one: 1000
                input_two: 2000

            expected_routes: 35

        MyTestcase_Two:
            uid: alternative_uid_2
            groups: [sanity, regression, ha, stability]

            parameters:
                input_x: 2000
                input_y: 3000


Example Run
-----------

The following is a short script designed to be run with datafiles. Notice how
many parameters and values are not defined directly in the script.

.. code-block:: python

    # Example
    # -------
    #
    #   short script designed to be run with a datafile
    #   (notice many expected values/parameters undefined)

    import logging

    from pyats import aetest

    logger = logging.getLogger(__name__)

    class MyTestcase(aetest.Testcase):

        @aetest.test
        def uid_and_groups(self):
            logger.info('notice how testcase uid/groups are modified')
            logger.info('  uid = %s' % self.uid)
            logger.info('  groups = %s' % self.groups)

        @aetest.test
        def script_params(self, script_param_a, script_param_b):
            logger.info('the following parameters are script-level')
            logger.info('  script_param_a = %s' % script_param_a)
            logger.info('  script_param_b = %s' % script_param_b)

        @aetest.test
        def testcase_params(self, tc_param_a, tc_param_b):
            logger.info('the following parameters are local to this testcase')
            logger.info('  tc_param_a = %s' % tc_param_a)
            logger.info('  tc_param_b = %s' % tc_param_b)

        @aetest.test
        def module_variables(self):
            logger.info('the following variables are defined at module level')
            logger.info('  module_var_a = %s' % module_var_a)
            logger.info('  module_var_b = %s' % module_var_b)

        @aetest.test
        def class_attributes(self):
            logger.info('the following attributes are defined at class level')
            logger.info('  class_var_a = %s' % self.class_var_a)
            logger.info('  class_var_b = %s' % self.class_var_b)

    if __name__ == '__main__':
        aetest.main()

Let's use the datafile below to provide these much-needed values:

.. code-block:: yaml

    # Example
    # -------
    #
    #   yaml datafile

    module_var_a: some string value
    module_var_b: 99999

    parameters:
        script_param_a: 3.1415926
        script_param_b: 2016-01-01

    testcases:
        MyTestcase:
            uid: customized_uid_from_datafile
            groups: [demo, datafile, awesomeness]

            parameters:
                tc_param_a: 100
                tc_param_b: 200

            class_var_a: [1,2,3,4,5]
            class_var_b: datafile feature is just that awesome

Running the above together, here is the expected output:

.. code-block:: text

    # Example
    # -------
    #
    #   running the above

    (pyats) [tony@jarvis:pyats]$ python testscript.py -datafile=datafile.yaml

    INFO: +------------------------------------------------------------------------------+
    INFO: |                Starting testcase customized_uid_from_datafile                |
    INFO: +------------------------------------------------------------------------------+
    INFO: +------------------------------------------------------------------------------+
    INFO: |                       Starting section uid_and_groups                        |
    INFO: +------------------------------------------------------------------------------+
    INFO: notice how testcase uid/groups are modified
    INFO:   uid = customized_uid_from_datafile
    INFO:   groups = ['demo', 'datafile', 'awesomeness']
    INFO: The result of section uid_and_groups is => PASSED
    INFO: +------------------------------------------------------------------------------+
    INFO: |                        Starting section script_params                        |
    INFO: +------------------------------------------------------------------------------+
    INFO: the following parameters are script-level
    INFO:   script_param_a = 3.1415926
    INFO:   script_param_b = 2016-01-01
    INFO: The result of section script_params is => PASSED
    INFO: +------------------------------------------------------------------------------+
    INFO: |                       Starting section testcase_params                       |
    INFO: +------------------------------------------------------------------------------+
    INFO: the following parameters are local to this testcase
    INFO:   tc_param_a = 100
    INFO:   tc_param_b = 200
    INFO: The result of section testcase_params is => PASSED
    INFO: +------------------------------------------------------------------------------+
    INFO: |                      Starting section module_variables                       |
    INFO: +------------------------------------------------------------------------------+
    INFO: the following variables are defined at module level
    INFO:   module_var_a = some string value
    INFO:   module_var_b = 99999
    INFO: The result of section module_variables is => PASSED
    INFO: +------------------------------------------------------------------------------+
    INFO: |                      Starting section class_attributes                       |
    INFO: +------------------------------------------------------------------------------+
    INFO: the following attributes are defined at class level
    INFO:   class_var_a = [1, 2, 3, 4, 5]
    INFO:   class_var_b = datafile feature is just that awesome
    INFO: The result of section class_attributes is => PASSED
    INFO: The result of testcase customized_uid_from_datafile is => PASSED
    INFO: +------------------------------------------------------------------------------+
    INFO: |                               Detailed Results                               |
    INFO: +------------------------------------------------------------------------------+
    INFO:  SECTIONS/TESTCASES                                                      RESULT
    INFO: --------------------------------------------------------------------------------
    INFO: .
    INFO: `-- customized_uid_from_datafile                                         PASSED
    INFO:     |-- uid_and_groups                                                   PASSED
    INFO:     |-- script_params                                                    PASSED
    INFO:     |-- testcase_params                                                  PASSED
    INFO:     |-- module_variables                                                 PASSED
    INFO:     `-- class_attributes                                                 PASSED
    INFO: +------------------------------------------------------------------------------+
    INFO: |                                   Summary                                    |
    INFO: +------------------------------------------------------------------------------+
    INFO:  Number of ABORTED                                                            0
    INFO:  Number of BLOCKED                                                            0
    INFO:  Number of ERRORED                                                            0
    INFO:  Number of FAILED                                                             0
    INFO:  Number of PASSED                                                             1
    INFO:  Number of PASSX                                                              0
    INFO:  Number of SKIPPED                                                            0
    INFO: --------------------------------------------------------------------------------


