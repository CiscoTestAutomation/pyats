# pyATS Issue Tracker

This is a place-holder repository used only so there's a bug tracking/forum/wiki for Cisco pyATS Test Framework.

Use the issue tab above to create issues for pyATS.

## General Information

- Website: https://developer.cisco.com/pyats/
- Documentation: https://developer.cisco.com/docs/pyats/
- Support: pyats-support-ext@cisco.com

## Common Questions

##### Is pyATS Free to Use
Yes, pyATS is 100% free to use for anyone and everyone, and available through Python Package Index.

```
$ pip install pyats[full]
```

##### Where do I get support?
You can send an email to pyats-support-ext@cisco.com directly, or post a question in the issues page in this repo. The team will get back to you as soon as possible.

You can also tweet @simingy and @jeaubin5 on twitter, hash-tag #pyATS.

Note that if you received pyATS/scripts as part of a collaborated effort with a Cisco development/test/engineering team, you should be approaching that team instead for script support.

##### Is pyATS Open Source?
Not yet. At the moment the core of pyATS is still closed-source as it is a critical part of the sanity/regression test infrastructure. Through DevNet we are only releasing the Cythonized, binary format of pyATS core framework, enabling customer/external developer usage & close team collaboration.

However, other packages that are developed to be used with pyATS, such as Unicon plugins, parser libraries, packages, YANG/REST connectors and etc, will be open source to public, and available to all in GitHub.

##### Will the pyATS core framework be open source one day?
We consider DevNet as the first baby step towards opening up the infrastructure to the general public. All other options, including open sourcing, are not out of the picture. We will be closely monitoring community adoption, feedback, and take the next steps accordingly.
