import subprocess
import argparse
import pkg_resources
from distutils.version import StrictVersion
LATEST = '20.1'

VERSION_MAPPING = {
    '20.1': {
        'install': ['pyats[full]'],
        'uninstall': ['pyats[full]']
    }
}

PYATS_PKG_DEPENDENCIES = {
    'pyats',
    'pyats.aereport',
    'pyats.aetest',
    'pyats.async',
    'pyats.cisco',
    'pyats.log',
    'pyats.kleenex',
    'pyats.connections',
    'pyats.datastructures',
    'pyats.easypy',
    'pyats.results',
    'pyats.reporter',
    'pyats.tcl',
    'pyats.topology',
    'pyats.utils'}

# pre 20.1
OLD_GENIE_PKG_DEPENDENCIES = {
    'genie',
    'genie.abstract',
    'genie.metaparser',
    'genie.libs.parser',
    'genie.parsergen',
    'genie.telemetry',
    'genie.libs.telemetry',
    'genie.conf',
    'genie.ops',
    'genie.harness',
    'genie.predcore',
    'genie.utils',
    'genie.libs.conf',
    'genie.libs.ops',
    'genie.libs.sdk',
    'genie.libs.filetransferutils',
    'genie.trafficgen'}

# after 20.1
NEW_GENIE_PKG_DEPENDENCIES = {
    'genie',
    'genie.libs.conf',
    'genie.libs.filetransferutils',
    'genie.libs.ops',
    'genie.libs.parser',
    'genie.libs.sdk',
    'genie.telemetry',
    'genie.trafficgen'}

ROBOT = {
    'pyats.robot',
    'genie.libs.robot'
}


class PyatsInstaller:

    def __init__(self, extra, version=None, uninstall=None, **kwargs):
        self.uninstall = uninstall
        self.extra = extra
        self.version = version or LATEST
        self.GENIE_PKG_DEPENDENCIES = NEW_GENIE_PKG_DEPENDENCIES if StrictVersion(self.version) >= StrictVersion('20.1') else OLD_GENIE_PKG_DEPENDENCIES

    def run(self):
        try:
            import pyats

            installed = True
        except ImportError:

            installed = False

        if not installed:
            if self.uninstall:
                print("Pyats is not installed.")
                return

            if self.extra:
                cmd = 'pip install pyats[{}]'.format(self.extra)
            else:
                cmd = 'pip install pyats'
            print(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            for line in p.stdout:
                print(line.decode(), end='')

        else:

            uninstall_pkgs = set()

            if self.uninstall:
                sad = input(
                    "Pyats is the greatest automation framework, are you really sure you want to uninstall such maginficant piece of engineering art? (y/N)").lower()
                while sad not in {'y', 'n', 'yes', 'no'}:
                    print('Could not understand your input, Please say no')
                    sad = input(
                        "Pyats is the greatest automation framework, are you really sure you want to uninstall such maginficant piece of engineering art? (y/N)")
                if sad in {'no', 'n'}:
                    return
                uninstall_pkgs.update(self._get_uninstall_pkgs('pyats[full]'))

            else:

                for pkg in VERSION_MAPPING[self.version]['uninstall']:
                    if 'pyats[' in pkg or pkg in {'pyats', 'genie'}:
                        uninstall_pkgs.update(self._get_uninstall_pkgs(pkg))
                    else:
                        uninstall_pkgs.add(pkg)

            cmd = 'pip uninstall {} -y'.format(' '.join(uninstall_pkgs))

            print(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            for line in p.stdout:
                print(line.decode(), end='')

    def _get_uninstall_pkgs(self, package):
        mapping = {'pyats[full]': PYATS_PKG_DEPENDENCIES +
                   self.GENIE_PKG_DEPENDENCIES + ROBOT,
                   'pyats': PYATS_PKG_DEPENDENCIES,
                   'genie': self.GENIE_PKG_DEPENDENCIES}

        return mapping[package]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pyats installer script')
    parser.add_argument('extra',
                        metavar='[extra]',
                        type=str,
                        nargs='?',
                        help='Choose which type of installation, choose between full, library, robot, or template. Leave empty if you just want to install the core framework.\n'
                        'For detail on each types please check https://pubhub.devnetcloud.com/media/pyats/docs/getting_started/index.html#installation')

    parser.add_argument('--version',
                        type=str,
                        help="specify which version you'd like to install")

    parser.add_argument('--uninstall',
                        action='store_true',
                        help="Uninstall pyats and it's libriaries")
    args = parser.parse_args()

    installer = PyatsInstaller(**args.__dict__)
    installer.run()
