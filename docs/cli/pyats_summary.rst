pyats summary
=============

Command to query summary of user's script execution regardless of the test execution engine it runs under

.. code-block:: text

    Usage:
        pyats summary

    Description:
        Get summary (status, job run summary) of script execution regardless of which test execution engine user is running on

    Summary Options:
        --request-id REQUEST_ID
                                Request ID on XPRESSO
        --uuid UUID           The uuid of your job run on TaaS
        --earms-id EARMS_ID   Earms id of your job run

    General Options:
        -h, --help            Show help
        -v, --verbose         Give more output, additive up to 3 times.
        -q, --quiet           Give less output, additive up to 3 times, corresponding to WARNING, ERROR,
                                and CRITICAL logging levels

Options
-------

``--request-id``
    use this argument to fetch the summary of a job run on XPRESSO

``--uuid``
    use this argument to fetch summary of a job run on TaaS. Note that the
    baseline comparisons summary is not available since TaaS currently does not
    have a baseline for job runs to compare against.

``--earms-id``
    use this argument to fetch summary of a job run on SSR.

Example
-------

.. code-block:: text

    bash$ pyats summary --earms-id 002241975664744
    Fetching summary of job run...

    Result ID of job run: 002241975664744
    Source: SSR
    Status: COMPLETED
    Summary:

        Abort: 0
        Blocked: 0
        Error: 0
        Fail: 0
        Pass: 13
        Passx: 0
        Skip: 0

    Baseline comparisons:

        Run ID: 002241975664744
        Baseline ID: 002238799151280
        Verdict: Matched or Improved
        Comparison count:
            added: 0
            broken: 0
            fixed: 0
            ignored: 2
            mismatch: 0
            missing: 0
            same: 38

    For more details regarding the job run, see https://ssr.cisco.com/execution/job/002241975664744

    Done.
