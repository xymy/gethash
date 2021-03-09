import glob
import os

from . import _check_int

__all__ = ["glob_resolver", "glob_scanner"]

_ESCAPE_SQUARE = glob.escape("[")


def _glob0(pathname, recursive=False):
    yield pathname


def _glob1(pathname, recursive=False):
    pathname = os.fspath(pathname)
    # Escape all square brackets to prevent glob from resolving them.
    pathname = pathname.replace("[", _ESCAPE_SQUARE)
    yield from glob.iglob(pathname, recursive=recursive)


def _glob2(pathname, recursive=False):
    yield from glob.iglob(pathname, recursive=recursive)


def _get_glob_func(mode):
    _check_int(mode, "mode")
    if mode == 0:
        return _glob0
    elif mode == 1:
        return _glob1
    elif mode == 2:
        return _glob2
    else:
        raise ValueError(f"mode must be in {{0, 1, 2}}, got {mode}")


def glob_resolver(pathname, *, mode=1, recursive=False):
    """Resolve a pathname with glob patterns.

    Parameters
    ----------
    pathname : str or path-like
        A pathname with glob patterns.
    mode : int, default=1
        The mode of glob. If ``0``, disable glob pathname pattern; if ``1``,
        resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    recursive : bool, default=False
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.

    Yields
    ------
    matched_pathname : str
        The matched pathname.
    """

    glob_func = _get_glob_func(mode)
    yield from glob_func(pathname, recursive=recursive)


def glob_scanner(pathnames, *, mode=1, recursive=False):
    """Resolve a list of pathnames with glob patterns.

    Parameters
    ----------
    pathnames : iterable of str or path-like
        A list of pathnames with glob patterns.
    mode : int, default=1
        The mode of glob. If ``0``, disable glob pathname pattern; if ``1``,
        resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    recursive : bool, default=False
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.

    Yields
    ------
    matched_pathname : str
        The matched pathname.
    """

    glob_func = _get_glob_func(mode)
    for pathname in pathnames:
        yield from glob_func(pathname, recursive=recursive)
