import subprocess
import argparse
import pkg_resources
from distutils.version import StrictVersion
LATEST = '19.12'

VERSION_MAPPING = {
    '20.1': {
        'install': ['pyats[full]'],
        'uninstall': ['pyats[full]']
    },
    '19.11':{
        'install': ['unicon', 'unicon.plugins'],
        'uninstall': ['unicon']
    }
}
# todo find a way to automatically find pkg deps+extras
# pkg_resource.require doesnt work b/c it raise exception if the dep is not installed
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

UNICON = {
    'unicon', 'unicon.plugins'
}


class PyatsInstaller:

    def __init__(self, extra, version=None, uninstall=None, **kwargs):
        self.uninstall = uninstall
        self.extra = extra
        self.version = version or LATEST
        # genie deps changed after 20.1
        self.GENIE_PKG_DEPENDENCIES = NEW_GENIE_PKG_DEPENDENCIES if StrictVersion(
            self.version) >= StrictVersion('20.1') else OLD_GENIE_PKG_DEPENDENCIES
        
        try:
            import pyats.aetest
            
        except ImportError:
            self.installed = False
            self.current_version = None
            self.downgrade = False
            
            
        else:
            self.installed = True
            self.current_version = pyats.aetest.__version__
            self.downgrade = StrictVersion(self.version) < StrictVersion(self.current_version)
            self.latest = StrictVersion(self.version) < StrictVersion(LATEST)

    def run(self):

        # install if not installed
        if not self.installed:
            if self.uninstall:
                print("Pyats is not installed.")
                return
            # if dont want to install latest
            if self.latest:
                cmd = 'pip install pyats{}=={}'.format(
                    ''.join(['[', self.extra, ']']) if self.extra else '', self.version)
            else:
                cmd = 'pip install pyats{}'.format(
                    ''.join(['[', self.extra, ']']) if self.extra else '')

        # uninsall then re-install to perform upgrade/downgrade
        else:

            uninstall_pkgs = set()

            # uninstall only
            if self.uninstall:
                sad = input(
                    "Pyats is the greatest automation framework, are you really sure you want to uninstall such a magnificent engineering masterpiece? (y/N)").lower()
                while sad not in {'y', 'n', 'yes', 'no'}:
                    print('Could not understand your input, Please say no')
                    sad = input(
                        "Pyats is the greatest automation framework, are you really sure you want to uninstall such a magnificent engineering masterpiece? (y/N)").lower()
                if sad in {'no', 'n'}:
                    return
                uninstall_pkgs.update(self._get_uninstall_pkgs('pyats[full]'))
                cmd = 'pip uninstall {} -y'.format(' '.join(uninstall_pkgs))

            elif self.version not in VERSION_MAPPING and not self.downgrade and self.latest:
            # this version upgrade does not require special care, simply upgrade the pkgs 
                cmd = 'pip install pyats{} --upgrade'.format(
                    ''.join(['[', self.extra, ']']) if self.extra else '')
            # upgrade
            else:
                # if downgrade then uninstall everything and re-install everything
                if self.downgrade:
                    print("Downgrading pyats to version {}".format(self.version))
                    uninstall_pkgs.update(
                        self._get_uninstall_pkgs('pyats[full]'))
                    

                # if upgrade we first uninstall/install what's provided in the mapping
                # then upgrade the rest of the pkgs
                else: 
                    print("Upgrading pyats to version {}".format(self.version))
                    # uninstall and reinstall in the from the version mapping
                    for pkg in VERSION_MAPPING[self.version]['uninstall']:
                        if 'pyats[' in pkg or pkg in {'pyats', 'genie'}:
                            uninstall_pkgs.update(
                                self._get_uninstall_pkgs(pkg))
                        else:
                            uninstall_pkgs.add(pkg)

                if self.downgrade or not self.latest:
                    install_cmd = 'pip install pyats{}=={}'.format(
                        ''.join(['[', self.extra, ']']) if self.extra else '', self.version)
                else:
                    install_pkg = ' '.join(
                        VERSION_MAPPING[self.version]['install'])
                    install_cmd = 'pip install {}; pip install pyats{} --upgrade'.format(
                        install_pkg, ''.join(['[', self.extra, ']']) if self.extra else '')

                cmd = ';'.join(
                    ['pip uninstall {} -y'.format(' '.join(uninstall_pkgs)), install_cmd])

        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        for line in p.stdout:
            print(line.decode(), end='')

    def _get_uninstall_pkgs(self, package):
        mapping = {'pyats[full]': PYATS_PKG_DEPENDENCIES |
                   self.GENIE_PKG_DEPENDENCIES | ROBOT | UNICON,
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
