import os
import re
from hmac import compare_digest
from typing import Callable, Optional, Tuple

__all__ = [
    "ParseHashLineError",
    "CheckHashLineError",
    "HashFileReader",
    "HashFileWriter",
    "format_hash_line",
    "parse_hash_line",
    "generate_hash_line",
    "check_hash_line",
    "re_name_to_hash",
    "re_hash_to_name",
]

_HASH_LINE_RE = re.compile(r"([0-9a-fA-F]+)(?:(?: \*|  | )(.+))?")


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


class HashFileReader:
    """General hash file reader.

    The :class:`HashFileReader` supports the context manager protocol for
    calling :meth:`HashFileReader.close` automatically.

    Parameters
    ----------
    filepath : str or path-like
        The path of a hash file.
    """

    def __init__(self, filepath):
        self.name = filepath
        self.file = open(filepath, "r", encoding="utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Close the underlying file."""

        self.file.close()

    def read_hash_line(self):
        """Read hash line.

        Returns
        -------
        hash_line : str
            A line of *hash* and *name* with GNU Coreutils style.
        """

        while True:
            line = self.file.readline()
            if not line:
                break
            if line.startswith("#") or line.isspace():
                continue
            break
        return line  # empty string for EOF

    def iter(self):
        """Yield hash line.

        Yields
        ------
        hash_line : str
            A line of *hash* and *name* with GNU Coreutils style.
        """

        with self:
            while True:
                hash_line = self.read_hash_line()
                if not hash_line:
                    break
                yield hash_line

    __iter__ = iter

    def iter2(self, *, root=None):
        """Yield hash and name.

        Parameters
        ----------
        root : str, path-like or None, optional
            The root directory.

        Yields
        ------
        hash : str
            The hexadecimal hash value string.
        name : str
            The path of a file or a directory with corresponding hash value.
        """

        for hash_line in self:
            yield parse_hash_line(hash_line, root=root)

    def iter_hash(self):
        """Yield hash.

        Yields
        ------
        hash : str
            The hexadecimal hash value string.
        """

        for entry in self.iter2():
            yield entry[0]

    def iter_name(self, *, root=None):
        """Yield name.

        Parameters
        ----------
        root : str, path-like or None, optional
            The root directory.

        Yields
        ------
        name : str
            The path of a file or a directory with corresponding hash value.
        """

        for entry in self.iter2(root=root):
            yield entry[1]

    def load(self):
        """Return a list of hash line.

        Returns
        -------
        hash_line_list : list
            A list of hash line.
        """

        return list(self)

    def load2(self, *, root=None):
        """Return a list of hash and name.

        Parameters
        ----------
        root : str, path-like or None, optional
            The root directory.

        Returns
        -------
        hash_name_list : list
            A list of hash and name.
        """

        return list(self.iter2(root=root))

    def load_hash(self):
        """Return a list of hash.

        Returns
        -------
        hash_list : list
            A list of hash.
        """

        return list(self.iter_hash())

    def load_name(self, *, root=None):
        """Return a list of name.

        Parameters
        ----------
        root : str, path-like or None, optional
            The root directory.

        Returns
        -------
        name_list : list
            A list of name.
        """

        return list(self.iter_name(root=root))


class HashFileWriter:
    """General hash file writer.

    The :class:`HashFileWriter` supports the context manager protocol for
    calling :meth:`HashFileReader.close` automatically.

    Parameters
    ----------
    filepath : str or path-like
        The path of a hash file.
    """

    def __init__(self, filepath):
        self.name = filepath
        self.file = open(filepath, "w", encoding="utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        """Close the underlying file."""

        self.file.close()

    def write_hash_line(self, hash_line):
        """Write hash line.

        Parameters
        ----------
        hash_line : str
            A line of *hash* and *name* with GNU Coreutils style.
        """

        self.file.write(hash_line)

    def write_comment(self, comment):
        """Write comment.

        Parameters
        ----------
        comment : str
            A line of comment without leading ``#`` and tailing newline.
        """

        self.file.write(f"# {comment}\n")


def format_hash_line(hex_hash_value: str, path: str, *, root: Optional[str] = None) -> str:
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
        root (str | None, default=None):
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


def parse_hash_line(hash_line: str, *, root: Optional[str] = None) -> Tuple[str, str]:
    r"""Parse hash line.

    Parameters:
        hash_line (str):
            A line of *hash* and *name* with GNU Coreutils style.
        root (str | None, default=None):
            The root directory.

    Returns:
        Tuple[str, str]:
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


def generate_hash_line(path: str, hash_function: Callable[[str], bytes], *, root: Optional[str] = None) -> str:
    """Generate hash line.

    Parameters:
        path (str):
            The path of a file or a directory with corresponding hash value.
            Three representations are supported:
            (1) Absolute path;
            (2) Relative path;
            (3) Relative to a given root directory.
        hash_function (Callable[[str], bytes]):
            A function for generating hash value.
        root (str | None, default=None):
            The root directory.

    Returns:
        str:
            ``hash_line``.
    """

    hash_value = hash_function(path)
    hex_hash_value = hash_value.hex()
    return format_hash_line(hex_hash_value, path, root=root)


def check_hash_line(hash_line: str, hash_function: Callable[[str], bytes], *, root: Optional[str] = None) -> str:
    """Check hash line.

    Parameters:
        hash_line (str):
            A line of *hash* and *name* with GNU Coreutils style.
        hash_function (Callable[[str], bytes]):
            A function for generating hash value.
        root (str | None, default=None):
            The root directory.

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


def _parse_for_re(hash_line, *, root=None):
    hex_hash_value, naming_path = parse_hash_line(hash_line, root=root)
    hashing_path = os.path.join(os.path.dirname(naming_path), hex_hash_value)
    return hashing_path, naming_path


def re_name_to_hash(hash_line, *, root=None):
    """Re name to hash.

    Parameters
    ----------
    hash_line : str
        A line of *hash* and *name* with GNU Coreutils style.
    root : str, path-like or None, optional
        The root directory.

    Returns
    -------
    naming_path : str
        The naming (source) path.
    hashing_path : str
        The hashing (destination) path.
    """

    hashing_path, naming_path = _parse_for_re(hash_line, root=root)
    os.rename(naming_path, hashing_path)
    return naming_path, hashing_path


def re_hash_to_name(hash_line, *, root=None):
    """Re hash to name.

    Parameters
    ----------
    hash_line : str
        A line of *hash* and *name* with GNU Coreutils style.
    root : str, path-like or None, optional
        The root directory.

    Returns
    -------
    hashing_path : str
        The hashing (source) path.
    naming_path : str
        The naming (destination) path.
    """

    hashing_path, naming_path = _parse_for_re(hash_line, root=root)
    os.rename(hashing_path, naming_path)
    return hashing_path, naming_path
