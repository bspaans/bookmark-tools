from distutils.core import setup
import glob

setup(name="btools",
      version="1.0rc4",
      description="Command line bookmarking tools",
      author="Bart Spaans",
      author_email = "onderstekop@gmail.com",
      license="BSD",
      packages = ["btools", "btools.matching"],
      scripts = ["scripts/bm", "scripts/mkbm", "scripts/bm-match"],
      data_files = [("/etc/bash_completion.d/", ["data/bm-completion"]),
                    ("/usr/share/bm/", ["data/bm.bash", "data/bm-config-template"]),
                    ("/usr/share/man/man1/", glob.glob("doc/man/*.1")),
                   ]

     )


