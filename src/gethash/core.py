import io
import os
import re
from hmac import compare_digest

from tqdm import tqdm

from .utils.strxor import strxor

__all__ = [
    "IsADirectory",
    "ParseHashLineError",
    "CheckHashLineError",
    "Hasher",
    "HashFileReader",
    "HashFileWriter",
    "format_hash_line",
    "parse_hash_line",
    "generate_hash_line",
    "check_hash_line",
]

_CHUNKSIZE = 0x100000  # 1 MB
_HASH_LINE_RE = re.compile(r"([0-9a-fA-F]+) (?:\*| )?(.+)")


class IsADirectory(OSError):
    """Raised by method `Hasher.calc_hash`."""


class ParseHashLineError(ValueError):
    """Raised by function `parse_hash_line`."""


class CheckHashLineError(ValueError):
    """Raised by function `check_hash_line`."""

    def __init__(self, hash_line, hash_value, path, curr_hash_value):
        super().__init__(hash_line, hash_value, path, curr_hash_value)
        self.hash_line = hash_line
        self.hash_value = hash_value
        self.path = path
        self.curr_hash_value = curr_hash_value


class Hasher(object):
    """General hash value generator.

    Generate hash values using given hash context prototype. A progressbar
    based on ``tqdm`` is also available.

    Parameters
    ----------
    ctx_proto : hash context
        The hash context prototype used to generate hash values.
    chunksize : int or None, optional (default: None)
        The size of data blocks when reading data from files.
    tqdm_args : dict or None, optional (default: None)
        The arguments passed to the underlying ``tqdm`` constructor.
    """

    def __init__(self, ctx_proto, *, chunksize=None, tqdm_args=None):
        # We use the copies of parameters for avoiding potential side-effects.
        self.ctx_proto = ctx_proto.copy()
        self.chunksize = _CHUNKSIZE if chunksize is None else int(chunksize)
        self.tqdm_args = {} if tqdm_args is None else dict(tqdm_args)
        # Set the unit of iterations as byte.
        self.tqdm_args.setdefault("unit", "B")
        self.tqdm_args.setdefault("unit_scale", True)
        self.tqdm_args.setdefault("unit_divisor", 1024)

    def hash_f(self, filepath, start=None, stop=None):
        """Return the hash value of a file.

        Parameters
        ----------
        filepath : str or path-like
            The path of a file.
        start : int or None, optional (default: None)
            The start offset of the file.
        stop : int or None, optional (default: None)
            The stop offset of the file.

        Returns
        -------
        hash_value : bytes
            The hash value of the file.
        """

        # Decide the range of current file. Use (0, filesize) by default.
        # The (start, stop) will be shrinked to (0, filesize) if necessary.
        filesize = os.path.getsize(filepath)
        if start is None or start < 0:
            start = 0
        if stop is None or stop > filesize:
            stop = filesize
        if start > stop:
            raise ValueError("require start <= stop, but {} > {}".format(start, stop))

        ctx = self.ctx_proto.copy()
        chunksize = self.chunksize
        total = stop - start
        with tqdm(total=total, **self.tqdm_args) as bar, open(filepath, "rb") as f:
            # Precompute chunk count and remaining size.
            count, remainsize = divmod(total, chunksize)
            f.seek(start, io.SEEK_SET)
            for _ in range(count):
                chunk = f.read(chunksize)
                ctx.update(chunk)
                bar.update(chunksize)
            remain = f.read(remainsize)
            ctx.update(remain)
            bar.update(remainsize)
        return ctx.digest()

    def hash_d(self, dirpath, start=None, stop=None):
        """Return the hash value of a directory.

        Parameters
        ----------
        dirpath : str or path-like
            The path of a directory.
        start : int or None, optional (default: None)
            The start offset of files belonging to the directory.
        stop : int or None, optional (default: None)
            The stop offset of files belonging to the directory.

        Returns
        -------
        hash_value : bytes
            The hash value of the directory.
        """

        # The initial hash value is all zeros.
        value = bytes(self.ctx_proto.digest_size)
        with os.scandir(dirpath) as it:
            for entry in it:
                if entry.is_dir():
                    other = self.hash_d(entry, start, stop)
                else:
                    other = self.hash_f(entry, start, stop)
                # Just XOR each byte string as hash value.
                value = strxor(value, other)
        return value

    def hash(self, path, start=None, stop=None, *, dir_ok=False):
        """Return the hash value of a file or a directory.

        Parameters
        ----------
        path : str or path-like
            The path of a file or a directory.
        start : int or None, optional (default: None)
            The start offset of the file or files belonging to the directory.
        stop : int or None, optional (default: None)
            The stop offset of the file or files belonging to the directory.
        dir_ok : bool, optional (default: False)
            If ``True``, enable directory hashing.

        Returns
        -------
        hash_value : bytes
            The hash value of the file or the directory.
        """

        if os.path.isdir(path):
            if dir_ok:
                return self.hash_d(path, start, stop)
            raise IsADirectory("'{}' is a directory".format(path))
        return self.hash_f(path, start, stop)

    __call__ = hash


class HashFileReader(object):
    """General hash file reader.

    Parameters
    ----------
    filepath : str or path-like
        The path of a hash file.
    """

    def __init__(self, filepath):
        self.name = filepath
        self.file = open(filepath, "r", encoding="utf-8")

    def close(self):
        self.file.close()

    def read_hash_line(self):
        """Read hash line.

        Returns
        -------
        hash_line : str
            The formatted `hex_hash_value` and `path_repr` with GNU Coreutils style.
        """

        while True:
            line = self.file.readline()
            if line.startswith("#"):
                continue
            # A empty string means EOF and will not give rise to infinite loop
            # since `''.isspace() == False`.
            if line.isspace():
                continue
            break
        return line

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __iter__(self):
        with self as f:
            while True:
                hash_line = f.read_hash_line()
                if not hash_line:
                    break
                yield hash_line


class HashFileWriter(object):
    """General hash file writer.

    Parameters
    ----------
    filepath : str or path-like
        The path of a hash file.
    """

    def __init__(self, filepath):
        self.name = filepath
        self.file = open(filepath, "w", encoding="utf-8")

    def close(self):
        self.file.close()

    def write_hash_line(self, hash_line):
        """Write hash line.

        Parameters
        ----------
        hash_line : str
            The formatted `hex_hash_value` and `path_repr` with GNU Coreutils style.
        """

        self.file.write(hash_line)

    def write_comment(self, comment):
        """Write comment.

        Parameters
        ----------
        comment : str
            A comment without newline.
        """

        self.file.write("# ")
        self.file.write(comment)
        self.file.write("\n")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def format_hash_line(hex_hash_value, path_repr):
    r"""Format hash line.

    Parameters
    ----------
    hex_hash_value : str
        The hex hash value string.
    path_repr : str or path-like
        The certain path representation of a file or a directory with
        corresponding hash value.
        (1) A absolute path;
        (2) A relative path;
        (3) A path relative to a given root directory.

    Returns
    -------
    hash_line : str
        The formatted `hex_hash_value` and `path_repr` with GNU Coreutils style.

    Examples
    --------
    >>> format_hash_line('d41d8cd98f00b204e9800998ecf8427e', 'a.txt')
    'd41d8cd98f00b204e9800998ecf8427e *a.txt\n'
    """

    return "{} *{}\n".format(hex_hash_value, path_repr)


def format_hash_line_real(hash_value, path, *, root=None):
    # Do convert bytes to hex string.
    hex_hash_value = hash_value.hex()
    # Do generate path representation.
    path_repr = path
    if root is not None:
        path_repr = os.path.normpath(os.path.relpath(path, root))
    return format_hash_line(hex_hash_value, path_repr)


def parse_hash_line(hash_line):
    r"""Parse hash line.

    Parameters
    ----------
    hash_line : str
        The formatted `hex_hash_value` and `path_repr` with GNU Coreutils style.

    Returns
    -------
    hex_hash_value : str
        The hex hash value string.
    path_repr : str
        The certain path representation of a file or a directory with
        corresponding hash value.
        (1) A absolute path;
        (2) A relative path;
        (3) A path relative to a given root directory.

    Examples
    --------
    >>> parse_hash_line('d41d8cd98f00b204e9800998ecf8427e *a.txt\n')
    ('d41d8cd98f00b204e9800998ecf8427e', 'a.txt')
    """

    m = _HASH_LINE_RE.match(hash_line)
    if m is None:
        raise ParseHashLineError(hash_line)
    return m.groups()


def parse_hash_line_real(hash_line, *, root=None):
    hex_hash_value, path_repr = parse_hash_line(hash_line)
    # Do convert hex string to bytes.
    hash_value = bytes.fromhex(hex_hash_value)
    # Do resolve path representation.
    path = path_repr
    if root is not None:
        path = os.path.normpath(os.path.join(root, path_repr))
    return hash_value, path


def generate_hash_line(path, hash_function, *, root=None):
    """Generate hash line.

    Parameters
    ----------
    path : str or path-like
        The path of a file or a directory with corresponding hash value.
    hash_function : callable(str or path-like) -> bytes-like
        A function for generating hash value.
    root : str, path-like or None, optional (default: None)
        The root directory of `path`. The path field in `hash_line` is relative
        to the root directory.

    Returns
    -------
    hash_line : str
        The formatted `hash_value` and `path` with GNU Coreutils style.
    """

    hash_value = hash_function(path)
    return format_hash_line_real(hash_value, path, root=root)


def check_hash_line(hash_line, hash_function, *, root=None):
    """Check hash line.

    Parameters
    ----------
    hash_line : str
        The formatted `hash_value` and `path` with GNU Coreutils style.
    hash_function : callable(str or path-like) -> bytes-like
        A function for generating hash value.
    root : str, path-like or None, optional (default: None)
        The root directory of `path`. The path field in `hash_line` is relative
        to the root directory.

    Returns
    -------
    path : str
        The path of a file or a directory with corresponding hash value.
    """

    hash_value, path = parse_hash_line_real(hash_line, root=root)
    curr_hash_value = hash_function(path)
    if not compare_digest(hash_value, curr_hash_value):
        raise CheckHashLineError(hash_line, hash_value, path, curr_hash_value)
    return path


def re_name_to_hash(hash_line, *, root=None):
    hash_value, nameing_path = parse_hash_line_real(hash_line, root=root)
    hashing_path = os.path.join(os.path.dirname(nameing_path), hash_value.hex())
    os.rename(nameing_path, hashing_path)


def re_hash_to_name(hash_line, *, root=None):
    hash_value, nameing_path = parse_hash_line_real(hash_line, root=root)
    hashing_path = os.path.join(os.path.dirname(nameing_path), hash_value.hex())
    os.rename(hashing_path, nameing_path)
