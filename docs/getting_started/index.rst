Getting Started
===============

pyATS is a foundation-layer test framework. It is designed to provide a
reasonable end-to-end test environment for developers to write test cases in,
featuring multiple packages and modules making writing networking-related
tests a breeze.

The goal of this document is to provide an informal overview of how pyATS
works, and just enough technical specifics to get you started with your first
test project.


Installation
------------

pyATS currently supports Python ``v3.6.x``, ``v3.7.x`` and  ``v3.8.x``, and is
tested to work on the following platforms:

    - Linux (tested with CentOS, RHEL, Ubuntu, Alpine)
    - Mac OSX (10.13+)

.. note::

    **Cisco Internal Engineering**

    For all Cisco engineering users (eg, if you are a Cisco employee), refer to
    installation section of the pyATS Wiki for guidelines on how to install 
    pyATS correctly in your environment.

For all external users (Cisco DevNet users, customers, general public), you can 
install pyATS from public PyPI directly using  `pip install`:

``pip install pyats``
    **core framework only**: this installs just the core pyATS framework with
    zero optional extras.

``pip install pyats[library]``
    **pyATS + pyATS Library/Genie**: this installs the core pyATS framework,
    and the standard pyATS network automation library, 
    `Genie`_.

    *This is the recommended option*

.. _Genie: https://developer.cisco.com/docs/genie-docs/

``pip install pyats[robot]``
    **pyATS framework with RobotFramework support**. This installs the optional
    RobotFramework package, and ``pyats.robot`` package that features pyATS
    specific keywords.

``pip install pyats[template]``
    installs the cookiecutter dependency require for ``pyats create project``
    command

``pip install pyats[full]``
    installs pyATS, along with **all optional extras**.

Describe Your Testbed
---------------------

Because we are in the business of network test automation, pyATS is designed
around the concept of :ref:`testbeds <topology_concept>`: where you describe
your *devices under testing* in `YAML`_ format.

This :ref:`testbed YAML file <topology_testbed_file>` provides many
:ref:`sections <schema>` for you to describe your physical devices, and how they
link together to form the topology.

.. code-block:: yaml

    # Example
    # -------
    #
    #   an example testbed file - ios_testbed.yaml

    testbed:
        name: IOS_Testbed
        credentials:
            default:
                username: admin
                password: cisco
            enable:
                password: cisco

    devices:
        ios-1: # <----- must match to your device hostname in the prompt
            os: ios
            type: ios
            connections:
                a:
                    protocol: telnet
                    ip: 1.1.1.1
                    port: 11023
        ios-2:
            os: ios
            type: ios
            connections:
                a:
                    protocol: telnet
                    ip: 1.1.1.2
                    port: 11024
                vty:
                    protocol: ssh
                    ip: 5.5.5.5
    topology:
        ios-1:
            interfaces:
                GigabitEthernet0/0:
                    ipv4: 10.10.10.1/24
                    ipv6: '10:10:10::1/64'
                    link: link-1
                    type: ethernet
                Loopback0:
                    ipv4: 192.168.0.1/32
                    ipv6: '192::1/128'
                    link: ios1_Loopback0
                    type: loopback
        ios-2:
            interfaces:
                GigabitEthernet0/0:
                    ipv4: 10.10.10.2/24
                    ipv6: '10:10:10::2/64'
                    link: link-1
                    type: ethernet
                Loopback0:
                    ipv4: 192.168.0.2/32
                    ipv6: '192::2/128'
                    link: ios2_Loopback0
                    type: loopback

.. _YAML: http://www.yaml.org/start.html


Connect and Issue Commands
--------------------------

Once a testbed yaml file is written, you can load it, query your topology,
connect & issue commands to your devices using :ref:`the APIs <topology_usage>`.

This is the best way to validate whether your topology file is well formed,
and your devices connectable.

.. code-block:: python

    # loader our newly minted testbed file
    from pyats.topology import loader
    testbed = loader.load('ios_testbed.yaml')

    # access the devices
    testbed.devices
    # AttrDict({'ios-1': <Device ott-tb1-n7k4 at 0xf77190cc>,
    #           'ios-2': <Device ott-tb1-n7k5 at 0xf744e16c>})
    ios_1 = testbed.devices['ios-1']
    ios_2 = testbed.devices['ios-2']

    # find links from one device to another
    for link in ios_1.find_links(ios_2):
        print(repr(link))
    # <Link link-1 at 0xf744ef8c>

    # establish basic connectivity
    ios_1.connect()

    # issue commands
    print(ios_1.execute('show version'))
    ios_1.configure('''
        interface GigabitEthernet0/0
            ip address 10.10.10.1 255.255.255.0
    ''')

    # establish multiple, simultaneous connections
    ios_2.connect(alias = 'console', via = 'a')
    ios_2.connect(alias = 'vty_1', via = 'vty')

    # issue commands through each connection separately
    ios_2.vty_1.execute('show running')
    ios_2.console.execute('reload')

    # creating connection pools
    ios_2.start_pool(alias = 'pool', size = 2)

    # use connection pool in multiprocessing paradigms
    # each process will be allocated a connection - whenever one is available
    def sleep(seconds):
        ios_2.pool.execute('sleep %s' % seconds)
    import multiprocessing
    p1 = multiprocessing.Process(target=sleep, args = (10, ))
    p2 = multiprocessing.Process(target=sleep, args = (10, ))
    p3 = multiprocessing.Process(target=sleep, args = (10, ))
    p1.start(); p2.start(); p3.start()
    p1.join(); p2.join(); p3.join()


Design Your Testscript
----------------------

pyATS is all about testing; and the absolute cornerstone in testing is
the actual testscript. In pyATS, test scripts are written and executed through
:ref:`AEtest Package <aetest_index>`.

Testscripts are :ref:`structured <aetest_script_structure>` Python files that
contains/describes the testing you want to do. A clean, elegant testscript
is scalable, and generates easy-to-read test results and logs.

.. code-block:: python

    # Example
    # -------
    #
    #   connectivity_check.py

    from pyats import aetest

    class CommonSetup(aetest.CommonSetup):

        @aetest.subsection
        def check_topology(self,
                           testbed,
                           ios1_name = 'ios-1',
                           ios2_name = 'ios-2'):
            ios1 = testbed.devices[ios1_name]
            ios2 = testbed.devices[ios2_name]

            # add them to testscript parameters
            self.parent.parameters.update(ios1 = ios1, ios2 = ios2)

            # get corresponding links
            links = ios1.find_links(ios2)

            assert len(links) >= 1, 'require one link between ios1 and ios2'


        @aetest.subsection
        def establish_connections(self, steps, ios1, ios2):
            with steps.start('Connecting to %s' % ios1.name):
                ios1.connect()

            with steps.start('Connecting to %s' % ios2.name):
                ios2.connect()

    @aetest.loop(device=('ios1', 'ios2'))
    class PingTestcase(aetest.Testcase):

        @aetest.test.loop(destination=('10.10.10.1', '10.10.10.2'))
        def ping(self, device, destination):
            try:
                result = self.parameters[device].ping(destination)

            except Exception as e:
                self.failed('Ping {} from device {} failed with error: {}'.format(
                                    destination,
                                    device,
                                    str(e),
                                ),
                            goto = ['exit'])
            else:
                match = re.search(r'Success rate is (?P<rate>\d+) percent', result)
                success_rate = match.group('rate')

                logger.info('Ping {} with success rate of {}%'.format(
                                            destination,
                                            success_rate,
                                        )
                                   )

    class CommonCleanup(aetest.CommonCleanup):

        @aetest.subsection
        def disconnect(self, steps, ios1, ios2):
            with steps.start('Disconnecting from %s' % ios1.name):
                ios1.disconnect()

            with steps.start('Disconnecting from %s' % ios2.name):
                ios2.disconnect()

    if __name__ == '__main__':
        import argparse
        from pyats.topology import loader

        parser = argparse.ArgumentParser()
        parser.add_argument('--testbed', dest = 'testbed',
                            type = loader.load)

        args, unknown = parser.parse_known_args()

        aetest.main(**vars(args))

This example uses Python `argparse`_ to parse command line arguments for a
testbed file input, and passes it to the script as the ``testbed``
:ref:`script parameter <test_parameters>`. This is a good practice to do -
take arguments from command line makes your script more dynamic.

.. _argparse: https://docs.python.org/3/library/argparse.html


Run the Testscript
------------------

With your script written & saved, you can run it from the command line:

.. code-block:: bash

    bash$ python connectivity_check.py --testbed ios_testbed.yaml

The ``if __name__ == '__main__'`` block in your testscript will invoke AEtest
to run the file's content when called from the command line, and when finished,
displays testcase results:

.. code-block:: text

    +------------------------------------------------------------------------------+
    |                               Detailed Results                               |
    +------------------------------------------------------------------------------+
     SECTIONS/TESTCASES                                                      RESULT
    --------------------------------------------------------------------------------
    .
    |-- common_setup                                                         PASSED
    |   |-- check_topology                                                   PASSED
    |   `-- establish_connections                                            PASSED
    |       |-- Step 1: Connecting to ios-1                                  PASSED
    |       `-- Step 2: Connecting to ios-2                                  PASSED
    |-- PingTestcase[device=ios1]                                            PASSED
    |   |-- ping[destination=10.10.10.1]                                     PASSED
    |   `-- ping[destination=10.10.10.2]                                     PASSED
    |-- PingTestcase[device=ios2]                                            PASSED
    |   |-- ping[destination=10.10.10.1]                                     PASSED
    |   `-- ping[destination=10.10.10.2]                                     PASSED
    `-- common_cleanup                                                       PASSED
        `-- disconnect                                                       PASSED
            |-- Step 1: Disconnecting from ios-1                             PASSED
            `-- Step 2: Disconnecting from ios-2                             PASSED
    +------------------------------------------------------------------------------+
    |                                   Summary                                    |
    +------------------------------------------------------------------------------+
     Number of ABORTED                                                            0
     Number of BLOCKED                                                            0
     Number of ERRORED                                                            0
     Number of FAILED                                                             0
     Number of PASSED                                                             4
     Number of PASSX                                                              0
     Number of SKIPPED                                                            0
    --------------------------------------------------------------------------------


This is the quickest way to see your testscript in action: everything is printed
directly to screen, so you can edit, run, edit, and run again until your testing
is tuned to perfection.


Creating a Job
--------------

A :ref:`job <easypy_jobfile>` is a step above simply running testscripts as
an executable and getting output in STDOUT. Job files enables the execution of
testscripts as :ref:`tasks <easypy_tasks>` in standardized runtime environment,
allowing testscripts to run in series or in parallel, and aggregates their logs
and results together into a more manageable format.

In-effect, the engine around job files handle the typical boilerplate
environment-setup, such as loading testbed files, through the use of
:ref:`plugins <easypy_plugin>`.

A job must feature a ``main()`` method - this is entry point.

.. code-block:: python

    # Example: ios_job.py
    # -------------------
    #
    #   a simple job file for the script above

    from pyats.easypy import run

    def main():

        # run api launches a testscript as an individual task.
        run('connectivity_check.py')


To launch a job, use ``pyats``. The built-in testbed file handling plugin
accepts a ``--testbed-file`` argument, which automatically loads and parses the
provided testbed file into ``testbed`` parameter, and provide it to the
testscript. When launched, each testscript called by ``run()`` api inside the
job runs as a child process, and the contents inside its
``if __name__ == '__main__'`` block is ignored. Add the ``--html-logs`` argument
to enable generation of HTML log files - they are easier to read.

.. code-block:: bash

    bash$ pyats run job ios_job.py --testbed-file ios_testbed.yaml --html-logs


.. code-block:: text

    +------------------------------------------------------------------------------+
    |                                Easypy Report                                 |
    +------------------------------------------------------------------------------+
    pyATS Instance   : /path/to/pyats
    Tcl-ATS Tree     :
    Python Version   : cpython-3.4.1 (32bit)
    CLI Arguments    : pyats run job ios_job.py --testbed-file ios_testbed.yaml
    User             : joe
    Host Server      : automation
    Host OS Version  : Red Hat Enterprise Linux Server 6.6 Santiago (x86_64)

    Job Information
        Name         : ios_job
        Start time   : 2018-03-15 00:24:05.847263
        Stop time    : 2018-03-15 00:24:17.066042
        Elapsed time : 0:00:11.218779
        Archive      : archive/18-Mar/ios_job.2018Mar15_00:24:04.zip

    Total Tasks    : 1

    Overall Stats
        Passed     : 4
        Passx      : 0
        Failed     : 0
        Aborted    : 0
        Blocked    : 0
        Skipped    : 0
        Errored    : 0

        TOTAL      : 4

    Success Rate   : 100.00 %

    +------------------------------------------------------------------------------+
    |                             Task Result Summary                              |
    +------------------------------------------------------------------------------+
    Task-1: connectivity_check.commonSetup                                    PASSED
    Task-1: connectivity_check.PingTestcase[device=ios1]                      PASSED
    Task-1: connectivity_check.PingTestcase[device=ios2]                      PASSED
    Task-1: connectivity_check.commonCleanup                                  PASSED

    +------------------------------------------------------------------------------+
    |                             Task Result Details                              |
    +------------------------------------------------------------------------------+
    Task-1: connectivity_check
    |-- common_setup                                                          PASSED
    |   |-- check_topology                                                    PASSED
    |   `-- establish_connections                                             PASSED
    |       |-- Step 1: Connecting to ios-1                                   PASSED
    |       `-- Step 2: Connecting to ios-2                                   PASSED
    |-- PingTestcase[device=ios1]                                             PASSED
    |   |-- ping[destination=10.10.10.1]                                      PASSED
    |   `-- ping[destination=10.10.10.2]                                      PASSED
    |-- PingTestcase[device=ios2]                                             PASSED
    |   |-- ping[destination=10.10.10.1]                                      PASSED
    |   `-- ping[destination=10.10.10.2]                                      PASSED
    `-- common_cleanup                                                        PASSED
        `-- disconnect                                                        PASSED
            |-- Step 1: Disconnecting from ios-1                              PASSED
            `-- Step 2: Disconnecting from ios-2                              PASSED

By default, the results of a job file is an archive: a zipped folder containing
files describing the runtime environment, what was run, result XML files, and
log files - eg, everything that was generated in your job's :ref:`runinfo folder
<easypy_runinfo>`.


Scratching the Surface
----------------------

Congratulation, you now understand the basic building blocks of pyATS: job,
script, and testbed files. Aside from the above, there are tons more features
in pyATS left for you to explore. Checkout the rest of the documentation for
all the other awesome features that can help you with your day-to-day testing!


Example
-------

Various pyATS script examples can be found in GitHub:

- **Feature Usage**: https://github.com/CiscoTestAutomation/examples

- **Solutions and Scripts**: https://github.com/CiscoTestAutomation/solutions_examples

Feel free to clone them into your workspace and run.

.. code-block:: bash

    # Example
    # -------
    #
    #   launching pyats from the command line

    # activating pyats instance
    # (if you have not yet activated)
    [tony@jarvis:~]$ cd /ws/tony-stark/pyats
    [tony@jarvis:pyats]$ source env.sh

    # clone example folder
    (pyats) [tony@jarvis:pyats]$ git clone https://github.com/CiscoTestAutomation/examples
    (pyats) [tony@jarvis:pyats]$ cd examples

    # start with executing the basic examples jobfiles.
    # this is a basic example demonstrating the usage of a jobfiles,
    # and running through a single aetest testscript.
    (pyats) [tony@jarvis:examples]$ pyats run job basic/basic_example_job.py
