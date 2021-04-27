=============
Terminologies
=============

py
    Short-hand for Python. The current Python version used in pyATS is Python
    3.6/3.7/3.8

CONFIG file
    Tcl-ATS legacy file, used to describe testbed hardware information such as
    IPs, FTP/TFTP, clean etc information. This concept is now rolled into a
    single pyATS Testbed file

MAP file
    Tcl-ATS legacy file, used to describe testbed topology information in a
    keyed-list format. This concept is now rolled into a single pyATS testbed
    file

pyATS Instance/Install
    A particular instance (a.k.a. installation) of pyATS infrastructure. The
    equivalent concept in Tcl ATS is an "ATS Tree"

PyPI
    Python Package Index, a Python package/module software repository. The
    official PyPI for Python is at http://pypi.python.org, and the internal
    pyATS PyPI repository (for hosting ATS released, internal modules) is
    located at http://pyats-pypi.cisco.com/

Tcl-ATS
    Legacy Tcl-based test infrastructure written using Tcl, available only for
    internal Cisco Engineering. Deprecated since 2016.

Testbed
    defines the sum of all physical hardware (routers, switches, TGNs)
    interconnected together.

Testbed Topology
    the description of how testbed devices are physically interconnected.

Testbed File
    pyATS standard testbed interconnect & meta-data definition in YAML format

TIMS
    Test Information Management System, a Cisco online content mgmt system that
    supports the documentation and tracking of tests on a project-by-project
    basis.

XRUT
    XR-Unit Testing infrastructure. XRUT is a powerful automation framework
    that was initially development for XR-unit testing, and evolved overtime
    to include NXOS, IOS, Titanium, IOL. As well, it supports black-box and
    white-box testing capabilities.

YAML
    "Yet-Another-Markup-Language" or "YAML Ain't Markup Language",
    is a human-readable data serialization format. See: http://www.yaml.org/
