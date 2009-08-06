import os
import sys

loglevel = 4


template = "/usr/share/bm/bm-config-template"

def debug(msg):
    if loglevel >= 3:
        sys.stderr.write("[DEBUG]   %s\n" % msg)

def info(msg):
    if loglevel >= 2:
        sys.stderr.write("[INFO]    %s\n" % msg)

def warning(msg):
    if loglevel >= 1:
        sys.stderr.write("[WARN]    %s\n" % msg)

def error(msg):
    sys.stderr.write("[ERROR]   %s\n" % msg)
    os.sys.exit(1)


def get_conf_location():
    if os.path.exists(".bm-match"):
        return os.path.realpath("./.bm-match")
    else:
        h = os.environ["HOME"]
        return os.path.join(h, ".bm-match")

def replace_variables(dest, variables):
    res = []
    for d in dest.split():
        if d[0] == "%" and d[-1] == "%":
            if variables.has_key(d[1:-1].lower()):
                d = variables[d[1:-1].lower()]
            else:
                d = ""
        res.append(d)
    return " ".join(res)


OUTPUT_COLOR = True

VERSION = "1.0rc4"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
GRAY = "\033[1;30m"
NOCOLOR = "\033[0m"


themes = [("gray-blue-green", GRAY, BLUE, GREEN),
          ("gray-red-green", GRAY, RED, GREEN),
          ("gray-gray-green", GRAY, GRAY, GREEN),
          ("gray-gray-red", GRAY, GRAY, RED),
          ("gray-green-red", GRAY, GREEN, RED),
          ("gray-green-blue", GRAY, GREEN, BLUE),
         ]
theme = themes[0]
