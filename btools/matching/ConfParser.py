import os
import re


import btools.common as common
import btools.pybookmark as pybookmark
import RuleParsers

class ConfParser:

    def __init__(self, bookmark_file = ""):
        # Dictionary for the 'set' command
        self.variables = { "threshold" : "0.75",
                           "bookmarks" : pybookmark.get_conf_location(),
                           "strict" : "1",
                           "symlink": "0",
                           "exec_best" : "mv %file% %match%",
                           "exec_latter" : "ln -s %file% %match%",
                           "exec_unmatched" : "",
                           "handle_directories": "2",
                           "loglevel": str(common.loglevel),
                           }
        self.parsers = [ y() for y in RuleParsers.__dict__.values() if \
                            type(y) == type(RuleParsers.Parser) and \
                            issubclass(y, RuleParsers.Parser) and \
                            y != RuleParsers.Parser ] 
        

        self.rules = []

        rweight = "\(\ *w(eight)?\ *=\ *([0-9]*[\.[0-9]*]?)\ *\)"
        rvariable = "^\ *([A-Z]+[A-Z0-9_]*)\ *=\ *(.*)\ *$"

        self.re_weight = re.compile(rweight, re.IGNORECASE)
        self.re_variable = re.compile(rvariable, re.IGNORECASE)

        self.set_bookmarks(bookmark_file)


    def set_bookmarks(self, bookmarks):
        """Load bookmark file"""

        if bookmarks == "":
            if hasattr(self.variables, "bookmarks"):
                bookmarks = self.variables["bookmarks"]
            else:
                bookmarks = pybookmark.get_conf_location()

        common.debug("Reading bookmarks from %s" % bookmarks)
        self.bookmarks = pybookmark.read_bookmarks(bookmarks)
        self.variables["bookmarks"] = bookmarks


    def parse_file(self, file):
        common.debug("Parsing configuration file %s" % file)
        f = open(file, "r")
        c = f.read()
        f.close()
        return self.parse(c)


    def parse(self, string):
        self.rules_started = False
        map(self.parse_line, string.split(os.linesep))
        self.rules_started = False


    def parse_line(self, line):
        line = str.strip(line)
        if line == "" or line[0] == "#":
            return

        i = line.find("set ")
        if i == 0:
            if not self.rules_started:
                return self.parse_variable_assignment(line[4:])
            else:
                common.error("Error: variable assignments after rules.")

        i = line.find(" matches ")

        if i != -1:
            bm = line[:i]
            if self.is_valid_bookmark(bm):
                self.parse_rule(bm, line[i + 9:])
                self.rules_started = True
            else:
                common.warning("Unknown tag '%s'. Ignoring rule: %s" % (bm, line))
        else:
            common.warning("Invalid syntax: %s" % line)

    def parse_variable_assignment(self, line):
        s = self.re_variable.search(line)
        if s:
            g = s.groups()
            var = str.lower(g[0])
            common.debug("Setting %s to %s" % (g[0], g[1]))
            if var == "loglevel":
                common.loglevel = int(g[1])
            elif var == "bookmarks":
                self.set_bookmarks(g[1])
            self.variables[g[0]] = g[1]
        else:
            common.error("Couldn't parse variable assignment: %s" % line)

    def parse_rule(self, bookmark, string):

        s = string
        weight,partition = self.get_weight(s)
        if partition >= 0:
            s = s[:partition]

        args = s.split()
        match_token =args[0].lower()

        found = False
        for p in self.parsers:
            if match_token in p.match_token:
                r = p.get_Rule(args[1:], bookmark, weight)
                if r is not None: 
                    self.rules.append(r)
                    common.debug("Added new %s rule on %s (%s)" % (r.match_token, r.bookmark, r.text))
                    found = True

        if not found:
            common.error("Couldn't parse rule: %s" % string)

    def get_weight(self, args):
        w = self.re_weight.search(args)
        if w is not None:
            return float(w.groups()[1]), w.start()
        return 1.0, -1


    def is_valid_bookmark(self, bookmark):
        return len(pybookmark.get_bookmark(bookmark, self.bookmarks)) > 0
