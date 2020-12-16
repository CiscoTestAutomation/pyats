April 2018
==========

Apr 30, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.4
    ``ats.robot``, v4.1.0
    ``ats.utils``, v4.1.3


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.robot pyats.easypy pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.robot ats.easypy ats.utils

Changes
^^^^^^^

    - introducing a new optional package ``robot``, enabling users to leverage 
      key pyATS features within Robot Framework

    - applied a workaround for Easypy erroring out in MacOSX under Python3.5/3.6
      due to https://bugs.python.org/issue33395

    - fixed a bug in ``utils.dicts.recursive_cast`` where the input dictionary
      is corrupted

Apr 27, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.tcl``, v4.1.1


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.tcl

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.tcl

Changes
^^^^^^^

    - removed ``_tclHelper_eval_cb()`` unsafe functionality
    - removed the need for ``tclHelper`` namespace package

Apr 20, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.easypy``, v4.1.3


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.easypy

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.easypy

Changes
^^^^^^^

    - Refactored to ensure compatibility with pip v10.0.0.


Apr 11, 2018
------------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.utils``, v4.1.2
    ``ats.easypy``, v4.1.2


Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.utils ats.easypy

Changes
^^^^^^^

    - Refactored the utils.fileutils API to be more general.

    - The easypy Jenkins runinfo class now places runinfo content inside
      a new temp directory and removes the directory when archiving
      succeeds.

Apr 5, 2018
-----------

.. csv-table:: New Module Versions
    :header: "Modules", "Versions"

    ``ats.aetest``, v4.1.2
    ``ats.easypy``, v4.1.1
    ``ats.cisco``, v4.1.2
    ``ats.topology``, v4.1.1
    ``ats.utils``, v4.1.1

Upgrade Instructions
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # DevNet Community
    bash$ pip install --upgrade pyats.aetest pyats.easypy pyats.topology pyats.utils

    # Cisco Internal Developers
    bash$ pip install --upgrade ats.aetest ats.easypy ats.cisco ats.topology ats.utils

Changes
^^^^^^^

    - fixed a deployment bug in ``pyats.aetest`` package where the uploaded
      PyPI package was 32-bit instead of the intended 64-bit support.
      **[DevNet Only]**

    - added a new schema field to topology devices named ``platform``

    - fixed a bug where occasionally Easypy report emails were not being sent
      out to the caller automatically **[Cisco Only]**

    - easypy report should now display Mac OSX platform information correctly

    - removed hard-coding of email default domains and smtp-servers globally
