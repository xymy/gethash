import glob
import os


def glob_resolver(pathname, *, mode=0, recursive=False):
    pathname = os.fspath(pathname)
    if mode == 0:
        yield pathname
    elif mode == 1:
        pathname = pathname.replace('[', glob.escape('['))
        yield from glob.iglob(pathname, recursive=recursive)
    elif mode == 2:
        yield from glob.iglob(pathname, recursive=recursive)
    else:
        raise ValueError("invalid mode {}".format(mode))


def glob_scanner(pathnames, *, mode=0, recursive=False):
    for pathname in pathnames:
        for path in glob_resolver(pathname, mode=mode, recursive=recursive):
            yield path
