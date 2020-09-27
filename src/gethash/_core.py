import io
import os
import re
from hmac import compare_digest
from os import PathLike
from typing import ByteString, Tuple

from tqdm import tqdm

_CHUNK_SIZE = 0x100000
_HL_PAT = re.compile(r"([0-9a-fA-F]+) (?:\*| )?(.+)")


class ParseHashLineError(ValueError):
    """Raised by function `phl`."""


class CheckHashLineError(ValueError):
    """Raised by function `chl`."""

    def __init__(self, hash_line, hash_value, path, curr_hash_value):
        super().__init__(hash_line, hash_value, path, curr_hash_value)
        self.hash_line = hash_line
        self.hash_value = hash_value
        self.path = path
        self.curr_hash_value = curr_hash_value


class IsDirectory(OSError):
    """Raised by function `calc_hash`."""


class Hasher(object):
    """Calculate the hash value using the copy of given hash context prototype
    `ctx_proto`.

    A tqdm progressbar is also available.
    """

    def __init__(self, ctx_proto, *, chunk_size=None, tqdm_args=None):
        self.ctx_proto = ctx_proto
        self.chunk_size = _CHUNK_SIZE if chunk_size is None else chunk_size
        self.tqdm_args = {} if tqdm_args is None else tqdm_args

    def calc_hash_f(self, filepath, start=None, stop=None) -> bytes:
        """Calculate the hash value of a file.

        A tqdm progressbar is also available.
        """
        ctx = self.ctx_proto.copy()
        chunk_size = self.chunk_size
        file_size = os.path.getsize(filepath)
        # Set the range for current file.
        if start is None:
            start = 0
        if stop is None:
            stop = file_size
        # Set the total of progressbar as file range size.
        total = stop - start
        bar = tqdm(total=total, **self.tqdm_args)
        with bar as bar, open(filepath, "rb") as f:
            count, remain_size = divmod(total, chunk_size)
            f.seek(start, io.SEEK_SET)
            for _ in range(count):
                chunk = f.read(chunk_size)
                ctx.update(chunk)
                bar.update(chunk_size)
            remain = f.read(remain_size)
            ctx.update(remain)
            bar.update(remain_size)
        return ctx.digest()

    def calc_hash_d(self, dirpath, start=None, stop=None) -> bytes:
        """Calculate the hash value of a directory.

        A tqdm progressbar is also available.
        """
        value = bytes(self.ctx_proto.digest_size)
        with os.scandir(dirpath) as it:
            for entry in it:
                if entry.is_dir():
                    other = self.calc_hash_d(entry, start, stop)
                else:
                    other = self.calc_hash_f(entry, start, stop)
                value = bytes(x ^ y for x, y in zip(value, other))
        return value

    def calc_hash(self, path, start=None, stop=None, *, dir_ok=False) -> bytes:
        """Calculate the hash value of `path`.

        A tqdm progressbar is also available.
        """
        if os.path.isdir(path):
            if dir_ok:
                return self.calc_hash_d(path, start, stop)
            raise IsDirectory('"{}" is a directory'.format(path))
        return self.calc_hash_f(path, start, stop)


def calc_hash_f(ctx_proto, filepath, *, chunk_size=_CHUNK_SIZE, **tqdm_args) -> bytes:
    """Calculate the hash value of a file using the copy of given hash context
    prototype `ctx_proto`.

    A tqdm progressbar is also available.
    """
    ctx = ctx_proto.copy()
    file_size = os.path.getsize(filepath)
    bar = tqdm(total=file_size, **tqdm_args)
    with bar as bar, open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            ctx.update(chunk)
            bar.update(len(chunk))
        return ctx.digest()


def calc_hash_d(ctx_proto, dirpath, *, chunk_size=_CHUNK_SIZE, **tqdm_args) -> bytes:
    """Calculate the hash value of a directory using the copy of given hash
    context prototype `ctx_proto`.

    A tqdm progressbar is also available.
    """
    value = bytes(ctx_proto.digest_size)
    with os.scandir(dirpath) as it:
        for entry in it:
            if entry.is_dir():
                other = calc_hash_d(
                    ctx_proto, entry, chunk_size=chunk_size, **tqdm_args
                )
            else:
                other = calc_hash_f(
                    ctx_proto, entry, chunk_size=chunk_size, **tqdm_args
                )
            value = bytes(x ^ y for x, y in zip(value, other))
    return value


def calc_hash(
    ctx_proto, path, *, chunk_size=_CHUNK_SIZE, dir_ok=False, **tqdm_args
) -> bytes:
    """Calculate the hash value of `path` using the copy of given hash context
    prototype `ctx_proto`.

    A tqdm progressbar is also available.
    """
    if os.path.isdir(path):
        if dir_ok:
            return calc_hash_d(ctx_proto, path, chunk_size=chunk_size, **tqdm_args)
        raise IsDirectory('"{}" is a directory'.format(path))
    return calc_hash_f(ctx_proto, path, chunk_size=chunk_size, **tqdm_args)


def format_hash_line(hash_value: ByteString, path: PathLike) -> str:
    """Format hash line.

    Require hash value and path; return hash line.
    """
    return "{} *{}\n".format(hash_value.hex(), path)


def parse_hash_line(hash_line: str) -> Tuple[bytes, str]:
    """Parse hash line.

    Require hash line; return hash value and path.
    """
    m = _HL_PAT.match(hash_line)
    if m is None:
        raise ParseHashLineError(hash_line)
    hash_value, path = m.groups()
    return bytes.fromhex(hash_value), path


def generate_hash_line(ctx_proto, path, *, inplace=False, **extra):
    """Generate hash line.

    Require path; return hash line.
    """
    hash_value = calc_hash(ctx_proto, path, **extra)
    if inplace:
        path = os.path.basename(path)
    return format_hash_line(hash_value, path)


def check_hash_line(ctx_proto, hash_line, *, inplace=False, **extra):
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
    curr_hash_value = calc_hash(ctx_proto, path, **extra)
    if not compare_digest(hash_value, curr_hash_value):
        raise CheckHashLineError(hash_line, hash_value, path, curr_hash_value)
    return path
