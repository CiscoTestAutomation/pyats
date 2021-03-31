--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* Cisco
    * Remove proxies from `os.environ` before a call to requests package in `businesstelemetry.py`.
    * Mocked out the get_token() function during the test_tims_via_rest function of test_cisco_aereporter.py. Fixes issue
    * when a valid tims token has not been previously acquired by user

* Log
    * fix logviewer file list to support nested folder
    * add argument --displayed-url
    * fixed bug not showing all steps in logviewer
    * changed aiohttp version for sdk.
    * Install aiohttp==3.6.3 when python_version<3.6;
    * Install aiohttp==3.7.2 when python_version>=3.6 .
    * update log color in logviewer

* Easypy
    * Added `--branch` and `--meta` arguments for cli
    * Add `--no-xml-report` option to disable generating the xml report

* Utils
    * change version requirement to cryptography<=3.2.1
    * Overwrite `email._policybase.Policy.max_line_length`'s deafult value (78) with a higher value (998) to stop emails from wrapping lines

* Markup
    * Add YAML markup for command line arguments
        * Allows users to specify --arg value on the command line to populate the value for %CLI{arg} in the YAML file.

* Aetest
    * Fix test_interaction tests failing due to a requests package issue when running on lab machines that use proxy

* pyats.connections
    * Close log handlers on disconnect

* Aetest/Reporter
    * Remove parameter reporting for sections

* Reporter
    * reporter.details() now returns an Explorer instead of the full testsuite,

* Makefile
    * Change version requirement robotframework -> robotframework==3.2.2

* Robot
    * Install now requires robotframework==3.2.2

* pyATS
    * Add extra empty string to `cli/commands/version/check.py`'s `metavar` argument to keep argparse formatting reliable

* pyats.topology
    * Updated type as optional in testbed schema validation
