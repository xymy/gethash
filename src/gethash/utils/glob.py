from __future__ import annotations

import glob
import os
from collections.abc import Iterable, Iterator
from typing import Any, AnyStr, Callable

from natsort import os_sort_keygen

_ESCAPE_SQUARE = glob.escape("[")
_ESCAPE_SQUARE_BYTES = glob.escape(b"[")

_HASH_SUFFIXES = (
    ".blake2b",
    ".blake2s",
    ".crc32",
    ".md2",
    ".md4",
    ".md5",
    ".ripemd160",
    ".sha1",
    ".sha256",
    ".sha512",
    ".sha3_256",
    ".sha3_512",
    ".sm3",
)


def expand_path(path: AnyStr, *, user: bool = False, vars: bool = False) -> AnyStr:
    """Expand user home directory and environment variables.

    Parameters:
        path (AnyStr):
            The path.
        user (bool, default=False):
            If ``True``, expand user home directory.
        vars (bool, default=False):
            If ``True``, expand environment variables.

    Returns:
        AnyStr:
            The expanded path.
    """

    if user:
        path = os.path.expanduser(path)
    if vars:
        path = os.path.expandvars(path)
    return os.path.normpath(path)


def _glob0(path: AnyStr, *, recursive: bool = False, user: bool = False, vars: bool = False) -> Iterator[AnyStr]:
    yield expand_path(path, user=user, vars=vars)


def _glob1(path: AnyStr, *, recursive: bool = False, user: bool = False, vars: bool = False) -> Iterator[AnyStr]:
    path = expand_path(path, user=user, vars=vars)
    if isinstance(path, bytes):
        path = path.replace(b"[", _ESCAPE_SQUARE_BYTES)
    else:
        path = path.replace("[", _ESCAPE_SQUARE)
    yield from glob.iglob(path, recursive=recursive)


def _glob2(path: AnyStr, *, recursive: bool = False, user: bool = False, vars: bool = False) -> Iterator[AnyStr]:
    path = expand_path(path, user=user, vars=vars)
    yield from glob.iglob(path, recursive=recursive)


def _get_glob(mode: int) -> Callable[..., Iterator]:
    if mode == 0:
        return _glob0
    elif mode == 1:
        return _glob1
    elif mode == 2:
        return _glob2
    else:
        raise ValueError(f"mode must be in {{0, 1, 2}}, got {mode!r}")


def _path_filter(paths: Iterable[AnyStr], *, type: str) -> Iterator[AnyStr]:
    pred: Callable[[str | bytes], bool]
    if type == "a":
        pred = os.path.exists
    elif type == "d":
        pred = os.path.isdir
    elif type == "f":
        pred = os.path.isfile
    else:
        raise ValueError(f"type must be in {{'a', 'd', 'f'}}, got {type!r}")
    yield from filter(pred, paths)


def glob_scanners(
    paths: Iterable[AnyStr], *, mode: int = 1, recursive: bool = False, user: bool = False, vars: bool = False
) -> Iterator[AnyStr]:
    """Match a list of paths with glob patterns.

    Parameters:
        paths (Iterable[AnyStr]):
            A list of paths with glob patterns.
        mode (int, default=1):
            The mode of glob. If ``0``, disable globbing; if ``1``, resolve
            ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
        recursive (bool, default=False):
            If ``True``, the pattern ``**`` will match any files and zero or
            more directories, subdirectories and symbolic links to directories.
        user (bool, default=False):
            If ``True``, user home directory will be expanded.
        vars (bool, default=False):
            If ``True``, environment variables will be expanded.

    Yields:
        AnyStr:
            The matched path.
    """

    glob = _get_glob(mode)
    for path in paths:
        yield from glob(path, recursive=recursive, user=user, vars=vars)


def glob_filters(
    paths: Iterable[AnyStr],
    *,
    mode: int = 1,
    type: str = "a",
    recursive: bool = False,
    user: bool = False,
    vars: bool = False,
) -> Iterator[AnyStr]:
    """Match and filter a list of paths with glob patterns.

    Parameters:
        paths (Iterable[AnyStr]):
            A list of paths with glob patterns.
        mode (int, default=1):
            The mode of glob. If ``0``, disable globbing; if ``1``, resolve
            ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
        type (str, default='a'):
            The type of file. If ``a``, include all types; if ``d``, include
            directories; if ``f``, include files.
        recursive (bool, default=False):
            If ``True``, the pattern ``**`` will match any files and zero or
            more directories, subdirectories and symbolic links to directories.
        user (bool, default=False):
            If ``True``, user home directory will be expanded.
        vars (bool, default=False):
            If ``True``, environment variables will be expanded.

    Yields:
        AnyStr:
            The matched path with the given file type.
    """

    matched = glob_scanners(paths, mode=mode, recursive=recursive, user=user, vars=vars)
    yield from _path_filter(matched, type=type)


def auto_glob(roots: Iterable[str]) -> Iterator[str]:
    for root in roots:
        for dirpath, _dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.lower().endswith(_HASH_SUFFIXES):
                    yield os.path.join(dirpath, filename)


def sorted_path(
    iterable: Iterable[AnyStr], *, key: Callable[[AnyStr], Any] | None = None, reverse: bool = False
) -> list[AnyStr]:
    """Sort a list of path strings the same as the underlying operating system.

    Parameters:
        iterable (Iterable[AnyStr]):
            A list of path strings.
        key (Callable[[AnyStr], Any] | None, default=None):
            The same parameter as :func:`sorted`.
        reverse (bool, default=False):
            The same parameter as :func:`sorted`.

    Returns:
        list[AnyStr]:
            The sorted list of path strings.
    """

    dirs = []
    files = []
    for path in iterable:
        if os.path.isdir(path):
            dirs.append(path)
        else:
            files.append(path)

    key = os_sort_keygen(key)
    dirs.sort(key=key, reverse=reverse)
    files.sort(key=key, reverse=reverse)

    if reverse:
        return files + dirs
    else:
        return dirs + files
