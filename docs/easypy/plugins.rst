.. _easypy_plugin:

Plugin System
=============

Easypy is designed around a modular plugin-based architecture. The end goal
is to allow maximum developer configurability & extendability without
sacrificing overall structure, flow and code-base integrity.

.. note::

    Easypy plugins are not for the faint of heart: it is intended for advanced
    developers to provide optional *pluggable* Easypy features for other
    developers to use.


Concept & Rules
---------------

Plugins offers *optional* functionalities that may be added to Easypy. Each
plugin must be configured first via a configuration YAML file before they can
be loaded, instantiated and run at various stages of execution.

All plugins must obey the following rules of development:

- plugins may be configured globally (for all runs in this pyATS instance) by
  creating a  ``easypy_config.yaml`` in the root pyATS installation folder.

- plugins may be configured locally (for this run only) by passing in a config
  YAML via a command-line argument called ``--configuration``.

- plugins may also be configured by setting the environment variable as shown 
  below ``export PYATS_CONFIGURATION_EASYPY=path/to/easypy_config.yaml``

- plugins shall be independent from all other plugins & test scripts.

- plugins must inherit from ``easypy.plugins.bases.BasePlugin`` class

- plugins may contain its own argument parser. Such parsers shall follow the
  :ref:`easypy_argument_propagation` scheme, and shall not contain positional
  arguments.

- plugins may modify ``easypy.runtime`` attributes, but it is the responsibility
  of the plugin owner to diagnose and support any failures due to such changes.

- plugins may self-disable during any point of execution by setting
  ``self.disable = True``. This will remove it from execution stack.

There are four available stages where plugins may run its actions, and each
plugin may choose to run its actions in any or all of these available stages.

.. csv-table:: Easypy Plugin Stages
    :header: Stage, Description

    ``pre_job``, "run before the jobfile starts"
    ``pre_task``, "run before the start of each :ref:`Task<easypy_tasks>`, within the
    task process"
    ``post_task``, "run after the finish of each :ref:`Task<easypy_tasks>`, within
    the task process"
    ``post_job``, "run after the jobfile finishes"

During ``pre_job`` and ``pre_task`` stages, plugins are run in the same sequence
as they appear in the ``order`` definition section of the easypy configuration
YAML file. During ``post_task`` and ``post_job`` stages, plugins are
run in exactly the same but reverse order.


Creating Plugins
----------------

To create a plugin, simply subclass ``easypy.plugins.bases.BasePlugin`` class
and define the stages where your plugin needs to run.

.. code-block:: python

    # Example
    # --------
    #
    #   hello-world plugin

    import logging
    import argparse
    import datetime

    from pyats.easypy.plugins.bases import BasePlugin

    logger = logging.getLogger(__name__)

    class HelloWorldPlugin(BasePlugin):
        '''HelloWorld Plugin

        Runs before and after each job and task, saluting the world and printing
        out the job/task runtime if a custom flag is used.
        '''

        # each plugin may have a unique name
        # set it by setting the 'name' class variable.
        # (defaults to the current class name)
        name = 'HelloWorld'

        # each plugin may have a parser to parse its own command line arguments.
        # these parsers are expected to add arguments to the main easypy parser
        @classmethod
        def configure_parser(cls, parser, legacy_cli = False):
            '''
            plugin parser configurations

            Arguments
            ---------
                parser: main program parser to update
                legacy_cli: boolean indicating whether to support legacy args or
                            not
            '''
            # always create a plugin's own parser group
            hello_world_grp = parser.add_argument_group("My Hello World")

            # custom arguments shall always use -- as prefix
            # positional custom arguments are NOT allowed.
            hello_world_grp.add_argument('--print-timestamp',
                                         action = 'store_true',
                                         default = False)

        # plugins may define its own class constructor __init__, though, it
        # must respect the parent __init__, so super() needs to be called.
        # any additional arguments defined in the plugin config file would be
        # passed to here as keyword arguments
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        # define your plugin's stage actions as methods
        # as this plugin should run pre and post job
        # we need to deifne 'pre_job' and 'post_job' methods.

        # define the pre-job action
        # if 'job' is specified as a function argument, the current Job
        # object is provided as input to this action method when called
        def pre_job(self, job):

            # plugin parser results are stored under self.runtime.args
            if self.runtime.args.print_timestamp:
                self.job_start = datetime.datetime.now()
                logger.info('Current time is: %s' % self.job_start)

            logger.info('Pre-Job %s: Hello World!' % job.name)

        # define post_job action
        def post_job(self, job):

            if self.runtime.args.print_timestamp:
                self.job_end = datetime.datetime.now()
                logger.info('Job run took: %s' % self.job_end - self.job_start)

            logger.info('Post-Job %s: Hello World!' % job.name)

        # similarly, with pre and post-task methods
        # if a 'task' argument is specified as a function argument, the current
        # Task object is provided as input to this action method on call.
        def pre_task(self, task):
            if self.runtime.args.print_timestamp:
                self.task_start = datetime.datetime.now()
                logger.info('Current time is: %s' % self.task_start)

            logger.info('Pre-Task %s: Hello World!' % task.taskid)

        def post_task(self, task):
            if self.runtime.args.print_timestamp:
                self.task_end = datetime.datetime.now()
                logger.info('Task run took: %s' %
                            self.task_end - self.task_start)

            logger.info('Post-Task %s: Hello World!' % task.taskid)

.. note::

    It is possible to retrieve the full results of a job run from a plugin
    post-job method. ``self.runtime.details()`` will retrieve the full suite of
    test results from the reporter. The attributes follow the same values as
    the YAML file, which can be seen in the :ref:`reporter` section.

After defining a plugin class, it needs to be configured in order to run. The
``easypy`` plugin manager automatically reads plugin configurations from a YAML
file, ``easypy_config.yaml``, located under top level folder of pyats instance
or the file path can be provided with ``--configuration`` parameter.

.. code-block:: yaml

    # Example
    # -------
    #
    #   example easypy configuration file for plugins

    plugins:                   # top level key for plugins

        HelloWorldPlugin:   # this is the plugin name we defined
                            # enabled, module and order keys are
                            # mandatory. Any additional key/values are
                            # used as arguments to the plugin class
                            # constructor.

          enabled: True           # flag marking it as "enabled"
                                  # set to False to disable a plugin

          module: module.where.plugin.is.defined      # module path where this
                                                      # plugin can be imported

          order: 1.0                # defines the order of execution of plugins
                                    # it's just a number that allows users to
                                    # specify plugin order.
                                    # - smaller numbers runs first

And ``easypy`` automatically discovers, loads your plugin, and runs its
actions as part of its standard execution stage.


Plugin Errors
-------------

Because plugins are a fundamental building block of Easypy, any unhandled
exceptions raised from plugin actions result in catastrophic failures:
make **double sure** that your plugin is well tested and robust against all
possible environments and outcomes.  Please also see :ref:`easypy_return_codes`.

By default, all plugin errors are automatically caught and handled by
``BasePlugin.error_handler()`` method, which registers the error and prevent
the system from crashing. Plugin developers may overwrite this method to
develop custom error handling schemes.

When a plugin registers an exception during a **pre_job** stage:

    - the job file will not be run
    - all plugins that ran up until the errored plugin will be run in the
      reverse order, calling the corresponding **post_job** stage for cleaning
      up.

When a plugin registers and exception during a **pre_task** stage:

    - this current task will not be run
    - all plugins that ran up until the errored plugin will be run in the
      reverse order, calling the corresponding **post_task** stage for cleaning
      up.

Whenever plugins error out, your email report will contain the detailed
exception.

Runtime Plugin Disable
----------------------

By default, if a plugin is enabled in the configuration YAML file, it will be
loaded and run. However, if ever there is a need to disable a loaded plugin from
running again - you can do so by settings its attribute ``enabled`` to
``False``.

.. code-block:: python

    # Example
    # -------
    #
    #   a plugin that disables it self when pre_job is run

    class MyControlPlugin(BasePlugin):

        def pre_job(self):
            self.enabled = False
            return

        # from here onwards, the plugin's various stages
        # will no longer be run.

Custom Plugin Entrypoints
-------------------------

Easypy can also automatically run any customized user-developed plugins that
are installed within the same python virtual environment, even if they aren't
explicitly specified in the easypy plugin configuration YAML file. Simply ensure
that the custom user-developed plugin package is registered with and advertises
entrypoint ``pyats.easypy.plugins`` within the package's setup.py file. This
will allow the Easypy plugin manager to find and execute the plugin.

.. sidebar:: Useful Reading

    - `Entry Points`_

.. _Entry Points: https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points

Loading the entrypoint should provide a Python dictionary that contains all the
necessary information of the easypy plugin including the plugin name, class,
module, etc. as defined in the example below.

.. code-block:: python

    # Easypy plugin dict for user-developed plugin
    custom_plugin = {
        'plugins': {
            'CustomPlugin':
                {'class': CustomPlugin,
                'enabled': True,
                'kwargs': {},
                'module': 'custom.plugin',
                'name': 'CustomPlugin',
                },
            },
        }

By default, user-developed plugins that are loaded via entrypoints will be
sorted to execute at the end of the pyATS task and job by the Easypy plugin
manager. Alternatively, user's can specify the order in the plugin dict returned
by loading the entrypoint.
