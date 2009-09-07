from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install import install

import glob
import os
import platform
from os import path


class check_platform(install):

    def run(self):
        if platform.system() in ["Windows", "Win32"]:
            print "=" * 80
            print
            print "I'm sorry, it's not that we don't like you; it's just that this package "
            print "depends on UNIX-like features and does not work on the Windows platform."
            print "I want to thank you for trying it out, though. Treat yourself to something nice."
            print "And may your future endeavors be more fruitful. Fare thee well! "
            print
        else:
            install.run(self)


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
      version="0.99999",
      description="Command line navigation and organization tools",
      long_description=
"""Bookmark tools is a collection of useful shell commands and Python scripts \
for UNIX-like platforms that aim to speed up navigation and organization in day to day work. 
""",
      author="Bart Spaans",
      author_email = "onderstekop@gmail.com",
      url="http://www.bookmark-tools.com/",
      license="GPLv3",
      packages = ["btools", "btools.matching"],
      scripts = ["scripts/bm", "scripts/mkbm", "scripts/bm-match",
                 "scripts/bmsuggest", "scripts/bmsuggest-move", 
                 "scripts/bmsuggest-series", "scripts/bm-add-series", 
                 "scripts/mvbm", "scripts/blog", "scripts/fill-template",
                 "scripts/script2gif"],
      data_files = [("/etc/bash_completion.d/", ["data/bm-completion"]),
                    ("/usr/share/bm/", ["data/bm.bash", "data/bm-match-config", "data/movies.patterns"]),
                    ("/usr/share/man/man1/", glob.glob("doc/man/*.1")),
                    ("/usr/share/blog/hooks/", glob.glob("data/blog/hooks/*")),
                   ],
      cmdclass={"install": check_platform, 
                "install_data": source_shell_script},
     )


