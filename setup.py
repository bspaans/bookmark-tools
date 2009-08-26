from distutils.core import setup
from distutils.command.install_data import install_data

import glob
import os
from os import path

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
      version="0.999",
      description="Command line navigation and organization tools",
      long_description=
"""Bookmark tools is a collection of useful UNIX/Linux shell commands and Python scripts \
that aim to speed up navigation and organization in day to day work. 
""",
      author="Bart Spaans",
      author_email = "onderstekop@gmail.com",
      url="http://www.bookmark-tools.com/",
      license="GPLv3",
      packages = ["btools", "btools.matching"],
      scripts = ["scripts/bm", "scripts/mkbm", "scripts/bm-match",
                 "scripts/bmsuggest", "scripts/bmsuggest-move", 
                 "scripts/bmsuggest-series", "scripts/bm-add-series", 
                 "scripts/mvbm", "scripts/blog", "scripts/fill-template"],
      data_files = [("/etc/bash_completion.d/", ["data/bm-completion"]),
                    ("/usr/share/bm/", ["data/bm.bash", "data/bm-config-template", "data/movies.patterns"]),
                    ("/usr/share/man/man1/", glob.glob("doc/man/*.1")),
                   ],
      cmdclass={"install_data": source_shell_script},

     )


