.. _easypy_email_notification:

Email Notification
==================

When Easypy finishes a job execution, an overall report is emailed to
the user that initiated the run (and any other email addresses provided through
``--mailto`` argument). This behavior is turned-on by default, and may be turned
off using ``--no-mail`` argument.


Report Defaults
---------------

The following describes the default email report content. Note that fields in
``{}`` are dynamic fields generated during runtime.

.. code-block:: text

    # Default Email Subject
    # ---------------------
    pyATS Report - job: {jobname} by: {user}, total: # (P:#, PX:#, F:# ...)


    # Default Email Body
    # ------------------
    pyATS Instance   : {pyats_instance_path}
    Python Version   : {python_name}-{python_version} ({platform arch bits})
    CLI Arguments    : {easypy_cli_arguments}
    User             : {user_id}
    Host Server      : {hostname}
    Host OS Version  : {linux_distro} ({system_architecture})

    Job Information
        Name         : {job.name}
        Start time   : {job.starttime}
        Stop time    : {job.stoptime}
        Elapsed time : {job.elapsedtime}
        Archive      : {job.archive}

    Total Tasks    : {job.taskcount}

    Overall Stats
        Passed     : {#}
        Passx      : {#}
        Failed     : {#}
        Aborted    : {#}
        Blocked    : {#}
        Skipped    : {#}
        Errored    : {#}

        TOTAL      : {#}

    Success Rate   : #.## %

    +------------------------------------------------------------------------------+
    |                             Task Result Summary                              |
    +------------------------------------------------------------------------------+
    {taskid}: {script}.{section}                                            {result}

    +------------------------------------------------------------------------------+
    |                             Task Result Details                              |
    +------------------------------------------------------------------------------+
    {taskid}: {script}
    |-- {section}                                                           {result}
    |   |-- {subsection}                                                    {result}
    |   |   |-- Step 1: {step}                                              {result}
    |   |   |-- Step 1.1: {substep}                                         {result}



Custom SMTP Information
-----------------------

.. tip:

    if you are using pyATS internally in Cisco Engineering, the SMTP host
    information is automatically configured for you.

By default there are no SMTP hosts configured to automatically send out result
emails when a job run is finished. To configure Easypy to use your own SMTP
host, update the following fields in pyATS :ref:`pyats_configuration`'s
``[email]`` block:

- `smtp.host`
- `smtp.port`
- `default_domain`

.. _easypy_report_customization:

Report Customization
--------------------

Easypy email notification reports are fully customizable, allowing users to
attach custom information to the email report body.

During runtime, the current report generation object can be accessed via
``runtime.mail_report`` as described in :ref:`easypy_runtime`. This object has
three editable fields:

``mail_report.subject``
    contains the current report subject template (defaults to the above). This
    field reflects current custom subject if ``--mail-subject`` argument is used
    to invoke ``pyats run job``.

``mail_report.contents``
    a sortable, :ref:`orderabledict` containing report section titles and
    content templates as keys and values. Each key/title is printed in the
    report as a banner to its section, and its value is used as the section
    body.

``mail_report.custom_template``
    Provide a string path to the custom template you would like to extend the
    base template and replace named blocks (tags) within them. Please refer to
    `Template Inheritance`_ for more information.

Editing the above within the jobfile results in a changed/altered report
email. Note however that even though ``runtime`` is also accessible in
:ref:`easypy_tasks` processes, modifying ``runtime.mail_report.contents`` has no
effect, as it is a child process and such modifications do not propagate back to
the main Easypy process.

.. code-block:: python

    # Example
    # -------
    #
    #   adding custom report sections
    #   (always do this in the jobfile/main easypy process)

    # use the runtime object
    def main(runtime):

        # add a custom section
        runtime.mail_report.contents['My Custom Section'] = "My Custom Text"
        # path to the custom template
        runtime.mail_report.custom_template = '/ws/aalfakhr-ott/templates/custom.html'

        # -----------------------
        # when the above job file is run, the following
        # is added to the bottom of the email notification report
        # +------------------------------------------------------------------------------+
        # |                              My Custom Section                               |
        # +------------------------------------------------------------------------------+
        # My Custom Text


.. warning::

    always append your custom report information towards the end of the report.
    The top of the report reserved for important eye-catching information such
    as exceptions, crashes & etc.

Template Inheritance
--------------------

When ``--mail-html`` is used to enable html format email notifications, you have
the option to inherit the base report template into a custom child template.
Template inheritance is done using `Jinja2 templating engine`_ to extend other
templates and replace named blocks (tags) within them.

.. _Jinja2 templating engine: http://jinja.pocoo.org/docs

In the base template, there are 2 tags that are customizable: ``head`` and
``custom_content``. The {% extends email_template %} tells the template engine
that your child template extends another template. This extend tag should be the
first tag in the template. Everything before it is printed out and may cause
confusion when inherited.

Here is an example of what your custom (child) template should look like:

.. code-block:: html

    <!--extend base template-->
    {% extends email_template %}

    <!--add your custom stylesheets here-->
    {% block head %}
        <link rel="stylesheet" href="style.css" />
    {% endblock %}

    <!--add any custom content, displayed end of email report-->
    {% block custom_content %}
        <h1>Index</h1>
        <p class="important">
          Testing results:
        </p>
        {% for key, value in my_dict.iteritems() %}
          <dt>{{ key }}</dt>
          <dd>{{ value }}</dd>
        {% endfor %}
    {% endblock %}

Modify Recipient List
---------------------

During runtime, you are able to modify the recipient list by using
`runtime.mailbot.mailto<pyats.easypy.email.MailBot.mailto>`. By default, the job
submitter is included in the mailto list, users passed to the mailto are
appended to the mailto list.

.. code-block:: python

    # use the runtime object
    def main(runtime):
        mailto_list = ['userA', 'userB']
        runtime.mailbot.mailto = mailto_list

HTML Format Emails
------------------
To generate email notification report in an HTML format
email use ``--mail-html`` to enable HTML format email notifications. You are
still able to attach custom report information in the HTML report, please refer
to `Report Customization`_.

To add an attachment in both HTML and plain text, include the path to the file
content in your jobfile using
`runtime.mail_report<pyats.easypy.email.TextEmailReport>` runtime object:

``runtime.mail_report.attachment``
    contains a path to the attachment file you wish to attach to the Easypy
    email notification. Sends the email without an attachment when file is not
    found.

Report Internals
----------------

The ``easypy`` mailing engine expects ``runtime.mail_report`` object to be
a subclass of ``easypy.email.AbstractEmailReport`` instance. At the end of
execution, ``runtime.mail_report.create_email()`` api is called to automatically
to create an email message to be sent out through SMTP client.

The default report and behavior is defined in ``easypy.email.TextEmailReport``,
which generates a text email message based on a pre-defined, templated string
formatting using ``runtime`` as input.

EmailMsg Class
--------------

``EmailMsg`` class object is a wrapper around Python email module that sends
an email via the ``smtplib`` module. Initializes a single email message which
can be sent to multiple recipients. All parameters are optional and can be set
at any time prior to calling the send() method.

    - **from_email**: The sender's address. Both ``user`` and
      ``user@domain.com`` forms are legal.
    - **to_email**: A list or tuple of recipient addresses.
    - **subject**: The subject line of the email.
    - **body**: The body text. This should be a plain text message.
    - **attachments**: A list of attachments to put on the message. These can be
      either email.MIMEBase.MIMEBase instances, or (filename, content, mimetype)
      triples - currently only supports MIMEText.
    - **html_email**: flag to enable alternative HTML email format.
    - **html_body**: Body in HTML format.
