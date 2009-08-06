#!/usr/bin/env python
# Command line bookmark tool - shared back-end functions as used by bm
# Copyright 2008, 2009 Bart Spaans


import os
import sys
import btools.common as common
from subprocess import call

# Configuration options
SYSTEM_WIDE_BOOKMARKS = False
BOOKMARK_DATA = ".bookmarks"


def get_conf_location():
    """Returns the location of the bookmark file."""
    c = os.getcwd()
    if os.path.exists(os.path.join(c, BOOKMARK_DATA)):
            return os.path.join(c, BOOKMARK_DATA)
    if not SYSTEM_WIDE_BOOKMARKS:
        if "HOME" in os.environ:
            return os.path.join(os.environ["HOME"],  BOOKMARK_DATA)
        else:
            raise Exception("HOME variable not found in environment.")
    else:
        return BOOKMARK_DATA


def read_bookmarks(file):
    """Returns a (tag, destination) list"""
    f = open(file, "r")
    rawdata = f.readlines()
    f.close()

    res = []
    for r in rawdata:
        s = r.split()
        if len(s) >= 2:
            res.append((" ".join(s[1:]), s[0]))
        elif len(s) == 1:
            res.append(("", s[0]))
    return res

def write_bookmarks(file, bookmarks):
    """Writes a (tag, destination) list to a file."""
    f = open(file, "w")
    for tag, dest in bookmarks:
        f.write("%s %s\n" % (dest, tag))
    f.close()


def get_bookmark(tag, bookmarks):
    """Returns the bookmark(s) fitting 'tag'""" 
    if str.isdigit(tag):
        t = int(tag)
        if 0 <= t < len(bookmarks):
            return [bookmarks[t]]
        else:
            raise Exception("Index out of bounds: %d" % (t))
    possible = []
    for t, dest in bookmarks:
        if t.startswith(tag):
            possible.append((t, dest))
    return possible

def add_bookmark(file, tag, dest):
    """Adds a bookmark to the end of file."""
    f = open(file, "a")
    f.write("%s %s\n" % (dest, tag))
    f.close()


def clear_bookmarks(file):
    write_bookmarks(file, [])


def display_bookmarks(file):
    """Outputs the bookmarks."""
    for i, (tag, dest) in enumerate(read_bookmarks(file)):
        print "%d. %s [%s]" % (i, dest, tag)


def display_colored_bookmarks(file):
    """Outputs colorized bookmarks."""
    t = common.theme
    for i, (tag, dest) in enumerate(read_bookmarks(file)):
        print "%s%d.%s %s %s [%s] %s" % (t[1], i, t[2], dest, t[3], tag, common.NOCOLOR)



def bookmarks_to_symlinks(bookmarks, dest_dir):
    """Makes symbolic links out of tags in dest_dir. 
    If you set CDPATH to dest_dir in your environment,
    the tags will be seemlessly integrated."""

    for tag, src in bookmarks:
        dest = dest_dir + tag
        print "Linking %s to %s." % (dest, src)
        os.symlink(src, dest)



def sync_with_gtk_bookmarks(bm_file, gtk_bm_file):
    pass
