import glob
import os

from . import _check_int, _check_str

__all__ = ["glob_scanner", "glob_filter", "glob_scanners", "glob_filters"]

_ESCAPE_SQUARE = glob.escape("[")


def _glob0(pathname, recursive=False):
    yield os.fspath(pathname)


def _glob1(pathname, recursive=False):
    # Escape all square brackets to prevent glob from resolving them.
    pathname = os.fspath(pathname).replace("[", _ESCAPE_SQUARE)
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


def _get_glob_type(type):
    _check_str(type, "type")
    type = type.lower()
    if type not in {"a", "d", "f"}:
        raise ValueError(f"type must be in {{'a', 'd', 'f'}}, got '{type}'")

    all_ok = type == "a"
    dir_ok = all_ok or type == "d"
    file_ok = all_ok or type == "f"
    return all_ok, dir_ok, file_ok


def glob_scanner(pathname, *, mode=1, recursive=False):
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
        The glob matched pathname.
    """

    glob_func = _get_glob_func(mode)
    yield from glob_func(pathname, recursive=recursive)


def glob_filter(pathname, *, mode=1, recursive=False, type="a"):
    """Resolve and filter a pathname with glob patterns.

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
    type : str, default='a'
        The type of file. If ``a``, include all types; if ``d``, include
        directories; if ``f``, include files.

    Yields
    ------
    matched_pathname : str
        The glob matched pathname.
    """

    all_ok, dir_ok, file_ok = _get_glob_type(type)
    for path in glob_scanner(pathname, mode=mode, recursive=recursive):
        if os.path.isdir(path):
            if dir_ok:
                yield path
        elif os.path.isfile(path):
            if file_ok:
                yield path
        else:
            if all_ok:
                yield path


def glob_scanners(pathnames, *, mode=1, recursive=False):
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
        The glob matched pathname.
    """

    glob_func = _get_glob_func(mode)
    for pathname in pathnames:
        yield from glob_func(pathname, recursive=recursive)


def glob_filters(pathnames, *, mode=1, recursive=False, type="a"):
    """Resolve and filter a list of pathnames with glob patterns.

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
    type : str, default='a'
        The type of file. If ``a``, include all types; if ``d``, include
        directories; if ``f``, include files.

    Yields
    ------
    matched_pathname : str
        The glob matched pathname.
    """

    all_ok, dir_ok, file_ok = _get_glob_type(type)
    for path in glob_scanners(pathnames, mode=mode, recursive=recursive):
        if os.path.isdir(path):
            if dir_ok:
                yield path
        elif os.path.isfile(path):
            if file_ok:
                yield path
        else:
            if all_ok:
                yield path
