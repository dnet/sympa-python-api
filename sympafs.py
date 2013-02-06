#!/usr/bin/env python

from __future__ import print_function

from errno import ENOENT
from stat import S_IFDIR, S_IFREG
from time import time, mktime

from sympa import Sympa
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn

READ_ONLY = 0555
DOTDOTS = ['.', '..']

class SympaFS(LoggingMixIn, Operations):
    def __init__(self, url, email, passwd, mlist):
        self.sympa = Sympa(url)
        self.email = email
        self.passwd = passwd
        t = time()
        self.attr_cache = {'/': dict(st_mode=(S_IFDIR | READ_ONLY), st_nlink=2,
            st_ctime=t, st_mtime=t, st_atime=t)}
        self.list_cache = {}
        self.content_cache = {}
        self.sympa_login()
        self.mlist = self.sympa.lists[mlist]

    def __del__(self):
        if self.sympa is not None:
            self.sympa.log_out()

    def sympa_login(self):
        self.sympa.log_in(self.email, self.passwd)

    def getattr(self, path, fh=None):
        return self.attr_cache.get(path, self.query_attr(path))

    def query_attr(self, path):
        self.readdir(path.rsplit('/', 1)[0], None)
        try:
            return self.attr_cache[path]
        except KeyError:
            raise FuseOSError(ENOENT)

    def readdir(self, path, fh):
        try:
            return self.list_cache[path]
        except KeyError:
            ls = self.mlist.listdir(path)
            for name, entry in ls.iteritems():
                self.attr_cache[path + '/' + name] = entry2attr(entry)
            dirlist = DOTDOTS + ls.keys()
            self.list_cache[path] = dirlist
            return dirlist

    def read(self, path, size, offset, fh):
        cp = self.content_cache.get(path, self.query_content(path))
        return cp[offset:size+offset]

    def query_content(self, path):
        content = self.mlist.openfile(path).read()
        self.content_cache[path] = content
        return content
    
    access = None
    flush = None
    getxattr = None
    listxattr = None
    open = None
    opendir = None
    release = None
    releasedir = None
    statfs = None

def entry2attr(entry):
    m = (S_IFDIR if entry.is_dir() else S_IFREG) | READ_ONLY
    n = 2 if entry.is_dir() else 1
    t = mktime(entry.updated.timetuple())
    s = 0 if entry.is_dir() else entry.size
    return dict(st_mode=m, st_nlink=n, st_ctime=t,
            st_mtime=t, st_atime=t, st_size=s)

def main():
    from sys import argv, stderr
    if len(argv) != 5:
        print(('Usage: {0} <URL> <e-mail address> <mailing list> '
            '<mountpoint>').format(argv[0]), file=stderr)
        raise SystemExit(1)

    from getpass import getpass
    passwd = getpass()
    _, url, email, mlist, mpoint = argv
    FUSE(SympaFS(url, email, passwd, mlist), mpoint)

if __name__ == "__main__":
    main()
