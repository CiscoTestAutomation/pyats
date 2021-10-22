.. _pyats_configuration:

Configuration
=============

pyATS allows you to set various component/feature configuration and defaults
in a standard INI style config file.

- on Linux/Mac the default server-wide configuration file is ``/etc/pyats.conf``

- inside a virtual environment, the file is ``$VIRTUAL_ENV/pyats.conf``

- the per-user configuration file is ``$HOME/.pyats/pyats.conf``

- Setting environment variable ``export PYATS_CONFIGURATION=path/to/pyats.conf``

- The cli argument ``--pyats-configuration`` can be used to specify a
  configuration file

If multiple configuration files are found, then they are combined in the
following order:

1. the server-wide file is read
2. the virtual-environment specific file is read
3. the per-user file is read
4. the file specified by environment variable ``PYATS_CONFIGURATION`` is read
5. the file specified by cli argument ``--pyats-configuration` is read

Each file read overrides any values read from previous files.

.. code-block:: ini

    # Example
    # -------
    #
    #   pyATS configuration file

    [email]
    smtp.host = mail.google.com
    smtp.port = 25
    default_domain = gmail.com

Each INI file content is standardized to use:

- ``[]`` to denote sections
- ``=`` as key/value delimiter
- ``#`` for comments.

.. note::

    do not use quotes around strings in INI files - see
    `supported INI file structures <https://docs.python.org/3.6/library/configparser.html#supported-ini-file-structure>`_
    for details.

Configurable Fields
-------------------

The following fields are currently open for user to customize.

.. code-block:: ini

    # Configurable Fields
    # -------------------

    # configuration related to sending emails
    [email]

    # smtp host url/ip and port
    smtp.host = <value>
    smtp.port = <port>

    # smtp to use TLS/ssl
    smtp.ssl = <True/False>

    # smtp connection timeout (default to 30s)
    smtp.timeout = <timeout in seconds>

    # smtp username/password for authentication
    smtp.username = <username>
    smtp.password = <password>

    # default domain name
    # (use this to enable setting recipients to just ID without @domain.com)
    default_domain = <domain.com>

    # configuration related to log viewing
    [logs]
    server.host = <host interface/ip to start log server on>
    server.port = <port to start server on>
    browser = <path to browser executable to open>

    # configuration related to easypy execution
    [easypy]

    # archive storage directory
    # (use this to specify where you want pyATS archive zip file to be saved)
    runinfo.archive = <path>

    # runinfo directory
    # (specifies the location where the runtime dir is created during execution)
    runinfo.directory = <path to runinfo folder>

    # configuration related to aetest
    [aetest]

    # Value of steps continue_ when not explicitly set. Default is False.
    # Steps continue_ determines whether a section should continue execution
    # after a step fails, or immediately exit that section.
    steps.continue = <True/False>

    # Enable/disable banners around "Starting Section" log entries
    logging.banners = <True/False>

    # Enable/disable reporting for all processors. Using the report or noreport
    # decorators takes priority over this option.
    processors.report = <True/False>

    # configuration related to the report
    [report]
    # Format of the report file generated at the end of execution.
    # Default is JSON.
    format = <json/yaml>
    # Collect git info, default is True.
    git_info = <True/False>

    # configuration related to timestamps
    [timestamp]
    # When True, all timestamps are created with UTC time instead of local time
    utc = <True/False>

    # configuration related to topology for testbed loading
    [topology]

    # import paths for replacing any topology classes.
    # must be subclasses of original topology classes.
    # these will be overwritten by any specified class in the testbed yaml file.
    class.testbed = <new.testbed.class>
    class.device = <new.device.class>
    class.link = <new.link.class>
    class.interface = <new.interface.class>

    # configuration related to interaction calls
    [interaction]

    # Address to bind server to
    server.host = <address>
    server.port = <value>

    email.disable = <True/False>

    # May require authentication for SMTP
    email.from = <address>
    email.to = <address>

    # This is formatted by jinja2. section_name is one argument that will be
    # populated in a template format.
    email.subject = <subjectline>

    # Set this to one of the possible section results
    timeout.result = <errored/failed/blocked/etc...>

    # This can be inf, for no timeout, otherwise specify a number of seconds.
    timeout.time = <value>

    # Maximum seconds to wait for a response when loading a YAML file from a URL
    max_wait_time = <value>

    # configuration related to file transfer server
    [filetransfer]

    # Subnet for devices in testbed to identify correct IP address on execution
    # host to use as the file transfer server address
    subnet = <subnet_string>

    # Default server protocol, defaults to ftp
    protocol = <ftp/tftp/scp>

    # configuration related to secrets
    [secrets]

    # This class defines how a secret string is to be encoded and decoded
    # and how keys (if required) are to be generated.
    # (Optional)
    # If not specified, defaults to a class representing a secret string
    # as a non-cryptographically secure cipher.
    # Users must ensure the specified module's directory may be imported
    # by setting their $PYTHONPATH appropriately.
    string.representer = module.class_name

    # This key is used to convert a secret string to plaintext.
    # Some representers may require a key to be set, others may default
    # the key if it is not set.
    # Users are encouraged to secure configuration files containing this key
    # with appropriate permissions.
    string.key = <my secret string key>

    # Set this pattern when using 'pyats run job' to select which environment
    # variables are hidden (encoded as secret strings) prior to being dumped
    # into env.txt.  Environment variables whose names match this pattern are
    # written as ENC(xyz123) and may be decoded via
    # 'pyats secret decode xyz123'.
    env.hide_pattern = .*PASSWORD.*


.. note::
   See :ref:`secret_strings` for more details on how pyATS handles private
   strings (such as passwords).

.. tip::

    More configurable fields to come!
