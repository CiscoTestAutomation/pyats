#!/usr/bin/python
import subprocess
import argparse
import json
from distutils.version import StrictVersion
LATEST = '20.1'

VERSION_MAPPING = {
    '20.1': {
        'uninstall': ['pyats[full]']
    },
    '19.11': {

        'uninstall': ['unicon']

    },

    '19.7': {
        'uninstall': ['genie.example', 'pyats.templates', 'pyats.examples']
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

# internal version
ATS_PKG_DEPENDENCIES = {
    'ats',
    'ats.aereport',
    'ats.aetest',
    'ats.async',
    'ats.cisco',
    'ats.log',
    'ats.kleenex',
    'ats.connections',
    'ats.datastructures',
    'ats.easypy',
    'ats.results',
    'ats.reporter',
    'ats.tcl',
    'ats.topology',
    'ats.utils',
    'ats.templates',
    'ats.examples'}

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
    'genie.examples'}

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
        
        print("Checking your current environment for existing pyATS installations...")
        pkg_list = json.loads(subprocess.check_output("pip list --format json", shell=True, universal_newlines=True))
        self.installed = True
        for pkg in pkg_list:
            if pkg['name'] == 'pyats':
                self.current_version = pkg['version']
                self.ats = False
                break
            elif pkg['name'] == 'ats':
                self.current_version = pkg['version']
                self.ats = True
                break
        else:
            # pyats or ats not in pip list, it's not installed
            self.installed = False
            self.current_version = None
            self.downgrade = False

        if self.installed:
            print("You have {} version {} installed".format('ats (internal)' if self.ats else 'pyats (external)', self.current_version))
            # genie deps changed after 20.1
            self.GENIE_PKG_DEPENDENCIES = NEW_GENIE_PKG_DEPENDENCIES if StrictVersion(
                self.current_version) >= StrictVersion('20.1') else OLD_GENIE_PKG_DEPENDENCIES
            self.downgrade = StrictVersion(
                self.version) < StrictVersion(self.current_version)

    def run(self):
        cmds = []
        # install if not installed
        if not self.installed:
            if self.uninstall:
                print("Pyats is not installed.")
                return
            # if dont want to install latest
            else:
                cmds.append(('Installing pyATS', self._get_install_cmd()))

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

                cmds.append(('Uninstalling pyATS and its libraries',
                             self._get_uninstall_cmd()))

            elif self.version not in VERSION_MAPPING and not self.downgrade:
                # this version upgrade does not require special care, simply upgrade the pkgs
                msg = "Upgrading pyats to version {}".format(self.version)
                if self.latest:
                    cmds.append((msg,self._get_install_cmd(True)))
                else:
                    cmds.append((msg,self._get_install_cmd()))
            # upgrade
            else:
                cmds.append(
                    ("Uninstalling existing pyats and its libraries", self._get_uninstall_cmd()))
                if self.downgrade or not self.latest:
                    install_cmd = self._get_install_cmd()
                else:
                    install_cmd = self._get_install_cmd(True)

                # if downgrade then uninstall everything and re-install everything
                if self.downgrade:
                    msg = "Downgrading pyats to version {}".format(
                        self.version)

                # if upgrade we first uninstall/install what's provided in the mapping
                # then upgrade the rest of the pkgs
                else:
                    msg = "Upgrading pyats to version {}".format(self.version)
                    # uninstall and reinstall in the from the version mapping

                cmds.append((msg, install_cmd))

        for cmd in cmds:
            print('==================================================')
            print(cmd[0])
            print('==================================================')
            print(cmd[1])
            p = subprocess.Popen(cmd[1], stdout=subprocess.PIPE,
                                 universal_newlines=True, shell=True)
            for line in p.stdout:
                print(line, end='')
            p.wait()
            if p.returncode != 0:
                raise subprocess.CalledProcessError(p.returncode, cmd[1])

    def _get_install_cmd(self, upgrade=False):
        if upgrade:
            cmd = 'pip3 install {}{} --upgrade'.format(self._get_pkg_type(), self._get_extra())

        elif not self.latest:
            if StrictVersion(self.version) < StrictVersion('19.10'):
                if (self.extra == 'full' or self.extra == 'library') and StrictVersion(self.version) >= StrictVersion('19.7'):
                    cmd = 'pip3 install {}=={} genie=={} unicon=={}'.format(self._get_pkg_type(),
                        self.version, self.version, self.version)
                elif self.extra == 'full' or self.extra == 'library':
                    cmd = 'pip3 install {}=={} {}'.format(self._get_pkg_type(), self.version, ''.join(''.join(
                        [pkg, '==', self.version, ' ']) for pkg in OLD_GENIE_PKG_DEPENDENCIES | {'unicon'}))

                else:
                    cmd = 'pip3 install {}=={}'.format(self._get_pkg_type(),self.version)
            else:
                cmd = 'pip3 install {}{}=={}'.format(self._get_pkg_type(), self._get_extra(), self.version)
        else:
            cmd = 'pip3 install {}{}'.format(self._get_pkg_type(), self._get_extra())

        return cmd
    
    def _get_pkg_type(self):
    # return ats or pyats based on pkg type
        return 'ats' if self.ats else 'pyats'

    def _get_extra(self):
        return ''.join(['[', self.extra, ']']) if self.extra else ''

    def _get_uninstall_cmd(self):
        mapping = {'pyats[full]': PYATS_PKG_DEPENDENCIES |
                   self.GENIE_PKG_DEPENDENCIES | ROBOT | UNICON,
                   'ats[full]': ATS_PKG_DEPENDENCIES |
                   self.GENIE_PKG_DEPENDENCIES | ROBOT | UNICON,
                   'pyats': PYATS_PKG_DEPENDENCIES,
                   'ats': ATS_PKG_DEPENDENCIES,
                   'genie': self.GENIE_PKG_DEPENDENCIES}

        uninstall_pkgs = set()
        # pytas[full] does not exist before 19.10, so if user wannts to uninstall the full suite we need to manually uninstall all pkgs
        if self.uninstall or self.downgrade or StrictVersion(self.current_version) < StrictVersion('19.10'):
            if self.ats:
                uninstall_pkgs.update(mapping['ats[full]'])
            else:
                uninstall_pkgs.update(mapping['pyats[full]'])

        else:
            for pkg in VERSION_MAPPING[self.version]['uninstall']:
                if 'ats[' in pkg or pkg in {'ats','pyats', 'genie'}:
                    if self.ats:
                        uninstall_pkgs.update(mapping[pkg.replace('pyats.', 'ats.')])
                    else:
                        uninstall_pkgs.update(mapping[pkg])
                else:
                    if self.ats:
                        uninstall_pkgs.add(pkg.replace('pyats.', 'ats.'))
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
