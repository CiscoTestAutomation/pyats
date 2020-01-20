#!/usr/bin/python
import subprocess
import argparse
from distutils.version import StrictVersion
LATEST = '20.1'

VERSION_MAPPING = {
    '20.1': {
        'uninstall': ['pyats[full]']
    },
    '19.11':{
        
        'uninstall': ['unicon']
        
    },
    
    '19.7':{
        'uninstall':['genie.example','pyats.templates', 'pyats.examples']
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
    'pyats.utils',
    'pyats.templates',
    'pyats.examples'}

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
    'genie.trafficgen',
    'genie.example'}

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
        self.latest = StrictVersion(self.version) == StrictVersion(LATEST)
        try:
            import pyats.aetest
            
        except ImportError:
            self.installed = False
            self.current_version = None
            self.downgrade = False
            
        else:
            self.installed = True
            self.current_version = pyats.aetest.__version__
            # genie deps changed after 20.1
            self.GENIE_PKG_DEPENDENCIES = NEW_GENIE_PKG_DEPENDENCIES if StrictVersion(
                    self.current_version) >= StrictVersion('20.1') else OLD_GENIE_PKG_DEPENDENCIES
            self.downgrade = StrictVersion(self.version) < StrictVersion(self.current_version)

    def run(self):

        # install if not installed
        if not self.installed:
            if self.uninstall:
                print("Pyats is not installed.")
                return
            # if dont want to install latest
            else:
                cmd = self._get_install_cmd()

        # uninsall then re-install to perform upgrade/downgrade
        else:

            # uninstall only
            if self.uninstall:
                sad = input(
                    "Are you sure you want to uninstall pyats and it's libraries? (y/n)").lower()
                while sad not in {'y', 'n', 'yes', 'no'}:
                    print('Your response is invalid, please enter y or n')
                    sad = input(
                        "Are you sure you want to uninstall pyats and it's libraries? (y/n)").lower()
                if sad in {'no', 'n'}:
                    return
                
                cmd = self._get_uninstall_cmd()

            elif self.version not in VERSION_MAPPING and not self.downgrade and self.latest:
            # this version upgrade does not require special care, simply upgrade the pkgs 
                cmd = self._get_install_cmd(True)
            # upgrade
            else:
                # if downgrade then uninstall everything and re-install everything
                if self.downgrade:
                    print("Downgrading pyats to version {}".format(self.version))

                # if upgrade we first uninstall/install what's provided in the mapping
                # then upgrade the rest of the pkgs
                else: 
                    print("Upgrading pyats to version {}".format(self.version))
                    # uninstall and reinstall in the from the version mapping
                    

                if self.downgrade or not self.latest:
                    install_cmd = self._get_install_cmd()
                else:
                    install_cmd = self._get_install_cmd(True)

                cmd = ';'.join([self._get_uninstall_cmd(), install_cmd])

        print(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        for line in p.stdout:
            print(line.decode(), end='')
        p.wait()

    def _get_install_cmd(self, upgrade=False):
        if upgrade:
            cmd = 'pip3 install pyats{} --upgrade'.format(
                    ''.join(['[', self.extra, ']']) if self.extra else '')
        
        elif not self.latest:
            cmd = 'pip3 install pyats{}=={}'.format(
                ''.join(['[', self.extra, ']']) if self.extra else '', self.version)
        else:
            cmd = 'pip3 install pyats{}'.format(
                ''.join(['[', self.extra, ']']) if self.extra else '')
        
        return cmd

    def _get_uninstall_cmd(self):
        mapping = {'pyats[full]': PYATS_PKG_DEPENDENCIES |
                   self.GENIE_PKG_DEPENDENCIES | ROBOT | UNICON,
                   'pyats': PYATS_PKG_DEPENDENCIES,
                   'genie': self.GENIE_PKG_DEPENDENCIES}
                   
        uninstall_pkgs = set()

        if self.uninstall or self.downgrade:
            uninstall_pkgs.update(mapping['pyats[full]'])

        else:
            for pkg in VERSION_MAPPING[self.version]['uninstall']:
                        if 'pyats[' in pkg or pkg in {'pyats', 'genie'}:
                            uninstall_pkgs.update(mapping[pkg])
                        else:
                            uninstall_pkgs.add(pkg)

        cmd = 'pip3 uninstall {} -y'.format(' '.join(uninstall_pkgs))

        return cmd


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
