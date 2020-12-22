.. _pyats secret CLI:

pyats secret
============

This command offers subcommands providing utilities to work with
:ref:`secret_strings`.

.. code-block:: text

    Usage:
      pyats secret <subcommand> [options]

    Subcommands:
        decode              decode an encoded string
        encode              encode a plaintext string
        keygen              generate a key used to encode/decode a secret string

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels
.. _pyats secret keygen:

pyats secret keygen
-------------------

This subcommand generates a key that influences the encoding/decoding of
secret strings (such as credential passwords in the testbed YAML file).

The output of this command is typically manually placed in pyATS
:ref:`pyats_configuration`.

.. code-block:: text

    Usage:
      pyats secret keygen [options]

    Description:
      Generates a new personalized key used to encode/decode a secret string.

      This key, once generated, would typically be manually placed in the pyats
      configuration:
      [secrets] string.key = <generated_key>

      The chosen representer controls the format of the returned key.
      The format of the returned key depends upon the representer specified
      via the pyats configuration:
      [secrets] string.representer = representer_module.representer_class

      IMPORTANT: Please ensure any pyats configuration file(s) containing this key
      are locked down with appropriate permissions to ensure only authorized parties
      may read it.

      If specified, --prefix selects other representers defined in the pyats
      configuration.  The following is expected to be present:
      [secrets] <prefix>.representer

    Keygen Options:
      --prefix [prefix]     Cfg prefix to use (Optional)

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels

Options
^^^^^^^

``--prefix [prefix]``
    the pyATS configuration prefix to use to select a nondefault representer.



.. _pyats secret encode:

pyats secret encode
-------------------

This subcommand will prompt to ask a plaintext string and outputs an encoded form of this
string.(Recommended) Or the plaintext string can be given via `--string`.

The encoding used may be customized via  pyATS :ref:`pyats_configuration`.
In some cases the pyATS configuration may be required to also specify a key.

.. code-block:: text

    Usage:
      pyats secret encode [options]

    Description:
      Encodes a plaintext string into an encoded form.

      The encoding used may be changed by specifying the pyats configuration:
      [secrets] string.representer = representer_module.representer_class

      Otherwise, a default cipher encoding is used.

      The encoding may be personalized by using the pyats configuration:
      [secrets] string.key = <generated_key>

      where <generated_key> refers to the key generated with the "pyats secret keygen"
      command.

      If specified, --prefix selects other representers defined in the pyats
      configuration.  The following are expected to be present:
      [secrets] <prefix>.representer
      [secrets] <prefix>.key

    Encode Options:
      --string [string]     String to encode (Optional)
      --prefix [prefix]     Cfg prefix to use (Optional)

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels


Options
^^^^^^^

``--string [string]``
    the plaintext string to encode

``--prefix [prefix]``
    the pyATS configuration prefix to use to select a nondefault representer.



.. _pyats secret decode:

pyats secret decode
-------------------

This subcommand accepts an encoded string and outputs a plaintext form of this
string.

The encoding expected may be customized via  pyATS :ref:`pyats_configuration`.
In some cases the pyATS confuration may be required

.. code-block:: text

    Usage:
      pyats secret decode [string] [options]

    Description:
      Decodes an encoded string into plaintext form.

      The decoding used may be changed by specifying the pyats configuration:
      [secrets] string.representer = representer_module.representer_class

      Otherwise, a default cipher encoding is expected.

      The decoding may be personalized by using the pyats configuration:
      [secrets] string.key = <generated_key>

      where <generated_key> refers to the key generated with the "pyats secret keygen"
      command.

      If specified, --prefix selects other representers defined in the pyats
      configuration.  The following are expected to be present:
      [secrets] <prefix>.representer
      [secrets] <prefix>.key

    Decode Options:
      [string]              String to decode
      --prefix [prefix]     Cfg prefix to use (Optional)

    General Options:
      -h, --help            Show help
      -v, --verbose         Give more output, additive up to 3 times.
      -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                            and CRITICAL logging levels

Options
^^^^^^^

``[string]``
    the encoded string to decode

``--prefix [prefix]``
    the pyATS configuration prefix to use to select a nondefault representer.
