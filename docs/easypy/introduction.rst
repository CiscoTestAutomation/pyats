Introduction
============

Easypy provides a standardized runtime environment for testscript execution in
pyATS. It offers a simple, straight-forward way for users to aggregate
testscripts together into **jobs**, integrates various pyATS modules together
into a collectively managed ecosystem, and archives all resulting information
for post-mortem debugging. 

Features
--------

    - **Jobs**: aggregation of multiple testscripts into one *job*.
    - **TaskLog**: stores all runtime log outputs to :ref:`tasklog`.
    - **E-mail Notification**: emails the user result information upon
      finishing.
    - **Multiprocessing Integration**: executes each jobfile Task in a child
      process, and configures the environment to allow for hands-off forking.
    - **Clean**: clean/brings up the current testbed with new images & fresh
      configuration.
    - **Plugins**: plugin-based design, allowing custom user injections to alter
      and/or enhance the current runtime environment.


Installation & Updates
----------------------

Easypy module ``easypy`` is installed by default as part of pyATS installation.
The package is also featured in the PyPI server, and can be installed 
separately.

Note that ``easypy`` module is part of the ``pyats`` namespace, and therefore,
users should always refer to the full namespace when installing & using:

.. code-block:: bash

    pip install pyats.easypy  

To upgrade an existing installation of Easypy package in your environment, do:

.. code-block:: bash

    pip install pyats.easypy --upgrade

.. note ::

    always read the :ref:`changelog` first before you upgrade.


