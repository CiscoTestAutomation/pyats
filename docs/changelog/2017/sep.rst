September 2017
==============

Sep 25, 2017
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.kleenex``, v3.3.2
    ``ats.easypy``, v3.3.6
    ``ats.utils``, v3.3.4


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    bash$ pip install --upgrade ats.kleenex ats.easypy ats.utils

Changes
^^^^^^^

- Kleenex

  - If a bringup orchestrator emits clean configuration it is merged
    on top of the user's clean configuration.

  - Migration of bringup configuration from the legacy pre-v3.0.0 format
    has now been deprecated.

  - Relaxed a few Kleenex restrictions : now in the following cases
    instead of throwing an exception, only a warning is logged:

    - One or more specified images cannot be found.

    - The clean YAML contains devices not present in the testbed YAML.

  - Enhanced the Kleenex clean schema to allow images to be specified by
    type (for example, rp, lc, kickstart, system, smu, pie).

    - NOTE: Explicit cleaner support is required for this expanded format.

- Easypy

  - Now a logical testbed must be specified using the
    ``-logical_testbed_file`` parameter.  Auto-detection of logical devices
    in the non-logical testbed file has been deprecated.

- Utils

  - Made clean/testbed YAML schema failure reports more human-readable.
