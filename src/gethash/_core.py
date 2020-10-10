import io
import os
import re
from hmac import compare_digest
from os import PathLike
from typing import ByteString, Callable, Optional, Tuple

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
    """Calculate the hash value using the copy of given hash context prototype
    `ctx_proto`.

    A tqdm progressbar is also available.
    """

    def __init__(
        self,
        ctx_proto,
        *,
        chunksize: Optional[int] = None,
        tqdm_args: Optional[dict] = None,
    ):
        # We use the copies of parameters for avoiding potential side-effects.
        self.ctx_proto = ctx_proto.copy()
        self.chunksize = _CHUNKSIZE if chunksize is None else int(chunksize)
        self.tqdm_args = {} if tqdm_args is None else dict(tqdm_args)

    def calc_hash_f(
        self, fpath: PathLike, start: Optional[int] = None, stop: Optional[int] = None
    ) -> bytes:
        """Calculate the hash value of a file.

        A tqdm progressbar is also available.
        """
        ctx = self.ctx_proto.copy()
        chunksize = self.chunksize
        file_size = os.path.getsize(fpath)
        # Set the range of current file.
        if start is None or start < 0:
            start = 0
        if stop is None or stop > file_size:
            stop = file_size
        if start > stop:
            raise ValueError("require start <= stop, but {} > {}".format(start, stop))
        # Set the total of progressbar as range size.
        total = stop - start
        bar = tqdm(total=total, **self.tqdm_args)
        with bar as bar, open(fpath, "rb") as f:
            # Precompute chunk count and remaining size.
            count, remain_size = divmod(total, chunksize)
            f.seek(start, io.SEEK_SET)
            for _ in range(count):
                chunk = f.read(chunksize)
                ctx.update(chunk)
                bar.update(chunksize)
            remain = f.read(remain_size)
            ctx.update(remain)
            bar.update(remain_size)
        return ctx.digest()

    def calc_hash_d(
        self, dpath: PathLike, start: Optional[int] = None, stop: Optional[int] = None
    ) -> bytes:
        """Calculate the hash value of a directory.

        A tqdm progressbar is also available.
        """
        value = bytes(self.ctx_proto.digest_size)
        with os.scandir(dpath) as it:
            for entry in it:
                if entry.is_dir():
                    other = self.calc_hash_d(entry, start, stop)
                else:
                    other = self.calc_hash_f(entry, start, stop)
                value = bytes(x ^ y for x, y in zip(value, other))
        return value

    def calc_hash(
        self,
        path: PathLike,
        start: Optional[int] = None,
        stop: Optional[int] = None,
        *,
        dir_ok: bool = False,
    ) -> bytes:
        """Calculate the hash value of `path`.

        A tqdm progressbar is also available.
        """
        if os.path.isdir(path):
            if dir_ok:
                return self.calc_hash_d(path, start, stop)
            raise IsDirectory('"{}" is a directory'.format(path))
        return self.calc_hash_f(path, start, stop)


def format_hash_line(hash_value: ByteString, path: PathLike) -> str:
    """Format hash line.

    Require hash value and path; return hash line.
    """
    return "{} *{}\n".format(hash_value.hex(), path)


def parse_hash_line(hash_line: str) -> Tuple[ByteString, PathLike]:
    """Parse hash line.

    Require hash line; return hash value and path.
    """
    m = _HASH_LINE_RE.match(hash_line)
    if m is None:
        raise ParseHashLineError(hash_line)
    hash_value, path = m.groups()
    return bytes.fromhex(hash_value), path


def generate_hash_line(
    hash_function: Callable[[PathLike], ByteString],
    path: PathLike,
    *,
    inplace: Optional[bool] = None,
) -> str:
    """Generate hash line.

    Require path; return hash line.
    """
    hash_value = hash_function(path)
    if inplace:
        path = os.path.basename(path)
    return format_hash_line(hash_value, path)


def check_hash_line(
    hash_function: Callable[[PathLike], ByteString],
    hash_line: str,
    *,
    inplace: Optional[PathLike] = None,
) -> PathLike:
    """Check hash line.

    Require hash line; return path.
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
