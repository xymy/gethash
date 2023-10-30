from __future__ import annotations

import os
import re
from collections.abc import Iterator
from hmac import compare_digest
from pathlib import Path
from typing import Any, Callable

from typing_extensions import Self

_HASH_LINE_RE = re.compile(r"([0-9a-fA-F]+)(?: \*|  | )(.+)")


class ParseHashLineError(ValueError):
    """Raised by :func:`parse_hash_line`."""

    def __init__(self, hash_line: str) -> None:
        super().__init__(hash_line)
        self.hash_line = hash_line


class CheckHashLineError(ValueError):
    """Raised by :func:`check_hash_line`."""

    def __init__(self, hash_line: str, hash_value: bytes, path: str, curr_hash_value: bytes) -> None:
        super().__init__(hash_line, hash_value, path, curr_hash_value)
        self.hash_line = hash_line
        self.hash_value = hash_value
        self.path = path
        self.curr_hash_value = curr_hash_value


def format_hash_line(hex_hash_value: str, path: str, *, root: str | Path | None = None) -> str:
    r"""Format hash line.

    Parameters:
        hex_hash_value (str):
            The hexadecimal hash value string.
        path (str):
            The path of a file or a directory with corresponding hash value.
            Three representations are supported:
            (1) Absolute path;
            (2) Relative path;
            (3) Relative to a given root directory.
        root (str | Path | None, default=None):
            The root directory.

    Returns:
        str:
            ``hash_line``.

    Examples:
        >>> format_hash_line('d41d8cd98f00b204e9800998ecf8427e', 'foo.txt')
        'd41d8cd98f00b204e9800998ecf8427e *foo.txt\n'
    """

    if root is not None:
        path = os.path.relpath(path, root)
    path = os.path.normpath(path)
    return f"{hex_hash_value} *{path}\n"


def parse_hash_line(hash_line: str, *, root: str | Path | None = None) -> tuple[str, str]:
    r"""Parse hash line.

    Parameters:
        hash_line (str):
            The line of *hash* and *name* with GNU Coreutils style.
        root (str | Path | None, default=None):
            The root directory.

    Raises:
        ParseHashLineError:
            If fails to parse hash line.

    Returns:
        tuple[str, str]:
            ``(hex_hash_value, path)``.

    Examples:
        >>> parse_hash_line('d41d8cd98f00b204e9800998ecf8427e *foo.txt\n')
        ('d41d8cd98f00b204e9800998ecf8427e', 'foo.txt')
    """

    m = _HASH_LINE_RE.match(hash_line)
    if m is None:
        raise ParseHashLineError(hash_line)
    hex_hash_value, path = m.groups()
    if root is not None:
        path = os.path.join(root, path)
    path = os.path.normpath(path)
    return hex_hash_value, path


def generate_hash_line(path: str, hash_function: Callable[[str], bytes], *, root: str | Path | None = None) -> str:
    """Generate hash line.

    Parameters:
        path (str):
            The path of a file or a directory with corresponding hash value.
            Three representations are supported:
            (1) Absolute path;
            (2) Relative path;
            (3) Relative to a given root directory.
        hash_function (Callable[[str], bytes]):
            The function used to generate hash value.
        root (str | Path | None, default=None):
            The root directory.

    Returns:
        str:
            ``hash_line``.
    """

    hash_value = hash_function(path)
    hex_hash_value = hash_value.hex()
    return format_hash_line(hex_hash_value, path, root=root)


def check_hash_line(hash_line: str, hash_function: Callable[[str], bytes], *, root: str | Path | None = None) -> str:
    """Check hash line.

    Parameters:
        hash_line (str):
            The line of *hash* and *name* with GNU Coreutils style.
        hash_function (Callable[[str], bytes]):
            The function used to generate hash value.
        root (str | Path | None, default=None):
            The root directory.

    Raises:
        CheckHashLineError:
            If fails to check hash line.

    Returns:
        str:
            ``path``.
    """

    hex_hash_value, path = parse_hash_line(hash_line, root=root)
    hash_value = bytes.fromhex(hex_hash_value)
    curr_hash_value = hash_function(path)
    if not compare_digest(hash_value, curr_hash_value):
        raise CheckHashLineError(hash_line, hash_value, path, curr_hash_value)
    return path


class HashFileReader:
    """General hash file reader.

    The :class:`HashFileReader` supports the context manager protocol for
    calling :meth:`HashFileReader.close` automatically.

    Parameters:
        filepath (str | Path):
            The path of a hash file.

    Note:
        - ``hash_line``: The line of *hash* and *name* with GNU Coreutils style.
        - ``hash``: The hexadecimal hash value string.
        - ``name``: The path of a file or a directory with corresponding hash value.
    """

    def __init__(self, filepath: str | Path) -> None:
        self.name = str(filepath)
        self.file = open(filepath, encoding="utf-8")  # noqa: SIM115

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying file."""

        self.file.close()

    def read_hash_line(self) -> str:
        """Read hash line.

        Returns:
            str:
                ``hash_line``.
        """

        while line := self.file.readline():
            # Skip comments and blank lines.
            if not (line.startswith("#") or line.isspace()):
                break
        return line  # empty string for EOF

    def iter(self) -> Iterator[str]:
        """Yield hash line.

        Yields:
            str:
                ``hash_line``.

        Note:
            :meth:`HashFileReader.__iter__` is an alias of this method.
        """

        with self:
            while hash_line := self.read_hash_line():
                yield hash_line

    __iter__ = iter

    def iter2(self, *, root: str | Path | None = None) -> Iterator[tuple[str, str]]:
        """Yield hash and name.

        Parameters:
            root (str | Path | None, default=None):
                The root directory.

        Yields:
            tuple[str, str]:
                ``(hash, name)``.
        """

        for hash_line in self:
            yield parse_hash_line(hash_line, root=root)

    def iter_hash(self, *, root: str | Path | None = None) -> Iterator[str]:
        """Yield hash.

        Parameters:
            root (str | Path | None, default=None):
                The root directory.

        Yields:
            str:
                ``hash``.
        """

        for entry in self.iter2(root=root):
            yield entry[0]

    def iter_name(self, *, root: str | Path | None = None) -> Iterator[str]:
        """Yield name.

        Parameters:
            root (str | Path | None, default=None):
                The root directory.

        Yields:
            str:
                ``name``.
        """

        for entry in self.iter2(root=root):
            yield entry[1]


class HashFileWriter:
    """General hash file writer.

    The :class:`HashFileWriter` supports the context manager protocol for
    calling :meth:`HashFileWriter.close` automatically.

    Parameters:
        filepath (str | Path):
            The path of a hash file.
    """

    def __init__(self, filepath: str | Path) -> None:
        self.name = str(filepath)
        self.file = open(filepath, "w", encoding="utf-8")  # noqa: SIM115

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying file."""

        self.file.close()

    def write_hash_line(self, hash_line: str) -> None:
        """Write hash line.

        Parameters:
            hash_line (str):
                The line of *hash* and *name* with GNU Coreutils style.
        """

        self.file.write(hash_line)
