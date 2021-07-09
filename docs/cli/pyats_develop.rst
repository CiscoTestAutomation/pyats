pyats develop
=============

Helper command to ease and expedite the process of cloning pyATS package 
repositories and putting those packages into development mode.

.. note::

  This commands requires Github SSH keys if internal Cisco packages are to be 
  cloned 

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
                            unicon.plugins
      -e, --external        Clone external public repositories instead of internal. Only applicable to
                            internal Cisco pyATS installations. For external pyATS Installations,
                            external public repositories will always be used (Optional)
      -d, --directory DIRECTORY
                            Absolute or relative path of directory to clone repositories into. If not
                            supplied, then the default directory is $VIRTUAL_ENV/pypi if using a Python
                            virtual environment, or /usr/pypi otherwise (Optional)
      -f, --force-develop   Run 'make develop' even if packages are already in development mode
                            (Optional)
      -s, --skip-version-check
                            Do not check if pyATS packages are up to date before tool execution.
                            WARNING: Using this option may lead to pyATS package version conflicts which
                            could result in a corrupted pyATS installation! Use with discretion
                            (Optional)
      --delete-repos        Delete existing repositories within directory before cloning new ones
                            (Optional) IMPORTANT: Please back up your work before using this option!
      -c, --clone-only      Just clone the repos, do not put them into development mode (Optional)

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels

- if repos already exist in the target directory, then new repos will not be 
cloned unless the --delete-repos option is used

