import glob
import locale
import os

from . import _check_int, _check_str

__all__ = [
    "glob_scanner",
    "glob_filter",
    "glob_scanners",
    "glob_filters",
    "sorted_locale",
]

_ESCAPE_SQUARE = glob.escape("[")
_ESCAPE_SQUARE_BYTES = glob.escape(b"[")


def _expand(pathname, *, user=False, vars=False):
    pathname = os.fspath(pathname)
    if user:
        pathname = os.path.expanduser(pathname)
    if vars:
        pathname = os.path.expandvars(pathname)
    return pathname


def _glob0(pathname, *, recursive=False, user=False, vars=False):
    yield _expand(pathname, user=user, vars=vars)


def _glob1(pathname, *, recursive=False, user=False, vars=False):
    pathname = _expand(pathname, user=user, vars=vars)
    if isinstance(pathname, bytes):
        pathname = pathname.replace(b"[", _ESCAPE_SQUARE_BYTES)
    else:
        pathname = pathname.replace("[", _ESCAPE_SQUARE)
    yield from glob.iglob(pathname, recursive=recursive)


def _glob2(pathname, *, recursive=False, user=False, vars=False):
    pathname = _expand(pathname, user=user, vars=vars)
    yield from glob.iglob(pathname, recursive=recursive)


def _get_glob(mode):
    _check_int(mode, "mode")
    if mode == 0:
        return _glob0
    elif mode == 1:
        return _glob1
    elif mode == 2:
        return _glob2
    else:
        raise ValueError(f"mode must be in {{0, 1, 2}}, got {mode}")


def _path_filter(pathnames, *, type):
    _check_str(type, "type")
    if type == "a":
        yield from filter(os.path.exists, pathnames)
    elif type == "d":
        yield from filter(os.path.isdir, pathnames)
    elif type == "f":
        yield from filter(os.path.isfile, pathnames)
    else:
        raise ValueError(f"type must be in {{'a', 'd', 'f'}}, got '{type}'")


def glob_scanner(pathname, *, mode=1, recursive=False, user=False, vars=False):
    """Match a pathname with glob patterns.

    Parameters
    ----------
    pathname : str, bytes or path-like
        A pathname with glob patterns.
    mode : int, default=1
        The mode of glob. If ``0``, disable globbing; if ``1``, resolve ``*``
        and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    recursive : bool, default=False
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.
    user : bool, default=False
        If ``True``, user home directory will be expanded.
    vars : bool, default=False
        If ``True``, environment variables will be expanded.

    Yields
    ------
    matched_pathname : str or bytes
        The matched pathname.
    """

    glob = _get_glob(mode)
    yield from glob(pathname, recursive=recursive, user=user, vars=vars)


def glob_filter(pathname, *, mode=1, type="a", recursive=False, user=False, vars=False):
    """Match and filter a pathname with glob patterns.

    Parameters
    ----------
    pathname : str, bytes or path-like
        A pathname with glob patterns.
    mode : int, default=1
        The mode of glob. If ``0``, disable globbing; if ``1``, resolve ``*``
        and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    type : str, default='a'
        The type of file. If ``a``, include all types; if ``d``, include
        directories; if ``f``, include files.
    recursive : bool, default=False
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.
    user : bool, default=False
        If ``True``, user home directory will be expanded.
    vars : bool, default=False
        If ``True``, environment variables will be expanded.

    Yields
    ------
    matched_pathname : str or bytes
        The matched pathname with the given file type.
    """

    matched = glob_scanner(
        pathname, mode=mode, recursive=recursive, user=user, vars=vars
    )
    yield from _path_filter(matched, type=type)


def glob_scanners(pathnames, *, mode=1, recursive=False, user=False, vars=False):
    """Match a list of pathnames with glob patterns.

    Parameters
    ----------
    pathnames : iterable of str, bytes or path-like
        A list of pathnames with glob patterns.
    mode : int, default=1
        The mode of glob. If ``0``, disable globbing; if ``1``, resolve ``*``
        and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    recursive : bool, default=False
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.
    user : bool, default=False
        If ``True``, user home directory will be expanded.
    vars : bool, default=False
        If ``True``, environment variables will be expanded.

    Yields
    ------
    matched_pathname : str or bytes
        The matched pathname.
    """

    glob = _get_glob(mode)
    for pathname in pathnames:
        yield from glob(pathname, recursive=recursive, user=user, vars=vars)


def glob_filters(
    pathnames, *, mode=1, type="a", recursive=False, user=False, vars=False
):
    """Match and filter a list of pathnames with glob patterns.

    Parameters
    ----------
    pathnames : iterable of str, bytes or path-like
        A list of pathnames with glob patterns.
    mode : int, default=1
        The mode of glob. If ``0``, disable globbing; if ``1``, resolve ``*``
        and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    type : str, default='a'
        The type of file. If ``a``, include all types; if ``d``, include
        directories; if ``f``, include files.
    recursive : bool, default=False
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.
    user : bool, default=False
        If ``True``, user home directory will be expanded.
    vars : bool, default=False
        If ``True``, environment variables will be expanded.

    Yields
    ------
    matched_pathname : str or bytes
        The matched pathname with the given file type.
    """

    matched = glob_scanners(
        pathnames, mode=mode, recursive=recursive, user=user, vars=vars
    )
    yield from _path_filter(matched, type=type)


def sorted_locale(iterable, *, reverse=False):
    """Sort a list of strings according to locale.

    Parameters
    ----------
    iterable : iterable of str
        A list of strings.
    reverse : bool, default=False
        If ``True``, reverse the sorted result.

    Returns
    -------
    sorted_list : list
        The sorted list of strings.
    """

    return sorted(iterable, key=locale.strxfrm, reverse=reverse)
