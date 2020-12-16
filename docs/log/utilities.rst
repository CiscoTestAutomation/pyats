.. _log-banner:

Logging Utilities
=================

Banners
-------

The ``utils.banner`` api formats a string into a banner message, which can be
then passed to logger APIs. It itself does not perform logging, and instead
only performs style formatting of its input messages.

Banner API behaviors:

It accepts the following arguments

* The width of the banner can be altered with ``width = W``. ``W`` must be an
  int.  The default value is 80.
* The minimum ammount of white space to center the text can be
  altered with ``padding = Y``. ``Y`` must be an int. The default value is 8.
* The character that represents the top and bottom border of the box can be
  modified with ``h_margin = Z``. ``Z`` must be a ``string`` and its size must
  be of ``1``.  The default value is ``-``.
* The character that represents the right and left side border of the box can
  be modified with ``v_margin = X``. ``X`` must be a ``string`` and its size
  must be of ``1``. The default value is ``|``

.. note::
    The width of the banner must always be greater than the padding + 2 (for
    each side)

.. note::

    Newline characters in the message are respected

.. note::

    Single words (non-space separated) longer than the max width are
    chopped into max-width automatically.

.. code-block:: python

    # Example
    # -------
    #
    #   print a banner message

    from pyats.log.utils import banner

    # printing directly
    msg = banner('a banner message')
    print(msg)
    print(banner('aReallyLongMessageThatIsLongerThanMaxWidthIsChoppedUp',
                 width = 40))

    # Output
    # ------
    #
    # +------------------------------------------------------------------------------+
    # |                               a banner message                               |
    # +------------------------------------------------------------------------------+
    # +--------------------------------------+
    # |    aReallyLongMessageThatIsLonger    |
    # |       ThanMaxWidthIsChoppedUp        |
    # +--------------------------------------+


    # printing to log
    import logging
    logger = logging.getLogger(__name__)

    logger.info(banner('an informational message banner'))
    logger.error(banner('an error message\nwith newline'))

    # Output
    # ------
    #
    # +------------------------------------------------------------------------------+
    # |                       an informational message banner                        |
    # +------------------------------------------------------------------------------+
    # +------------------------------------------------------------------------------+
    # |                               an error message                               |
    # |                                 with newline                                 |
    # +------------------------------------------------------------------------------+

    # Changing margin
    msg = banner('a message', v_margin='!', h_margin='&')
    print(msg)

    # Output
    # ------
    #
    # +&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&+
    # !                                  a message                                   !
    # +&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&+

.. _log-title:

Titles
------

The ``utils.title`` api formats a string into a title message, which can be
then passed to logger APIs. It itself does not perform logging, and instead
only performs style formatting of its input messages.

Title API behaviors:

It accepts the following arguments

* The width of the title can be altered with ``width = W``. ``W`` must be an
  int.  The default value is 80.
* The minimum ammount of space that is filled with margin to center the
  text can be altered with ``padding = Y``. ``Y`` must be an int. The default
  value is 10.
* The character that fills the empty space within the given width can be
  modified with ``margin = Z``. ``Z`` must be a ``string`` and its size must
  be of ``1``.  The default value is ``=``.

.. note::
    The width of the title must always be greater than the padding

.. note::

    Newline characters in the message are respected

.. note::

    Single words (non-space separated) longer than the max width are
    chopped into max-width automatically.

.. code-block:: python

    # Example
    # -------
    #
    #   print a title message

    from pyats.log.utils import title

    # printing directly
    msg = title('a title message')
    print(msg)
    print(title('aReallyLongMessageThatIsLongerThanMaxWidthIsChoppedUp',
                 width = 38))

    # Output
    # ------
    #
    # ================================a title message=================================
    # ====aReallyLongMessageThatIsLonger====
    # =======ThanMaxWidthIsChoppedUp========

    # printing to log
    import logging
    logger = logging.getLogger(__name__)

    logger.info(title('an informational message title'))
    logger.error(title('an error message\nwith newline'))

    # Output
    # ------
    #
    # =========================an informational message title=========================
    # ================================an error message================================
    # ==================================with newline==================================

    # Changing margin
    msg = title('a message', margin='!')
    print(msg)

    # Output
    # ------
    #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!a message!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
