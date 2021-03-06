import os
import sys
import pipes
import subprocess
import platform

WINDOWS = platform.system() == "Windows"



## Packagers beware: Hard coded paths

if not WINDOWS:
    share = "/usr/share" 
    template = share + "/bm/bm-match-config"
    BLOG_SHARE = share + "/blog/"
    DEFAULT_EDITOR = "/etc/alternatives/editor"

    # This should ideally be moved to a separate package..btools-data?
    pattern_collections = { "movies" : share + "/bm/movies.patterns",
                            "tv" : share + "/bm/tv.patterns",
                            "albums": share + "/bm/albums.patterns",
                            "artists" : share + "/bm/artists.patterns"}
else:
    pf = os.environ["PROGRAMFILES"]
    template = os.path.join(pf, "btools", "bm-match", "bm-match-config")
    BLOGSHARE = os.path.join(pf, "btools", "blog", "")
    DEFAULT_EDITOR = "notepad"
    pattern_collections = { "movies" : os.path.join(pf, "btools", "bm-match", "movies.patterns")}




VERSION = "1.0rc4"


# Disable color codes on Windows
if not WINDOWS:
    OUTPUT_COLOR = True
else:
    OUTPUT_COLOR = False


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



loglevel = 4


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

def cli_module_help(module):
    cli_output_help( module["name"], module["description"], 
                    module["usage"], module["commands"], module["examples"] )

def cli_output_help(prog, description, usage, commands, examples, option_title = "Options:"):
    cli_version(prog, description)
    cli_usage(prog, usage)
    cli_help(commands, option_title)
    cli_examples(prog, examples)

def cli_version(name, description):
    name = os.path.basename(name)
    print "%s %s - %s" % (name, VERSION, description)
    print "© 2008, 2009, Bart Spaans <bart@bookmark-tools.com>"

def cli_usage(prog, usagelist):
    prog = os.path.basename(prog)
    if type(usagelist) == str:
        usagelist = [usagelist]

    maxlen = -1
    for u in usagelist:
        if type(u) == str and len(u) > maxlen:
            maxlen = len(u)
        elif type(u) == tuple and len(u[0]) > maxlen:
            maxlen = len(u[0])
    print
    print "Usage: ", 
    for u in usagelist:
        if type(u) == str:
            print prog, u, "\n\t",
        else:
            print prog, u[0],
            print " " * ((maxlen - len(u[0])) + 3),
            print u[1], "\n\t",
    print


def cli_examples(prog, examples):
    prog = os.path.basename(prog)
    print "Examples:"
    maxcommandlen = -1
    for command, description in examples:
        if len(command) > maxcommandlen:
            maxcommandlen = len(command)
    for command, description in examples:
        print "\t", prog, command,
        print " " * ((maxcommandlen - len(command)) + 4),
        print description



def cli_help(commands, title = "Commands:"):
    print title
    for com, args, description in commands:
            print "\n\t", 
            for c in com:
                    print "%s %s  " % (c, args),
            print "\n\t    %s" % description
    print


def cli_command_help(args, cmd):
    for a in args:
        for c in cmd:
            if a in c[0]:
                fmt = "%s"
                if len(c[0]) > 1:
                    fmt = "(%s)"
                print "Usage: %s %s" % (fmt % ", ".join(c[0]) , c[1])
                print "      ", c[2]

def default_editor():
    return os.environ.get("EDITOR", DEFAULT_EDITOR)


def edit_file(file):
    subprocess.Popen("%s %s" % (default_editor(), 
                                pipes.quote(file)),
                    shell=True).wait()
