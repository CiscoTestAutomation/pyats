.. _secret_strings:

Secret Strings
==============

Secret strings (such as passwords) may be specified in an encoded form suitable
for sharing with a wide audience, while ensuring that only authorized
users are able to decode these strings into their plaintext form.

A secret string class is provided that behaves like a string but has some
special features.

Refer to :ref:`pyats_configuration` for more details on secret string
related configuration.

See :ref:`pyats secret CLI` for details on the CLI commands related
to secret string manipulation.


.. warning::

       By default, pyATS secret strings are not cryptographically secure.

How to secure your secret strings
---------------------------------

Follow this procedure to make your secret strings cryptographically secure:

#. Update your :ref:`pyATS configuration file<pyats_configuration>` as
   follows::

       [secrets]
       string.representer = pyats.utils.secret_strings.FernetSecretStringRepresenter

#. Install the cryptography package::

    > pip install cryptography

#. Ensure the permissions are restricted on your
   :ref:`pyATS configuration file<pyats_configuration>` to prevent others
   from reading it.  For example::

       > chmod 600 ~/.pyats/pyats.conf

#. Generate a cryptographic key::

    > pyats secret keygen
    Newly generated key :
    dSvoKX23jKQADn20INt3W3B5ogUQmh6Pq00czddHtgU=

#. Update your :ref:`pyATS configuration file<pyats_configuration>` as
   follows::

       [secrets]
       string.representer = pyats.utils.secret_strings.FernetSecretStringRepresenter
       string.key = dSvoKX23jKQADn20INt3W3B5ogUQmh6Pq00czddHtgU=

#. Encode a password::

    (RECOMMENDED)
    > pyats secret encode 
    Password: MySecretPassword
    Encoded string :
    gAAAAABdsgvwElU9_3RTZsRnd4b1l3Es2gV6Y_DUnUE8C9y3SdZGBc2v0B2m9sKVz80jyeYhlWKMDwtqfwlbg4sQ2Y0a843luOrZyyOuCgZ7bxE5X3Dk_NY=

    OR

    > pyats secret encode --string MySecretPassword
    Encoded string :
    gAAAAABdsgvwElU9_3RTZsRnd4b1l3Es2gV6Y_DUnUE8C9y3SdZGBc2v0B2m9sKVz80jyeYhlWKMDwtqfwlbg4sQ2Y0a843luOrZyyOuCgZ7bxE5X3Dk_NY=

#. Do a test decode of the encoded password::

    > pyats secret decode gAAAAABdsgvwElU9_3RTZsRnd4b1l3Es2gV6Y_DUnUE8C9y3SdZGBc2v0B2m9sKVz80jyeYhlWKMDwtqfwlbg4sQ2Y0a843luOrZyyOuCgZ7bxE5X3Dk_NY=
    Decoded string :
    MySecretPassword

#. Add your encoded password to a testbed.yaml %ENC{} block, as described in
   :ref:`topology_credential_password_modeling`.  Now your password is
   secured.  The only way to decode the password from the testbed YAML file
   is to use the same pyATS configuration file used to encode the password::

    # Snippet of your testbed.yaml
    testbed:
        name: sampleTestbed
        credentials:
            default:
                username: admin
                password: "%ENC{gAAAAABdsgvwElU9_3RTZsRnd4b1l3Es2gV6Y_DUnUE8C9y3SdZGBc2v0B2m9sKVz80jyeYhlWKMDwtqfwlbg4sQ2Y0a843luOrZyyOuCgZ7bxE5X3Dk_NY=}"


Multiple Representers
---------------------

Follow this procedure to specify multiple representers if there are several
kinds of encoded strings you want to specify in a file such as a testbed YAML:

#. Add your new representer to the
   :ref:`pyATS configuration file<pyats_configuration>` as follows::

       [secrets]
       my_custom.representer = package.module.MyRepresenterClass

#. Generate a key if your representer requires it::

    > pyats secret keygen --prefix my_custom
    Newly generated key :
    <generated key for my_custom>


#. Update your :ref:`pyATS configuration file<pyats_configuration>` with the
   newly generated key (if required) as follows::

       [secrets]
       my_custom.representer = package.module.MyRepresenterClass
       my_custom.key = <generated key for my_custom>

#. Encode a password using the default representer::

    > pyats secret encode
    Password: MySecretPassword
    Encoded string :
    wr3DssK0w5nDlsORw4nDmcK2w4LDqMOfw6vDjsOdw4k=

#. Encode a password using the my_custom representer::

    > pyats secret encode --prefix my_custom
    Password: MySecretPassword
    Encoded string :
    <my_custom encoded string>

#. Add references to your encoded passwords to your testbed YAML file,
   for example::

    testbed:
        credentials:
            default:
                username: my_username
                password: "%ENC{wr3DssK0w5nDlsORw4nDmcK2w4LDqMOfw6vDjsOdw4k=}"
            alternate:
                username: alternate_username
                password: "%ENC{<my_custom encoded string>, prefix=my_custom}"
        custom:
            custom_key: |4-
                custom data containing encoded text
                %ENC{<my_custom encoded string>, prefix=my_custom}


#. Check that your passwords can be recovered from the loaded testbed::

    > pyats shell --testbed_file my_testbed.yaml
    >>> from pyats.utils.secret_strings import to_plaintext
    >>> to_plaintext(testbed.credentials.default.password)
    'MySecretPassword'
    >>> to_plaintext(testbed.credentials.alternate.password)
    'MySecretPassword'
    >>> testbed.custom.custom_key
    'custom data containing encoded text\nMySecretPassword'


Secret String Object
--------------------

.. code-block:: text

    +--------------------------------------------------------------------------+
    | SecretString object                                                      |
    +==========================================================================+
    | class methods  | description                                             |
    |----------------+---------------------------------------------------------|
    | from_plaintext | returns an encoded secret string from plaintext         |
    |----------------+---------------------------------------------------------|
    | keygen         | returns a key that affects the string encoding/decoding |
    +==========================================================================+
    | properties     | description                                             |
    |----------------+---------------------------------------------------------|
    | plaintext      | returns the decoded secret string in plaintext form     |
    +==========================================================================+
    | attributes     | description                                             |
    |----------------+---------------------------------------------------------|
    | data           | the secret string in encoded form                       |
    +==========================================================================+
    | methods        | description                                             |
    |----------------+---------------------------------------------------------|
    | __str__        | returns asterisks in order to hide the secret string    |
    +--------------------------------------------------------------------------+


Example
-------

.. code-block:: python

    # Example
    # -------
    #
    #   creating secret string objects

    from pyats.utils.secret_strings import to_plaintext, SecretString

    # Create a secret string by specifying its encoded form.
    # The ``pyats secret encode`` CLI command may be used to convert a
    # plaintext string to encoded form.
    my_secret = SecretString('w53DssKBw6fDmMOCw5bDisOa')

    # Decode the password
    my_secret.plaintext
    'my password'

    # Create a secret string from plaintext.
    my_secret =  SecretString.from_plaintext('another secret')

    # Asterisks are shown when the secret is printed.
    print(my_secret)
    **************

    # Print the secret string in plaintext form.
    # The ``pyats secret decode`` CLI command may be used to convert
    # an encoded string to plaintext form.
    to_plaintext(my_secret)
    'another secret'

    # to_plaintext works on regular strings as well.
    to_plaintext('plain string')
    'plain string'

    # Print the secret string in its encoded form.
    my_secret.data
    'w53DssKBw6fDmMOCw5bDisOa'

    # Allocate a brand new key.
    # This does the same thing as the ``pyats secret keygen`` CLI command.
    print(SecretString.keygen())

    # Allocate a secret string that stores a string in plaintext (non-encoded)
    # form.
    from pyats.utils.secret_strings import PlainTextSecretStringRepresenter
    weak_secret = SecretString('weak_pw', representer_cls= PlainTextSecretStringRepresenter)


Representer Classes
-------------------

The encoding/decoding of secret strings and any required key management is
defined in a pluggable manner by the use of representer classes.

Supported Representers
^^^^^^^^^^^^^^^^^^^^^^

The following representers are supported:

- ``pyats.utils.secret_strings.ObscuringSecretStringRepresenter``
  - This class stores the secret string in cipher-encoded form.

  - It is the default representer if the user has not specified a representer
    in pyATS configuration.

  - It uses a default key, but allows the user to overwrite the key in
    pyATS configuration.

- ``pyats.utils.secret_strings.PlainTextSecretStringRepresenter``
  - This class stores the secret string in plaintext form.

  - It does not make use of the key.

- ``pyats.utils.secret_strings.FernetSecretStringRepresenter``

  - This class stores the secret string in crypto-encoded form.

  - It requires the user to manually execute ``pip install cryptography``.

  - It can generate a decryption key.

  - A generated key must be specified in pyATS configuration.


Sample Representer Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. code-block:: python

    from pyats.utils.secret_strings import BaseSecretStringRepresenter

    class MySecretStringRepresenter(BaseSecretStringRepresenter):
        """ My secret string representer """
        @classmethod
        def keygen(cls):
            return my_generate_key()

        @property
        def key(self):
            key = super().key
            if key == self.DEFAULT_KEY:
                raise Exception("A key must be specified as pyATS "
                    "configuration under [secrets] string.key.\n"
                    "This key may be generated with "
                    "the 'pyats secret keygen' command")
            return key

        def encode(self):
            """ Encode a contained plaintext string object """
            return my_encode(key=self.key, data=self.obj.data)

        def decode(self):
            """ Decode a contained encoded string object """
            return my_decode(key=self.key, data=self.obj.data)

