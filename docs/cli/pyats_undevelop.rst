pyats undevelop
===============

Almost all pyATS package repositories come with a `make undevelop` command 
which removes a package from development mode, effectively uninstalling it. 
While this command is useful, it doesn't go the extra mile of reinstalling 
the uninstalled packages afterwards, often resulting in a non-funtional 
pyATS installation. This is where the `pyats undevelop` command comes in.

The `pyats undevelop` helper command is designed to ease and expedite 
the process of removing pyATS packages from development mode. It checks that 
all of your pyATS packages are up-to-date, removes specified packages from 
development mode, and then reinstalls the most up-to-date version of those 
packages using pip. No need to run each of these commands manually anymore.

.. code-block:: text

    Usage:
      pyats undevelop [packages...] [options]
    
    Usage Examples:
      pyats undevelop all
      pyats undevelop genie.libs.sdk --skip-version-check
      pyats undevelop genie.libs.parser genie.trafficgen --external
      pyats undevelop genie.libs unicon.plugins
    
    Description:
      Removes listed pyATS packages from development mode. Each listed package is 
      removed from development mode with 'make undevelop' and then is reinstalled 
      using 'pip install <package>'. Internal Cisco packages will be reinstalled if 
      the pyATS installation is internal, otherwise external packages will be 
      reinstalled instead.
    
    Undevelop Options:
      packages              Packages to remove from development mode. Available choices: all, cisco-
                            distutils, genie, genie.libs, genie.libs.clean, genie.libs.conf,
                            genie.libs.filetransferutils, genie.libs.health, genie.libs.ops,
                            genie.libs.robot, genie.libs.sdk, genie.libs.parser, genie.telemetry,
                            genie.trafficgen, pyats, pyats.contrib, rest.connector, unicon,
                            unicon.plugins, yang.connector
      -s, --skip-version-check
                            Do not check if pyATS packages are up to date before tool execution.
                            WARNING: Using this option may lead to pyATS package version conflicts which
                            could result in a corrupted pyATS installation! Use with discretion
                            (Optional)
      -e, --external        Reinstall external public pip packages instead of internal. Only applicable
                            to internal Cisco pyATS installations. For external pyATS Installations,
                            external public pip packages will always be used (Optional)
    
    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels


Options
-------

``packages``
    A space-separated list of packages to remove from development mode. Packages 
    must be listed by their package name and not by their repository name. The 
    two exceptions to this rule are 'all' and 'genie.libs'. Using 'all' will 
    expand the list to all available packages. Using 'genie.libs' will expand 
    the list to include genie.libs.clean, genie.libs.conf, 
    genie.libs.filetransferutils, genie.libs.health, genie.libs.ops, 
    genie.libs.robot, and genie.libs.sdk.  

    Packages will be reinstalled using `pip install <package>` after being 
    removed from development mode. The most up-to-date version of a package 
    will be reinstalled. 

``-s, --skip-version-check``
    By default, this command will run the `pyats version check` command before 
    execution. Use this flag to skip the version check.

``-e, --external``
    If you have an internal Cisco version of pyATS installed, then this tool 
    will automatically reinstall internal pip packages. If you have an 
    external/public version of pyATS installed, then this tool will 
    automatically reinstall external/public pip packages. Use this flag if 
    you have an internal version of pyATS and would like to have external 
    pip packages be reinstalled instead. Only applicable to internal 
    Cisco pyATS installations.
