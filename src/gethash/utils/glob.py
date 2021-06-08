import glob
import locale
import os
from os import PathLike
from typing import Any, AnyStr, Callable, Iterable, Iterator, List, Union

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


def _expand(
    path: Union[AnyStr, PathLike[AnyStr]], *, user: bool = False, vars: bool = False
) -> AnyStr:
    path = os.fspath(path)
    if user:
        path = os.path.expanduser(path)
    if vars:
        path = os.path.expandvars(path)
    return path


def _glob0(
    path: Union[AnyStr, PathLike[AnyStr]],
    *,
    recursive: bool = False,
    user: bool = False,
    vars: bool = False,
) -> Iterator[AnyStr]:
    yield _expand(path, user=user, vars=vars)


def _glob1(
    path: Union[AnyStr, PathLike[AnyStr]],
    *,
    recursive: bool = False,
    user: bool = False,
    vars: bool = False,
) -> Iterator[AnyStr]:
    path = _expand(path, user=user, vars=vars)
    if isinstance(path, bytes):
        path = path.replace(b"[", _ESCAPE_SQUARE_BYTES)
    else:
        path = path.replace("[", _ESCAPE_SQUARE)
    yield from glob.iglob(path, recursive=recursive)


def _glob2(
    path: Union[AnyStr, PathLike[AnyStr]],
    *,
    recursive: bool = False,
    user: bool = False,
    vars: bool = False,
) -> Iterator[AnyStr]:
    path = _expand(path, user=user, vars=vars)
    yield from glob.iglob(path, recursive=recursive)


# TODO: Callable[..., Iterator[AnyStr]]
def _get_glob(mode: int) -> Callable[..., Iterator[Any]]:
    _check_int(mode, "mode")
    if mode == 0:
        return _glob0
    elif mode == 1:
        return _glob1
    elif mode == 2:
        return _glob2
    else:
        raise ValueError(f"mode must be in {{0, 1, 2}}, got {mode}")


def _path_filter(
    paths: Iterable[Union[AnyStr, PathLike[AnyStr]]], *, type: str
) -> Iterator[AnyStr]:
    _check_str(type, "type")
    if type == "a":
        pred = os.path.exists
    elif type == "d":
        pred = os.path.isdir  # type: ignore
    elif type == "f":
        pred = os.path.isfile  # type: ignore
    else:
        raise ValueError(f"type must be in {{'a', 'd', 'f'}}, got '{type}'")
    yield from (os.fspath(path) for path in paths if pred(path))


def glob_scanner(
    path: Union[AnyStr, PathLike[AnyStr]],
    *,
    mode: int = 1,
    recursive: bool = False,
    user: bool = False,
    vars: bool = False,
) -> Iterator[AnyStr]:
    """Match a path with glob patterns.

    Parameters
    ----------
    path : str, bytes or path-like
        A path with glob patterns.
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
    matched_path : str or bytes
        The matched path.
    """

    glob = _get_glob(mode)
    yield from glob(path, recursive=recursive, user=user, vars=vars)


def glob_filter(
    path: Union[AnyStr, PathLike[AnyStr]],
    *,
    mode: int = 1,
    type: str = "a",
    recursive: bool = False,
    user: bool = False,
    vars: bool = False,
) -> Iterator[AnyStr]:
    """Match and filter a path with glob patterns.

    Parameters
    ----------
    path : str, bytes or path-like
        A path with glob patterns.
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
    matched_path : str or bytes
        The matched path with the given file type.
    """

    matched = glob_scanner(path, mode=mode, recursive=recursive, user=user, vars=vars)
    yield from _path_filter(matched, type=type)


def glob_scanners(
    paths: Iterable[Union[AnyStr, PathLike[AnyStr]]],
    *,
    mode: int = 1,
    recursive: bool = False,
    user: bool = False,
    vars: bool = False,
) -> Iterator[AnyStr]:
    """Match a list of paths with glob patterns.

    Parameters
    ----------
    paths : iterable of str, bytes or path-like
        A list of paths with glob patterns.
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
    matched_path : str or bytes
        The matched path.
    """

    glob = _get_glob(mode)
    for path in paths:
        yield from glob(path, recursive=recursive, user=user, vars=vars)


def glob_filters(
    paths: Iterable[Union[AnyStr, PathLike[AnyStr]]],
    *,
    mode: int = 1,
    type: str = "a",
    recursive: bool = False,
    user: bool = False,
    vars: bool = False,
) -> Iterator[AnyStr]:
    """Match and filter a list of paths with glob patterns.

    Parameters
    ----------
    paths : iterable of str, bytes or path-like
        A list of paths with glob patterns.
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
    matched_path : str or bytes
        The matched path with the given file type.
    """

    matched = glob_scanners(paths, mode=mode, recursive=recursive, user=user, vars=vars)
    yield from _path_filter(matched, type=type)


def sorted_locale(iterable: Iterable[str], *, reverse: bool = False) -> List[str]:
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
