from distutils.core import setup
from distutils.command.install_data import install_data

import glob
import os
import platform
from os import path

WINDOWS = platform.system() == "Windows"


## Attention packagers:
#  The following paths are hard-coded.
#  If you need to change anything, make sure you also change the path in btools/common.py

if not WINDOWS:
    scripts = glob.glob("scripts/*")
    data = [("/etc/bash_completion.d/", ["data/bm-completion"]),
            ("/usr/share/bm/", ["data/bm.bash", "data/bm-match-config", "data/movies.patterns"]),
            ("/usr/share/man/man1/", glob.glob("doc/man/*.1")),
            ("/usr/share/blog/hooks/", glob.glob("data/blog/hooks/*")),
           ]
else:
    try:
        import py2exe
    except: pass


    pf = os.environ["PROGRAMFILES"]
    scripts = [] # scripts are added to the 'bin' folder instead
    data = [(os.path.join(pf, "btools", "bm-match"), ["data/bm-match-config",
                                                      "data/movies.patterns"]),
            (os.path.join(pf, "btools", "blog"), glob.glob("data/blog/hooks/*")),
            (os.path.join(pf, "btools", "bin"), glob.glob("data/windows/*") + glob.glob("scripts/*"))]
       



class source_shell_script(install_data):

    def source_bash_script(self, to="/etc/bash.bashrc"):
        if path.exists(to) and path.exists("/usr/share/bm/bm.bash"):
            f = open(to)
            bashrc = f.read()
            f.close()

            cmd = "source /usr/share/bm/bm.bash"
            if cmd in bashrc.splitlines():
                return
            else:
                print "Sourcing bm.bash"
                try:
                    f = open(to, "a")
                except:
                    print "Error: Couldn't write to %s" % to
                    return
                f.write(cmd + os.linesep)
                f.close()
        else:
            print "Warning: the shell functions could not be sourced"

    def update_windows_registry(self):
        try:
            import _winreg
        except:
            print "Couldn't change PATH variable in registry, because the _winreg modules could not be loaded."
            return

        path = os.path.join(os.environ["PROGRAMFILES"], "btools", "bin")
        regpath = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)

        try:
            key = _winreg.OpenKey(reg, regpath, 0, _winreg.KEY_ALL_ACCESS)
        except:
            print "Error getting PATH from registry"
            return

        value, type_id = _winreg.QueryValueEx(key, "PATH")

        current = value.split(";")
        if path in current:
            return

        try: 
            _winreg.SetValueEx(key, "PATH", 0, type_id, ";".join(current + [path]))
            print "Updated %s\\PATH registry value" % (regpath)
        except:
            print "Error updating %s\\PATH registry value" % (regpath)



    def run(self):
        install_data.run(self)

        if not WINDOWS:
            self.source_bash_script()
        else:
            self.update_windows_registry()




setup(name="btools",
      version="0.9999999",
      description="Command line navigation and organization tools",
      long_description=
"""Bookmark tools is a collection of useful, cross platform shell commands and Python scripts \
that aim to speed up navigation and organization in day to day work. 
""",
      author="Bart Spaans",
      author_email = "bart@bookmark-tools.com",
      url="http://www.bookmark-tools.com/",
      license="GPLv3",
      packages = ["btools", "btools.matching"],
      scripts = scripts,
      data_files = data,
      cmdclass={ "install_data": source_shell_script},
      classifiers = [
            'Development Status :: 3 - Alpha',
            'Environment :: Console'
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Operating System :: Microsoft :: Windows'
            'Operating System :: POSIX',
            'Programming Language :: Other',
            'Programming Language :: Python :: 2.5',
            'Topic :: Other/Nonlisted Topic',
            'Topic :: System',
            'Topic :: System :: Archiving',
            'Topic :: System :: Shells',
            'Topic :: Text Processing',
            'Topic :: Utilities',
        ]
     )


