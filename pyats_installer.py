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

    def __init__(self, extra, version=None):
        self.extra = extra
        self.version = version or LATEST

    def run(self):
        try:
            import pyats
            
            installed = True
        except ImportError:
            
            installed = False

        if not installed:
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
        for pkg in pkg_resources.require(package):
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
    args = parser.parse_args()

    installer = PyatsInstaller(extra=args.extra, version=args.version)
    installer.run()
    