import os
import subprocess
import pipes

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
        self.interactive = False


    def strict(self):
        return self.variables["strict"].lower() not in [ "0", "false", ""]

    def symlink(self):
        return self.variables["symlink"].lower() not in ["0", "false", ""]

    def retain_structure(self):
        return self.variables["retain_structure"].lower() not in ["0", "false", ""]


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


    def match(self, fileOrDir, depth = 0):

        if os.path.isdir(fileOrDir):
            self.match_directory(fileOrDir, depth = depth)
        elif os.path.isfile(fileOrDir):
            self.match_file(fileOrDir, depth = depth)
        else:
            common.error("File not found '%s'" % fileOrDir)

    def match_file(self, file, matching_dir = False, depth = 0):
        ftable = self.get_weighted_table(file)
        if len(ftable) == 0:
            if not matching_dir:
                self.exec_unmatched(file)
            else:
                return False
        elif self.strict():
            if len(ftable) == 1:
                match = ftable[0]
                self.exec_matched(file, match, depth = depth)
            else:
                common.warning("Conflict: Disregarding matches for %s. "
                "Strictness is set and there are %d matches" % (file, len(ftable)))
        else:
            match = ftable[0]
            self.exec_matched(file, match, depth = depth)
            if self.symlink():
                bms = pybookmark.get_bookmark(match[0], self.bookmarks)
                if len(bms) != 1 and os.path.isdir(match[0]):
                    dir = match[0]
                else:
                    dir = bms[0][1]
                for m in ftable[1:]:
                    self.exec_latter(os.path.join(dir, file), m, depth = depth)

    def match_directory(self, dir, depth = 0):
        if self.variables["handle_directories"] in ["0", "2"]:
            if self.match_file(dir, matching_dir = True, depth = depth) is False:
                if self.variables["handle_directories"] == "2":
                    self.match_recursively(dir, depth = depth)
        else:
            self.match_recursively(dir, depth = depth)

    def match_recursively(self, dir, depth = 0):
        common.debug("Recursing on directory %s" % dir)
        map(lambda a: self.match(os.path.join(dir, a), depth = depth + 1), os.listdir(dir))



    def exec_unmatched(self, file):
        e = str.strip(self.variables["exec_unmatched"])
        if e != "":
            e = common.replace_variables(e.replace("%file%", os.path.realpath(file).replace("'", "\'")), self.variables)
            common.info("Executing: %s" % e)
            subprocess.Popen(e, shell = True)
        else:
            common.debug("Nothing to execute for %s. exec_unmatched is empty" % file)

    def exec_matched(self, file, match, depth = 0):
        self._exec_help("exec_best", file, match, depth)

    def exec_latter(self, file, match, depth = 0):
        self._exec_help("exec_latter", file, match, depth)

    def _exec_help(self, key, file, match, depth = 0):
        bms = pybookmark.get_bookmark(match[0], self.bookmarks)
        if len(bms) != 1 and os.path.isdir(match[0]):
            bms = [(match[0], match[0])]

        if len(bms) == 1:
            x = bms[0]
            e = self.variables[key]
            if e != "":
                file = os.path.realpath(file)
                dest = self.get_dest_retained_structure(file, os.path.realpath(x[1]), depth, makedir = False)

                e = e.replace("%file%", pipes.quote(file))
                e = e.replace("%bookmark%", pipes.quote(x[0]))
                e = e.replace("%match%", pipes.quote(dest))
                e = common.replace_variables(e, self.variables)
                common.info("Executing: %s" % e)
                if self.interactive:
                    t = common.theme
                    no = common.NOCOLOR
                    print
                    print "=" * 80
                    print
                    print "%s%s%s %s===>%s %s%s%s" % (t[2], file, no, t[1], no,
                                                      t[3],  dest, no)
                    print "%sMatched on %s%s" % (t[1], x[0], no)
                    print "%sThe following command is about to be executed%s" % (t[1], no)
                    print
                    print "   ", e
                    print
                    proceed= raw_input("Proceed? [Y/n/q] ").lower()
                    if proceed == "": proceed = "y"
                    print
                    if proceed[0] == "n":
                        return
                    elif proceed[0] == 'q':
                        os.sys.exit(0)

                dest = self.get_dest_retained_structure(file, os.path.realpath(x[1]), depth, makedir =True)
                subprocess.Popen(e, shell = True)
            else:
                common.debug("Nothing to execute for %s. %s is empty." % (file, key))
        else:
            common.warning("Bookmark matches too many directories. Can't move file.")

    def get_dest_retained_structure(self, file, dest, depth, makedir = False):
        if depth > 0 and self.retain_structure():
            dirs = file.split(os.sep)[-(depth + 1):]
            for d in dirs[:-1]:
                tmp = os.path.join(dest, d)
                if not os.path.exists(tmp):
                    common.debug("Making sub directory in destination.  %s." % tmp)
                    if makedir:
                        os.mkdir(tmp)
                dest = tmp
            dest = os.path.join(dest, dirs[-1])
        return dest

