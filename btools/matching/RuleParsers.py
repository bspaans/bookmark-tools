from Rule import Rule
import btools.common as common

import os
import re
import subprocess
import operator as op
import time

class Parser:

    match_token = [""]
    help = ""

    def __init__(self):
        self.oper = { '==': op.eq, '<=': op.le, "<": op.lt, 
                     '>': op.gt, '>=': op.ge, '!=': op.ne,
                     'eq': op.eq, 'le': op.le, 'lt': op.lt,
                     'gt': op.gt, 'ge': op.ge, 'ne': op.ne}
        self.init()

    def init(self):
        pass

    def get_Rule(self, slist, bookmark, weight):
        def logged_match(m, file, variables):
            common.debug("Testing %s against %s rule (%s)" % (file, self.match_token[0], " ".join(slist)))
            return m(file, variables)

        r = Rule()
        match = self.get_match_function(slist, {"bookmark": bookmark, "weight": weight})
        if match is not None:
            r.bookmark = bookmark
            r.weight = weight
            r.text = " ".join(slist)
            r.match_func = lambda file, variables: logged_match(match, file, variables)
            r.match_token = self.match_token[0]
            return r

    def get_match_function(self, slist, target):
        pass

    def __str__(self):
        return "%s parser" % (self.match_token[0].capitalize())

    def __repr__(self):
        return self.__str__()



class ExtensionParser(Parser):

    match_token = ["extension", "extensions", "ext"]

    def get_match_function(self, slist, target):
        ext = []
        for x in slist:
            x = x.strip()
            if x != "":
                if x[-1] == ",":
                    x = x[:-1]
                if x[0] == ".":
                    x = x[1:]
                ext.append(x.lower())

        def match(file, variables):
            extension = file.split(os.path.extsep)
            if os.path.isfile(file) and len(extension) > 1:
                extension = extension[-1]
                return extension.lower() in ext
            return False
        return match

class SizeParser(Parser):

    match_token = ["filesize", "size"]

    def init(self):
        rfilesize = "(==|<=|<|>|>=|!=|eq|le|lt|gt|ge|ne){1}\ *([0-9]*[\.[0-9]*]?)\ *(b|k|M|G|P|T|P)+?b?\ *$"
        self.re_filesize = re.compile(rfilesize, re.IGNORECASE)


    def get_match_function(self, slist, target):
        sizedict = { 'b': 1, 'k': 1 << 10, 'm': 1 << 20, 'g': 1 << 30,
                    't': 1 << 40, 'p': 1 << 50 }

        s = " ".join(slist)
        r = self.re_filesize.search(s)
        if r is None: return None

        g = r.groups()
        size = int(sizedict[g[2].lower()] * float(g[1]))
        cmp = self.oper[g[0].lower()]

        def match(file, variables):
            if os.path.isfile(file):
                return cmp(os.path.getsize(file), size)
            return False

        return match

class TimeParser(Parser):

    match_token = ["time"]

    def init(self):
        rtime = "(==|<=|<|>|>=|!=|lt|le|eq|ge|gt|ne){1}\ *([0-9]*[\.[0-9]*]?)\ *(y|mo|w|d|m|h|s)+"
        self.re_time = re.compile(rtime, re.IGNORECASE)

    def get_match_function(self, slist, target):
        timedict = { "s": 1, "m": 60, "h": 3600, "d": 86400, 
                     "w": 604800, "mo": 2592000, "y": 31536000 }

        s = " ".join(slist)
        r = self.re_time.search(s)
        if r is None: return None

        g = r.groups()
        pivot = float(g[1]) * timedict[g[2]]
        cmp = self.oper[g[0]]

        def match(file, variables):
            if os.path.isfile(file):
                t = os.path.getmtime(file)
                tnow = time.time()
                return cmp(t, tnow - pivot)
        return match

# Opens a new process
class ExpressionParser(Parser):

    match_token = ["expression", "expr"]

    def get_match_function(self, slist, target):
        s = " ".join(slist)
        def match(file, variables):
            c = common.replace_variables(s.replace("%file%", pipes.quote(file)), variables)
            try: return subprocess.Popen(c, shell = True).wait() == 0
            except: pass
            return False
        return match


#
#   Regular Expression Parsers
#

class RegexParser(Parser):
    
    match_token = ["regex"]

    def get_regex_flags(self):
        return 0

    def get_match_function(self, slist, target):
        regex = re.compile(" ".join(slist), self.get_regex_flags())
        def match(file, variables):
            f = file.split(os.path.sep)
            if f == []:
                return False
            file = f[-1]
            if file == "" and len(f) > 1:
                file = f[-2]
            if regex.search(file):
                return True 
            return False
        return match


class iRegexParser(RegexParser):

    match_token = ["iregex"]

    def get_regex_flags(self):
        return re.IGNORECASE


class SelfParser(iRegexParser):

    match_token = ["self", "itself"]

    def get_match_function(self, slist, target):
        return RegexParser.get_match_function(self, [target["bookmark"]], target)


class SentenceParser(iRegexParser):

    match_token = ["sentence", "words"]

    def get_match_function(self, slist, target):
        return RegexParser.get_match_function(self, [".*".join(slist)], target)





