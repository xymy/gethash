import glob
import os

__all__ = ["glob_resolver", "glob_scanner"]


def glob_resolver(pathname, *, mode=1, recursive=False):
    """Resolve glob pathname.

    Parameters
    ----------
    pathname : str or path-like
        A pathname with glob pattern.
    mode : int, optional (default: 1)
        The mode of glob. If ``0``, disable glob pathname pattern; if ``1``,
        resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    recursive : bool, optional (default: False)
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.

    Yields
    ------
    path : str
        The matched path.
    """

    pathname = os.fspath(pathname)
    if mode == 0:
        yield pathname
    elif mode == 1:
        pathname = pathname.replace("[", glob.escape("["))
        yield from glob.iglob(pathname, recursive=recursive)
    elif mode == 2:
        yield from glob.iglob(pathname, recursive=recursive)
    else:
        raise ValueError("invalid mode {}".format(mode))


def glob_scanner(pathnames, *, mode=1, recursive=False):
    """Resolve a list of glob pathnames.

    Parameters
    ----------
    pathnames : str or path-like
        A list of pathnames with glob pattern.
    mode : int, optional (default: 1)
        The mode of glob. If ``0``, disable glob pathname pattern; if ``1``,
        resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    recursive : bool, optional (default: False)
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.

    Yields
    ------
    path : str
        The matched path.
    """

    for pathname in pathnames:
        yield from glob_resolver(pathname, mode=mode, recursive=recursive)
