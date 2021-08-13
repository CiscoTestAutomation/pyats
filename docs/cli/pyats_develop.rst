pyats develop
=============

The process of cloning pyATS repositories and putting pyATS packages into 
development mode can be repetitive and time consuming, especially when working 
with many packages. This is where the `pyats develop` command comes in. This 
command is your one-stop-shop for not only cloning pyATS repositories, but for 
putting them into development mode too. List the packages you want, set the 
options you'd like, (maybe go make yourself a cup of tea/coffee/cocoa) and let 
`pyats develop` handle the rest. 

The `pyats develop` helper command is designed to ease and expedite the process 
of cloning pyATS package repositories and putting each of those packages into 
development mode. It checks that all of your pyATS packages are up-to-date, 
downloads packages (if necessary), puts packages into development 
mode, and then another check that packages in development mode are up-to-date.

.. note::

  This commands requires a Github SSH key to be set up if internal Cisco 
  repositories are to be cloned.

.. code-block:: text

    Usage:
      pyats develop [packages...] [options]
    
    Usage Examples:
      pyats develop all
      pyats develop genie.libs.sdk --skip-version-check
      pyats develop genie.libs.parser genie.trafficgen --external
      pyats develop unicon.plugins genie.libs --delete-repos --directory my_repos
      pyats develop pyats.config --clone-only
    
    Description:
      Puts listed pyATS packages into development mode. Listed packages will have 
      their repositories downloaded from Github if required and 'make develop' will be 
      run for each package. By default, internal Cisco repos will be cloned if the 
      pyATS installation is internal, otherwise external repos will be cloned instead. 
      Github SSH keys are required to clone internal Cisco packages.
    
    Develop Options:
      packages              Packages to put into development mode. Available choices: all, cisco-
                            distutils, genie, genie.libs, genie.libs.clean, genie.libs.conf,
                            genie.libs.filetransferutils, genie.libs.health, genie.libs.ops,
                            genie.libs.robot, genie.libs.sdk, genie.libs.parser, genie.telemetry,
                            genie.trafficgen, pyats, pyats.contrib, rest.connector, unicon,
                            unicon.plugins, yang.connector
      -e, --external        Clone external public repositories instead of internal. Only applicable to
                            internal Cisco pyATS installations. For external pyATS Installations,
                            external public repositories will always be used (Optional)
      -d, --directory DIRECTORY
                            Absolute or relative path of directory to clone repositories into. If not
                            supplied, then the default directory is $VIRTUAL_ENV/pypi (Optional)
      -f, --force-develop   Run 'make develop' even if packages are already in development mode
                            (Optional)
      -s, --skip-version-check
                            Do not check if pyATS packages are up to date before tool execution.
                            WARNING: Using this option may lead to pyATS package version conflicts which
                            could result in a corrupted pyATS installation! Use with discretion
                            (Optional)
      --delete-repos        Delete existing repositories within directory before cloning new ones
                            (Optional) IMPORTANT: Please back up your work before using this option!
      -c, --clone-only      Clone the repositories, but do not put any packages into development mode
                            (Optional)
    
    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels




Options
-------

``packages``
    A space-separated list of packages to put into development mode. Packages 
    must be listed by their package name and not by their repository name. The 
    two exceptions to this rule are 'all' and 'genie.libs'. Using 'all' will 
    expand the list to all available packages. Using 'genie.libs' will expand 
    the list to include genie.libs.clean, genie.libs.conf, 
    genie.libs.filetransferutils, genie.libs.health, genie.libs.ops, 
    genie.libs.robot, and genie.libs.sdk.  

    Packages repositories will be cloned if they do not exist in the default 
    (or specified) directory.

``-e, --external``
    If you have an internal Cisco version of pyATS installed, then this tool 
    will automatically clone internal pyATS repositories. If you have an 
    external/public version of pyATS installed, then this tool will 
    automatically clone external/public pyATS repositories. Use this flag if 
    you have an internal version of pyATS and would like to have external 
    packages be put into development mode instead. Only applicable to internal 
    Cisco pyATS installations.

``-d, --directory``
    By default, repositories will be cloned `$VIRTUAL_ENV/pypi`. Use 
    this argument to override the default behaviour and allow for a different 
    directory to be used instead. This tool does not keep a history of where 
    packages have been cloned, so this argument will have to be used whenever 
    packages have been cloned into a non-default directory.
    
    This argument can be combined with the ``--force-develop`` argument to help 
    when switching between multiple local repositories of the same package. 

``-f, --force-develop``
    By default, if a package is already in development mode, then the command to 
    put it into development mode will not be executed. Use this flag to execute 
    that command even if the package is already in development mode. Useful for 
    swicthing from an internal package to an external one or vice versa.

``-s, --skip-version-check``
    By default, this command will run the `pyats version check` command before 
    execution. Use this flag to skip the version check.

``--delete-repos``
    Please use this flag with caution. The default behaviour of this tool is to 
    use any pre-existing package repositories that are found within the used 
    directory (see above `--directory` argument). Using this flag will cause those 
    repositories to be deleted and then cloned. This can be a useful option when 
    you want to ensure packages are clean and up to date, but please, make sure 
    your work has been backed up before using this option.

``-c, --clone-only``
    Use this flag to only clone a package repository and not put that package 
    into development mode. 
