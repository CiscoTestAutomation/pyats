.. _testbench:

Test Bench Development
======================

    *A test bench or testing workbench is a virtual environment used to
    verify the correctness or soundness of a design or model.*

A customized test bench is the best way to approach Python development. Consider
a Python test bench as simply an executable ``.py`` file that loads all the
packages, modules & dependencies and provides a self-sufficient development 
environment, where users can **iteratively** develop and test their code.

In the case of pyATS, a successful test bench should include the following
components:

- import all necessary packages & modules

- testbed devices, and live connections to testbed devices

- interactive development/prompt

- iterative code & test, with the final code pluggable into a deliverable

A successful test bench bridges the gap in between knowing the Python language, 
and designing/writing a first library/testscript in pyATS.


Iterative Development
---------------------

Everyone can elect to write their own code test bench. Here's an idea/template 
that could help you to get started. Keep in mind that the primary goal is to
have something where you can code & test what you've just written without
having to re-run your entire test script, which can be costly when you are 
loading large number of libraries and connecting to multiple devices.


.. code-block:: python

    # Example
    # -------
    #
    #   example test bench (testbench.py)

    #! /bin/env python

    # import any modules/libraries/packages & etc
    import sys
    # ...

    # code here
    # --------------------------------------------------------------------------
    # 
    #   develop your test case, library apis & etc here.
    
    # ...

    # main block to execute the above test code
    # --------------------------------------------------------------------------
    if __name__ == '__main__':

        # setup test bench
        # ----------------
        #   setup your work environment, eg:
        #       - load yaml
        #       - connect to devices
        #       - require necessary tcl packages
        #       - etc

        # ...

        # go interactive
        # --------------
        #   note that there's a few ways to go into interactive:
        #       - using IPython
        #       - using pdb.set_trace()
        #       - using code.interact()

        # uncomment/pick one of these:
        from IPython import embed; embed()
        # import code; code.interact(local = locals())
        # import pdb; pdb.set_trace()
        # import ipdb; ipdb.set_trace()

        # cleanup work bench
        # ------------------
        #   do any necessary cleaning, such as:
        #       - remove lingering configurations
        #       - disconnecting from tb devices
        #       - etc

        # ...

        # exit script
        # -----------
        sys.exit()


        # any code from here onwards is just for your copy/paste purposes
        # ---------------------------------------------------------------
        #   use this space for anything you'd do to copy/paste into your
        #   interactive prompt. 

        # ...


When run, the above test bench code stops after setup and present an
interactive prompt (assuming working with ``testbench.py``). From there onwards,
you can code in the editor, and copy/paste code into the interactive shell and
run it to get quick results.

.. code-block:: text
    
    bash$ python testbench.py

    Python 3.8.2 (default, Apr  8 2020, 11:06:18)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: sys
    Out[1]: <module 'sys' (built-in)>

    In [2]: %cpaste
    Pasting code; enter '--' alone on the line to stop or use Ctrl-D.
    :    
    :def my_test_proc():
    :    print('this is my test proc working')
    :
    :--

    In [3]: my_test_proc()
    this is my test proc working

    In [4]: 

.. note::
    
    using IPython (http://ipython.org/) as an example. IPython is available on
    PyPI and is the most popular interactive python shell.

.. tip::

    IPython ``%cpaste`` functionality copes with copy/paste much better than
    the built-in interactive shell.


Test Bench Example
------------------

Here's a example of writing and executing an ``aetest`` based testcase on the
fly while maintaing a live device connection without disconnecting.

.. code-block:: python
    
    # Example
    # -------
    #
    #   aetest test bench with device connections
    
    # import what's necessary
    import sys
    from pyats import aetest, topology
    from genie.utils import Dq

    # write a testcase here
    # --------------------------------------------------------------------------

    class Testcase(aetest.Testcase):
        '''
        a testcase written in a test bench environment
        '''

        @aetest.setup
        def setup(self, uut, intf = None):

            if intf is None:
                # default to picking the first available interface
                intf = next(iter(uut.interfaces.values()))

            self.intf = intf

        @aetest.test
        def check_version_string_has_iosxe(self, uut):
            version = uut.execute('show version')
            assert 'IOS XE' in version

        @aetest.test
        def interface_can_be_configured(self, uut):
            # interface is assumed down, configure it
            uut.configure('''
                interface %s
                    ip address 1.1.1.1 255.255.255.0
                    no shutdown
            ''' % self.intf.name)

            # get the interface information from router_show
            result = uut.parse('show interfaces %s' % self.intf.name)

            # check that the status is reflected 
            assert Dq(result).get_values('enabled') == [True]
            assert Dq(result).get_values('ip') == ['1.1.1.1']

        @aetest.test
        def hostname_can_be_changed(self, uut):
            # configure hostname
            uut.configure('hostname %s' % uut.name)

            config = uut.execute('show running-config | include hostname')

            assert uut.name in config

            
    # run test code
    # --------------------------------------------------------------------------
    if __name__ == '__main__':

        # load testbed from yaml file &
        # grab a device by its alias (uut) for testing
        testbed = topology.loader.load('/path/to/testbed.yaml')
        uut = testbed.devices['uut']

        # connect to the device
        uut.connect()

        # go interactive, do whatever
        from IPython import embed; embed()
        
        # exit
        sys.exit()

        # copy paste code from here onwards..
        # -----------------------------------

        # create a testcase instance from the above code
        tc = Testcase()

        # run the testcase by calling it and providing it with
        # necessary parameters (in this case uut)
        # the result is printed to screen
        tc(uut = uut)

        # --------------------- BACKUP CODE ---------------------

        # Manually Creating Objects
        # -------------------------
        # note that alternatively, instead of loading from YAML, you may also
        # elect to create device and interface objects manually. this avoids the
        # usage of a testbed input file.

        # create a uut device
        uut = topology.Device(name = 'iol',
                              type = 'iol',
                              connections = {
                                 'a': {'protocol': 'telnet',
                                                   'ip': '1.2.3.4',
                                                   'port': 10000}
                              },
                              credentials = {
                                  'default' : {'username': 'admin',
                                               'password': 'adminpw'},
                                  'enable' : {'password': 'lab'},
                              })

        # add an interface to it
        uut.add_interface(topology.Interface(name = 'Ethernet1/1',
                                             type = 'Ethernet'))

Here's what the shortest YAML testbed file would look like (with a single 
interface):

.. code-block:: yaml

    # Example
    # -------
    #
    #   testbench YAML testbed file

    devices:
        device_name:                            # use actual device name here
            type: "device_type"
            alias: "alias of device"            # optional
            connections:
              a:                                # define a single connection
                protocol: "telnet"
                ip: 1.1.1.1
                port: 8888

    topology:
        device_name:                            # use actual device name here
            interfaces:
                Ethernet1/1:                    # define a single interface
                    alias: "test_intf"          # optional
                    type: "ethernet"


The execution of the above code looks like this:

.. code-block:: text

    (pyats) [tony@jarvis pyats]$ python testbench.py 

    ... initial connection output ...

    Python 3.8.2 (default, Apr  8 2020, 11:06:18)
    Type 'copyright', 'credits' or 'license' for more information
    IPython 7.13.0 -- An enhanced Interactive Python. Type '?' for help.

    In [1]: tc = Testcase()

    In [2]: tc()

    ... output of the actual testing ...

    Out[2]: Passed

    In [3]: 

And ... the testcase passed. 

Notice that within this bench environment, you can simply instantiate a Testcase
object ``tc = Testcase()``, and run it by calling that instance ``tc()`` and
passing it any testcase parameters it requires. This, combined with ``%cpaste``
copy/pasting functionality, enables users to get immediate feedback of the code 
(in this case, a ``Testcase``) that's just been written, by simply treating them
as callable class instances.

.. tip::
    
    this is a method of development. the concept also extends to other test 
    script sections, as well as the development of libraries & packages.

.. tip::

    use the python debugger (``pdb``) when encountering issues.

.. tip::

    use Ctrl-D to exit
