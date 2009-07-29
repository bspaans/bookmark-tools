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
