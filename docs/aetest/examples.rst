Examples
========

This section contains a few simple examples aimed towards guiding users on
writing their first ``aetest`` based testscripts.

.. note::

    more elaborate examples can be found in 
    `GitHub example repository <https://github.com/CiscoTestAutomation/examples/>`_.

Hello World
-----------

This is a very simply testscript demonstrating the *hello world* usage of
``aetest``. It contains a single ``Testcase`` with a single ``test``. Keep in
mind that this is the smallest possible testscript, as ``CommonSetup`` and
``CommonCleanup`` are optional sections block.


.. code-block:: python

    # Example
    # -------
    #
    #   hello world

    import logging
    from pyats import aetest

    logger = logging.getLogger(__name__)

    class HelloWorld(aetest.Testcase):

        @aetest.test
        def test(self):
            logger.info('Hello World!')

    # main()
    if __name__ == '__main__':
        # set logger level
        logger.setLevel(logging.INFO)

        aetest.main()

.. tip::

    do not submit to regression: insignificant test coverage

You can save this content to file named ``hello_world.py``, and try to run it
using :ref:`aetest_standalone_execution` method.

.. code-block:: bash

    bash$ python hello_world.py


Script Arguments
----------------

This example focuses on how to use :ref:`script_args` and pass them to your
testscript into parameters, using both :ref:`aetest_standalone_execution` and
:ref:`aetest_jobfile_execution`.

.. code-block:: python

    # Example
    # -------
    #
    #   script arguments demo

    import logging
    from pyats import aetest

    logger = logging.getLogger(__name__)

    class Testcase(aetest.Testcase):

        @aetest.test
        def test(self, testbed, vlan):
            logger.info('Testbed = %s' % testbed)
            logger.info('Vlan =  %s' % vlan)

    # main()
    if __name__ == '__main__':

        # set logger level
        logger.setLevel(logging.INFO)

        # local imports
        import sys
        import argparse
        from pyats.topology import loader

        parser = argparse.ArgumentParser(description = "standalone parser")
        parser.add_argument('--testbed', dest = 'testbed')
        parser.add_argument('--vlan', dest = 'vlan')

        # parse args
        args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

        # post-parsing processing
        testbed = loader.load(args.testbed)
        vlan = int(args.vlan)

        # and pass all arguments to aetest.main() as kwargs
        aetest.main(testbed = testbed, vlan = vlan)

Assuming the above testscript is saved into ``script_argument_demo.py``, then
when running under standalone execution, make sure to pass in both ``--testbed``
and ``--vlan`` arguments:

.. code-block:: bash

    bash$ python script_argument_demo.py --testbed /path/to/my/testbed.yaml --vlan 50


To run under Easypy, a job file needs to be created for it:

.. code-block:: python

    # Example
    # -------
    #
    #   job file demonstrating passing script arguments to testscripts

    from pyats.easypy import run

    # job file requires a main block
    def main():

        run('script_argument_demo.py', vlan = 50)

Keep in mind that during :ref:`aetest_jobfile_execution`, the ``testbed``
argument is automatically passed to the testscript if ``pyats run job`` was run with
the ``--testbed-file`` and/or ``--logical-testbed-file`` arguments.
Thus, save this to ``script_argument_demo_job.py`` file and run it with:

.. code-block:: bash

    bash$ pyats run job script_argument_demo_job.py --testbed-file /path/to/my/testbed.yaml


Feature Usage
-------------

Although loops and :ref:`aetest_control` features can be used (hard-coded)
directly in your main testscript, a good practice to follow is to always:

- develop a *library of testcases*, then

- build and control your testscripts by reference and inheritance.

This allows multiple scripts to share the same basic test code, but be driven by
varying parameters & etc. This also allows users to write testcases, but apply
loops to them as they see fit (in the inherited testcase).

.. code-block:: python

    # Example
    # -------
    #
    #   the base testcase library script (to be inherited by other scripts)
    #   let's call this script: base_script.py

    from pyats import aetest

    class MathTest(aetest.Testcase):

        def test_plus(self):
            '''test requires the definition of a & b at testcase level'''

            assert self.a + self.b < 1000

Note that in the above script, we defined a testcase, but its required values
(``a``/``b``) is not defined - the testcase expects to be inherited from.

.. code-block:: python

    # Example
    # -------
    #
    #   the script that inherits from the base_script and gives it meaning

    from base_script import MathTest

    class RealMathTest(MathTest):

        # provide uid and grouping information
        uid = 'rocket_science_math_test'
        groups = ('elementary', 'basic')

        # give values for the tests
        a = 1
        b = 2

When this testscript is run, it is given a meaningful uid, two unique testcase
groups, and is driven by new data values, all while the content of the
testcase's test remaining the same.

This concept allows testcases to be classified & driven differently dependent on
the actual script usage, and avoids hard-coding data, values and testcase
classifications within a testscript, further avoiding the need to constantly
modify and/or duplicate testscripts.

.. note::

    more elaborate examples can be found in 
    `GitHub example repository <https://github.com/CiscoTestAutomation/examples/>`_.


Mega Looping
------------

The following example is a mega loop script: it demonstrates every possible way
of :ref:`aetest_looping` definitions.

.. code-block:: python

    # Example
    # -------
    #
    #   loop everything!

    import logging
    from pyats import aetest

    logger = logging.getLogger(__name__)

    # static variable
    VLANS = list(range(1, 4096))

    class CommonSetup(aetest.CommonSetup):

        @aetest.subsection
        def check_testbed(self, testbed):
            '''
            checking testbed information
            '''

            logger.info('Testbed = %s' % testbed)
            # do some testbed checking
            # ...

        @aetest.subsection.loop(vlan=VLANS)
        def configure_vlan(self, vlan):
            '''
            configure every vlan, each being a subsection
            '''

            logger.info("configuring vlan: %s" % vlan)
            # do the configuration
            # ...

        # dynamically assign looping of Testcase
        # based on script argument information
        @aetest.subsection
        def mark_testcase_for_looping(self, interfaces):
            '''
            marking testcase for looping based on script argument interfaces
            '''

            aetest.loop.mark(InterfaceFlapping, interface = interfaces)


    class InterfaceFlapping(aetest.Testcase):
        '''
        tests interface flapping, requires parameter 'interface'
        '''

        @aetest.setup
        def setup(self, interface):
            logger.info('testing interface: %s' % interface)

        @aetest.test.loop(status=['up', 'down'])
        def test_status(self, status):
            '''
            check that intf status can be flapped
            '''
            logger.info('configure interface status to: %s' % status)
            # do testing
            # ...

    @aetest.loop(vlan = VLANS)
    class Traffic(aetest.Testcase):
        '''
        send traffic on all vlans on all interfaces
        '''

        @aetest.setup
        def setup(self, interfaces):
            '''
            mark traffic test with looping through interfaces
            '''
            aetest.loop.mark(self.test, interface = interfaces)

        def test(self, interface, vlan):
            '''
            send traffic to vlan + interface
            '''
            logger.info('interface: %s' % interface)
            logger.info('vlan: %s' % vlan)
            # send traffic
            # ...


    class CommonCleanup(aetest.CommonCleanup):

        @aetest.subsection.loop(vlan=VLANS)
        def unconfigure_vlan(self, vlan):
            '''
            unconfigure every vlan, each being a subsection
            '''

            logger.info("configuring vlan: %s" % vlan)
            # do the configuration
            # ...

    # main()
    if __name__ == '__main__':

        # set logger level
        logger.setLevel(logging.INFO)

        # local imports
        import sys
        import argparse
        from pyats.topology import loader

        parser = argparse.ArgumentParser(description = "standalone parser")
        parser.add_argument('--testbed', dest = 'testbed')
        parser.add_argument('--interfaces', dest = 'interfaces')

        # parse args
        args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

        # post-parsing processing
        testbed = loader.load(args.testbed)
        interfaces = args.interfaces.split(',')

        # and pass all arguments to aetest.main() as kwargs
        aetest.main(testbed = testbed, interfaces = interfaces)

Standalone Execution Command:

.. code-block:: bash

    bash$ python mega_looping.py --testbed tb.yaml --interfaces="Ethernet1/1,Ethernet1/2"

To run under Easypy, create the following job file:

.. code-block:: python

    # Example
    # -------
    #
    #   mega looping jobfile

    from pyats.easypy import run

    def main():

        run('mega_looping.py', interfaces=['Ethernet1/1', 'Ethernet1/2'])

And run ``pyats run job``:

.. code-block:: bash

    bash$ pyats run job mega_looping_job.py --testbed-file tb.yaml
