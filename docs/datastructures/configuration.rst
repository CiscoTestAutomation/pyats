Configuration Container
=======================

The ``Configuration`` container is a special type of ``NestedAttrDict`` intended
to store Python module and feature configurations. 

Avoid confusing Python configuration with router configuration. Python
configurations tends to be key value pairs that drives a particular piece
of infrastructure, telling it how its behavior should be. 

.. code-block:: Python

    # Example
    # -------
    # 
    #   using Configuration() class

    from pyats.datastructures import Configuration

    # instantiating it
    cfg = Configuration()

    # loading some INI style config files
    cfg.load_cfgs('/path/to/file.ini')
    cfg.load_cfgs('/path/to/file.conf')

    # load yaml style config files
    cfg.load_yamls('/path/to/config.yaml')

    # loading python entrypoints
    cfg.load_entrypoint(group = 'entrypoint.group.name')

    cfg
    # Configuration({
    #     'email': Configuration({
    #         'smtp': Configuration({
    #             'host': 'mail.cisco.com', 
    #             'port': 25}), 
    #         'default_domain': 'cisco.com'})})

Behavior
--------

- Configuration class inherits all the behaviors of ``NestedAttrDict``

- ``Configuration.copy()`` will walk the entire configuration tree, and all
  children ``Configuration`` nodes will be copied. (Eg - it's a pseudo deep
  copy, but will only deep copy its own object type)

- ``Configuration.load_cfgs(*files)`` accepts ``N`` INI style files. Internally
  it uses ``configparser.ConfigParser.read(*files)`` api, and inherits all of 
  its behavior. Returns the list of files that was loaded successfully.

  - does not raise exception if file doesn't exist
  
  - the ``DEFAULT`` block in configparser is removed

  - basic data types will be typecasted into Python objects
    (bool/int/float/None)

- ``Configuration.load_yamls(*files)`` accepts ``N`` yaml files. Internally
  performs a YAML load on each file, and saves the configuration data.
  The files are read from left to right, hence if any data block is repeated in
  the files, the right most file's data takes precedence. Returns the list of
  files that was loaded successfully.

- ``Configuration.load_entrypoint(group)`` loads a Python entrypoint group.
  Any loaded group data needs to return a dictionary-like data, which will
  get updated into this configuration object

