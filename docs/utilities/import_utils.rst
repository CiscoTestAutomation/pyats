Import Utilities
================

Import By String
----------------

Translate a 'x.y.z' style string into 'from x.y import z', and return z.
Allows users to import using string names instead of calling importer.

.. code-block:: python

    # Example
    # -------

    from pyats.utils.import_utils import import_from_name
    obj = import_from_name('my_package.my_module')

Run On Import
-------------

Allows user to decorate a function, and run the content of the function when
the function is declared/imported.

.. code-block:: python

    # Example
    # -------

    from pyats.utils.import_utils import on_import

    @on_import
    def _init():
        print('hello world')

Legacy Import Helper
--------------------

Enables you to continue using legacy import paths without having to modify much
of your script. This functionality is akin to Python's native
``from __future__ import X`` where ``X`` is a new, future feature. Where as in
Python the above import gives you a glimpse into the future, and leverage
future, upcoming features, this ``LegacyImporter`` enables you to dwell in the
past, and enables your older scripts to continue to function.

To enable legacy imports in any piece of code (python module, package, or
pyATS test script), add the following as the top-most line in your files:

.. code-block:: python

    # at the top of the script
    # (before all other imports)
    from pyats.utils import __legacy_imports__


From here on, you can start making legacy imports.

.. code-block:: python

    # Example
    # -------

    # assume for instance, a package changed its imports in a new release
    # from:
    import my_module

    # to:
    import my_package.my_module

    # in you script, as long as you do this first:
    from pyats.utils import __legacy_imports__

    # you'll be able to continue to
    import my_module

    # instead of changing your import statements everywhere :)

.. tip::

    It's always a good idea to update your script... whenever possible. Dwelling
    in the past is ... well, never a great thing.

Limitations
^^^^^^^^^^^

- **There is no Free Lunch**. In order for packages
  to continue offering legacy import paths, the package developers needs to
  follow the developer guide (below) and register their import mappings

- Only handles import **path** changes, eg, ``from x.y import z`` to
  ``from xx.yy import z``, and does not magically address things such as:

  - removed/deleted modules

  - renamed classes/functions/methods/variables

  - modified/altered code logic/behaviour

- Does not perform dual translations, eg, if you swap the content of two
  modules.

- Only works with **packaged** python code. Eg, any package that is installed
  using ``pip install`` command, that is built using a ``setup.py`` file using
  Setuptools.

Developer Guide
^^^^^^^^^^^^^^^

As a package developer, it is **your responsibility** to register your
legacy-to-latest import mappings to ``LegacyImporter`` in order to allow your
users to continue using their legacy imports.

.. tip::

    always be mindful of the limitations above.

.. code-block:: python

    # Step 1
    # ------
    #   add a dictionary mapping of your legacy to new import name mapping in
    #   your package as a module variable.
    #     - the key is the "legacy" import path
    #     - the value is the "new" import path

    # in your module's __init__, for example
    IMPORT_MAPPING = {
        'legacy': 'new',
    }

    # Step 2
    # ------
    #   in your package's setup.py file, add the follwing lines in setup()
    #   api block.
    #
    #   setup(
    #       ...
    #       entry_points = {
    #           'pyats.utils.__legacy_imports__': '<name> = <pkg.module.var>',
    #       },
    #       ...
    #   )
    #
    #   where <name> is your package's name, and <pkg.module.var> is the
    #   import paths to the above variable where you declared the mapping.

    # example - in your setup.py file
    setup(
        # ... ,
        entry_points = {
            'pyats.utils.__legacy_imports__': 'my_pkg = mypkg.my_module.IMPORT_MAPPING',
        },
        # ... ,
    )

    # and voila!
    # from here onwards, with any newly built packages, if users perform
    #   from pyats.utils import __legacy_imports__
    # they will be able to leverage the translations you've defined

Ultimately, the ability to translate imports comes down to how well you define
your translation mapping dictionary. Here's the built-in behaviour:

  - as the translation mapping is a dictionary,

    - the key represents 'legacy' name patterns

    - the value represents 'new', or 'latest up to date' name patterns

  - if both key/value are strings, string substitution is used when translating
    import paths. Eg - if an import module path wholly matches the key, it
    is replaced in whole, by value

    .. code-block:: python

        if import_requested == key or import_requested.startswith(key + '.'):
            new_import = import_requested.replace(key, value)

    .. note::

        the translation also auto-applies to a package's child modules. Eg,
        if ``x.y`` module is renamed to ``x.z``, then your imports such as
        ``x.y.a`` will auto map to ``x.z.a``

In addition, if you are making "complex" transformations, you can provide
functions that does the mappings:

.. code-block:: python

    # Example
    # -------
    #
    #   translating the name 'my_package' to 'your_package'

    # define a function that translates legacy names to new names
    def to_new(name):
        if name == 'my_package' or if name.startswith('my_package.'):
            return name.replace('my_package', 'your_package', 1)

    # define the reverse function that translates a new name to a legacy one
    def to_old(name):
        if name == 'your_package' or if name.startswith('your_package.'):
            return name.replace('your_package', 'my_package', 1)

    # in your module's __init__, instead of defining a dictionary,
    # define a tuple, where the first item is your to function, and
    # the 2nd item is your from function
    IMPORT_MAPPING = (to_new, to_old)

    # and follow step #2 of above.

Note that when providing callables to perform the translation, you must follow
these rules:

- both the to and from functions must be provided for completeness

- no assumptions will be made: all import names will pass through your function,
  and you will perform all necessary translations, including child module names.

- your translation function should never fail, and shall return ``None`` when
  the provided import name doesn't meet your translation criterion.

.. tip::

      be VERY mindful of what you're trying to do here.
