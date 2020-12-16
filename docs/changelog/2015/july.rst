July 2015
=========

July 23, 2015
-------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v2.0.3

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

- if you are upgrading from v2.0.1+, it's pretty straightforward.
 
  .. code-block:: bash

      bash$ pip install --upgrade ats

- if you are upgrading from a lower version, refer to v2.0.0 and v2.0.1 upgrade
  instructions for details.

- if you've upgraded your ``pip`` package to 7.x.x, please also perform the 
  following:

  - Modify your ``env.sh`` file, starting from ``# BEGIN CUSTOM pyATS CONTENT``:

    .. code-block:: bash
     
        # BEGIN CUSTOM pyATS CONTENT
        export PIP_TRUSTED_HOST=ats-pypi-server.cisco.com
        export PIP_INDEX_URL=http://ats-pypi-server.cisco.com/simple
        export PIP_DISABLE_PIP_VERSION_CHECK=1

    - Modify your ``env.csh`` file, starting from ``# BEGIN CUSTOM pyATS 
      CONTENT``:

    .. code-block:: bash
     
        # BEGIN CUSTOM pyATS CONTENT
        setenv PIP_TRUSTED_HOST ats-pypi-server.cisco.com
        setenv PIP_INDEX_URL http://ats-pypi-server.cisco.com/simple
        setenv PIP_DISABLE_PIP_VERSION_CHECK 1

Bug Fixes
^^^^^^^^^

- Fixed an issue with pre/post processors in AEtest not displaying ``Skipped``
  correctly for testcase sections (even though it was performing the act of
  skipping).
- Fixed an issue with taskresults file (that are generated during execution) to
  show the full id (eg, tc name + section name) instead of just section name.

Misc
^^^^

- installation now adds a new environment variable 
  ``PIP_DISABLE_PIP_VERSION_CHECK=1`` to ``env.sh`` and ``env.csh`` file, 
  intentionally disabling the automated version checking of ``pip``.
- removed ``PIP_EXTRA_INDEX_URL`` environment variable from ``env.sh`` and 
  ``env.csh`` file, 