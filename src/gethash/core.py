import io
import os
import re
from hmac import compare_digest

from Cryptodome.Util.strxor import strxor
from tqdm import tqdm

_CHUNKSIZE = 0x100000  # 1 MB
_HASH_LINE_RE = re.compile(r"([0-9a-fA-F]+) (?:\*| )?(.+)")


class IsDirectory(OSError):
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

    Generate hash values using given hash context prototype. A tqdm progressbar
    is also available.

    Parameters
    ----------
    ctx_proto : hash context
        The hash context prototype used to generate hash values.
    chunksize : int, optional
        The size of data blocks when reading data from files.
    tqdm_args : dict, optional
        The arguments passed to the tqdm constructor.
    """

    def __init__(self, ctx_proto, *, chunksize=None, tqdm_args=None):
        # We use the copies of parameters for avoiding potential side-effects.
        self.ctx_proto = ctx_proto.copy()
        self.chunksize = _CHUNKSIZE if chunksize is None else int(chunksize)
        self.tqdm_args = {} if tqdm_args is None else dict(tqdm_args)

    def hash_f(self, filepath, start=None, stop=None):
        """Return the hash value of a file.

        Parameters
        ----------
        filepath : str or path-like
            The path of a file.
        start : int, optional
            The start range of the file.
        stop : int, optional
            The stop range of the file.

        Returns
        -------
        hash_value : bytes
            The hash value of the file.
        """

        ctx = self.ctx_proto.copy()
        chunksize = self.chunksize
        filesize = os.path.getsize(filepath)
        # Set the range of current file.
        if start is None or start < 0:
            start = 0
        if stop is None or stop > filesize:
            stop = filesize
        if start > stop:
            raise ValueError("require start <= stop, but {} > {}".format(start, stop))
        # Set the total of progressbar as range size.
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
        start : int, optional
            The start range of files belonging to the directory.
        stop : int, optional
            The stop range of files belonging to the directory.

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
        start : int, optional
            The start range of the file or files belonging to the directory.
        stop : int, optional
            The stop range of the file or files belonging to the directory.
        dir_ok : bool, default=False
            If ``True``, enable directory hashing.

        Returns
        -------
        hash_value : bytes
            The hash value of the file or the directory.
        """

        if os.path.isdir(path):
            if dir_ok:
                return self.hash_d(path, start, stop)
            raise IsDirectory('"{}" is a directory'.format(path))
        return self.hash_f(path, start, stop)

    __call__ = hash


def format_hash_line(hash_value, path):
    """Format hash line.

    Parameters
    ----------
    hash_value : bytes-like
        The hash value.
    path : str or path-like
        The path of a file or a directory.

    Returns
    -------
    hash_line : str
        The formatted hash line with GNU Coreutils style.
    """

    return "{} *{}\n".format(hash_value.hex(), path)


def parse_hash_line(hash_line):
    """Parse hash line.

    Parameters
    ----------
    hash_line : str
        The formatted hash line with GNU Coreutils style.

    Returns
    -------
    hash_value : bytes
        The hash value.
    path : str
        The path of a file or a directory.
    """

    m = _HASH_LINE_RE.match(hash_line)
    if m is None:
        raise ParseHashLineError(hash_line)
    hash_value, path = m.groups()
    return bytes.fromhex(hash_value), path


def generate_hash_line(hash_function, path, *, inplace=None):
    """Generate hash line.

    Parameters
    ----------
    hash_function : callable(str or path-like) -> bytes-like
        The function used to generate hash value.
    path : str or path-like
        The path of a file or a directory.
    inplace : bool, optional
        If ``True``, use basename in hash line.

    Returns
    -------
    hash_line : str
        The formatted hash line with GNU Coreutils style.
    """

    hash_value = hash_function(path)
    if inplace:
        path = os.path.basename(path)
    return format_hash_line(hash_value, path)


def check_hash_line(hash_function, hash_line, *, inplace=None):
    """Check hash line.

    Parameters
    ----------
    hash_function : callable(str or path-like) -> bytes-like
        The function used to generate hash value.
    hash_line : str
        The formatted hash line with GNU Coreutils style.
    inplace : str or path-like, optional
        If given, it should be the filepath conatining the hash line.

    Returns
    -------
    path : str
        The path of a file or a directory.
    """

    hash_value, path = parse_hash_line(hash_line)
    try:
        hash_path = os.fspath(inplace)
    except TypeError:
        pass
    else:
        path = os.path.join(os.path.dirname(hash_path), path)
    curr_hash_value = hash_function(path)
    if not compare_digest(hash_value, curr_hash_value):
        raise CheckHashLineError(hash_line, hash_value, path, curr_hash_value)
    return path