import os
import subprocess

import btools.pybookmark as pybookmark
import btools.common as common
from ConfParser import ConfParser

class FileMatcher:

    def __init__(self, bookmark_file = "", rules_file = ""):
        if rules_file == "":
            rules_file = common.get_conf_location()

        c = ConfParser(bookmark_file)
        c.parse_file(rules_file)
        self.variables = c.variables
        self.rules = c.rules
        self.bookmarks = c.bookmarks


    def strict(self):
        return self.variables["strict"].lower() not in [ "0", "false", ""]

    def symlink(self):
        return self.variables["symlink"].lower() not in ["0", "false", ""]



    def get_weighted_table(self, file):
        """Returns sorted [(bookmark, weight)] list. Best match first."""

        common.debug("Weighing %s" % file)
        res = {}

        for r in self.rules:
            w = res.get(r.bookmark, 0.0)
            dw = r.weigh(file, self.variables)
            res[r.bookmark] = w + dw
            if dw > 0.0:
                common.info("Matched %s on %s using %s rule (%s)" % (file, r.bookmark, r.match_token, r.text))

        return filter(lambda a: a[1] >= float(self.variables["threshold"]),
                sorted(res.iteritems(), key=lambda a: a[1], reverse=True))


    def match(self, fileOrDir):

        if os.path.isdir(fileOrDir):
            self.match_directory(fileOrDir)
        elif os.path.isfile(fileOrDir):
            self.match_file(fileOrDir)
        else:
            common.error("File not found '%s'" % fileOrDir)

    def match_file(self, file, matching_dir = False):
        ftable = self.get_weighted_table(file)
        if len(ftable) == 0:
            if not matching_dir:
                self.exec_unmatched(file)
            else:
                return False
        elif self.strict():
            if len(ftable) == 1:
                match = ftable[0]
                self.exec_matched(file, match)
            else:
                common.warning("Conflict: Disregarding matches for %s. "
                "Strictness is set and there are %d matches" % (file, len(ftable)))
        else:
            match = ftable[0]
            self.exec_matched(file, match)
            if self.symlink():
                bms = pybookmark.get_bookmark(match[0], self.bookmarks)[0]
                for m in ftable[1:]:
                    self.exec_latter(os.path.join(bms[1], file), m)

    def match_directory(self, dir):
        if self.variables["handle_directories"] in ["0", "2"]:
            if self.match_file(dir, matching_dir = True) is False:
                if self.variables["handle_directories"] == "2":
                    self.match_recursively(dir)
        else:
            self.match_recursively(dir)

    def match_recursively(self, dir):
        common.debug("Recursing on directory %s" % dir)
        map(lambda a: self.match(os.path.join(dir, a)), os.listdir(dir))



    def exec_unmatched(self, file):
        e = str.strip(self.variables["exec_unmatched"])
        if e != "":
            e = common.replace_variables(e.replace("%file%", os.path.realpath(file).replace("'", "\'")), self.variables)
            common.info("Executing: %s" % e)
            subprocess.Popen(e, shell = True)
        else:
            common.debug("Nothing to execute for %s. exec_unmatched is empty" % file)

    def exec_matched(self, file, match):
        self._exec_help("exec_best", file, match)

    def exec_latter(self, file, match):
        self._exec_help("exec_latter", file, match)

    def _exec_help(self, key, file, match):
        bms = pybookmark.get_bookmark(match[0], self.bookmarks)
        if len(bms) == 1:
            x = bms[0]
            e = self.variables[key]
            if e != "":
                e = e.replace("%file%", os.path.realpath(file).replace("'", "\'"))
                e = e.replace("%bookmark%", x[0])
                e = e.replace("%match%", x[1])
                e = common.replace_variables(e, self.variables)
                common.info("Executing: %s" % e)
                subprocess.Popen(e, shell = True)
            else:
                common.debug("Nothing to execute for %s. %s is empty." % (file, key))
        else:
            common.warning("Bookmark matches too many directories. Can't move file.")

