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
    def run(self):
        install_data.run(self)

        cmd = "source /usr/share/bm/bm.bash"

        if path.exists("/etc/bash.bashrc") and path.exists("/usr/share/bm/bm.bash"):
            f = open("/etc/bash.bashrc")
            bashrc = f.read()
            f.close()

            if cmd in bashrc.splitlines():
                return
            else:
                print "Sourcing bm.bash"
                try:
                    f = open("/etc/bash.bashrc", "a")
                except:
                    print "Error: Couldn't write to /etc/bash.bashrc"
                    return
                f.write(cmd + os.linesep)
                f.close()



setup(name="btools",
      version="0.9999999",
      description="Command line navigation and organization tools",
      long_description=
"""Bookmark tools is a collection of useful, cross platform shell commands and Python scripts \
that aim to speed up navigation and organization in day to day work. 
""",
      author="Bart Spaans",
      author_email = "onderstekop@gmail.com",
      url="http://www.bookmark-tools.com/",
      license="GPLv3",
      packages = ["btools", "btools.matching"],
      scripts = scripts,
      data_files = data,
      cmdclass={ "install_data": source_shell_script},
     )


