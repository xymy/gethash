import glob
import locale
import os

from . import _check_int, _check_str

__all__ = ["glob_scanner", "glob_filter", "glob_scanners", "glob_filters", "sorted_locale"]

_ESCAPE_SQUARE = glob.escape("[")


def _glob0(pathname, *, recursive=False):
    yield os.fspath(pathname)


def _glob1(pathname, *, recursive=False):
    # Escape all square brackets to prevent glob from resolving them.
    pathname = os.fspath(pathname).replace("[", _ESCAPE_SQUARE)
    yield from glob.iglob(pathname, recursive=recursive)


def _glob2(pathname, *, recursive=False):
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
    all_ok = False
    dir_ok = False
    file_ok = False
    link_ok = False
    for t in set(type.lower()):
        if t == "a":
            all_ok = True
        elif t == "d":
            dir_ok = True
        elif t == "f":
            file_ok = True
        elif t == "l":
            link_ok = True
        else:
            raise ValueError(f"type must be in {{'a', 'd', 'f', 'l'}}, got '{t}'")

    if all_ok:
        yield from pathnames
    else:
        for path in pathnames:
            # Detect symlink first to avoid following symbolic links.
            if os.path.islink(path):
                if link_ok:
                    yield path
            elif os.path.isdir(path):
                if dir_ok:
                    yield path
            elif os.path.isfile(path):
                if file_ok:
                    yield path
            else:
                raise ValueError(f"unexpected file type for path '{path}'")


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

    glob = _get_glob(mode)
    yield from glob(pathname, recursive=recursive)


def glob_filter(pathname, *, mode=1, type="a", recursive=False):
    """Resolve and filter a pathname with glob patterns.

    Parameters
    ----------
    pathname : str or path-like
        A pathname with glob patterns.
    mode : int, default=1
        The mode of glob. If ``0``, disable glob pathname pattern; if ``1``,
        resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    type : str, default='a'
        The type of file. If ``a``, include all types; if ``d``, include
        directories; if ``f``, include files; if ``l``, includes symbolic links.
    recursive : bool, default=False
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.

    Yields
    ------
    matched_pathname : str
        The glob matched pathname with the given file type.
    """

    generator = glob_scanner(pathname, mode=mode, recursive=recursive)
    yield from _path_filter(generator, type=type)


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

    glob = _get_glob(mode)
    for pathname in pathnames:
        yield from glob(pathname, recursive=recursive)


def glob_filters(pathnames, *, mode=1, type="a", recursive=False):
    """Resolve and filter a list of pathnames with glob patterns.

    Parameters
    ----------
    pathnames : iterable of str or path-like
        A list of pathnames with glob patterns.
    mode : int, default=1
        The mode of glob. If ``0``, disable glob pathname pattern; if ``1``,
        resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    type : str, default='a'
        The type of file. If ``a``, include all types; if ``d``, include
        directories; if ``f``, include files; if ``l``, includes symbolic links.
    recursive : bool, default=False
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.

    Yields
    ------
    matched_pathname : str
        The glob matched pathname with the given file type.
    """

    generator = glob_scanners(pathnames, mode=mode, recursive=recursive)
    yield from _path_filter(generator, type=type)


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
