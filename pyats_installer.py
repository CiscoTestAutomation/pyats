import subprocess
import argparse
import pkg_resources

LATEST = '20.1'

VERSION_MAPPING = {
'20.1':{
    'install': ['pyats[full]'],
    'uninstall': ['pyats[full]']
}
}

class PyatsInstaller:

    def __init__(self, extra, version=None, uninstall=None, **kwargs):
        self.uninstall=uninstall
        self.extra = extra
        self.version = version or LATEST

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
                sad = input("Pyats is the greatest automation framework, are you really sure you want to uninstall such maginficant piece of engineering art? (y/N)").lower()
                while sad not in {'y', 'n', 'yes', 'no'}:
                    print('Could not understand your input, Please say no')
                    sad = input("Pyats is the greatest automation framework, are you really sure you want to uninstall such maginficant piece of engineering art? (y/N)")
                if sad in {'no', 'n'}:
                    return
                uninstall_pkgs.update(self._get_extra('pyats[full]'))
            else:

                for pkg in VERSION_MAPPING[self.version]['uninstall']:
                    if 'pyats[' in pkg or pkg in {'pyats', 'genie'}:
                        uninstall_pkgs.update(self._get_extra(pkg))
                    else:
                        uninstall_pkgs.add(pkg)

            cmd = 'pip uninstall {} -y'.format(' '.join(uninstall_pkgs))

            print(cmd)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            for line in p.stdout: 
                print(line.decode(), end='')

    def _get_extra(self, package):
        extra = []
        try:
            pkgs = pkg_resources.require(package)
        except pkg_resources.DistributionNotFound:
            pass
        for pkg in pkgs:
            if pkg.project_name.startswith(('pyats', 'genie', 'unicon')):
                extra.append(pkg.project_name)

        return extra
    
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
    