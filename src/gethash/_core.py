import os
import re
from hmac import compare_digest
from os import PathLike
from typing import ByteString, Tuple

from tqdm import tqdm

_CHUNK_SIZE = 0x100000
_HL_PAT = re.compile(r'([0-9a-fA-F]+) (?:\*| )?(.+)')


class IsDirectory(OSError):
    """Raised by function `calc_hash`."""


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


def calc_hash_f(
    ctx_proto,
    path,
    *,
    chunk_size=_CHUNK_SIZE,
    **tqdm_args
) -> bytes:
    ctx = ctx_proto.copy()
    file_size = os.path.getsize(path)
    bar = tqdm(total=file_size, **tqdm_args)
    with bar as bar, open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            ctx.update(chunk)
            bar.update(len(chunk))
        return ctx.digest()


def calc_hash_d(
    ctx_proto,
    path,
    *,
    chunk_size=_CHUNK_SIZE,
    **tqdm_args
) -> bytes:
    value = bytes(ctx_proto.digest_size)
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                other = calc_hash_d(
                    ctx_proto, entry, chunk_size=chunk_size, **tqdm_args)
            else:
                other = calc_hash_f(
                    ctx_proto, entry, chunk_size=chunk_size, **tqdm_args)
            value = bytes(x ^ y for x, y in zip(value, other))
    return value


def calc_hash(
    ctx_proto,
    path,
    *,
    chunk_size=_CHUNK_SIZE,
    dir_ok=False,
    **tqdm_args
) -> bytes:
    """Calculate the hash value of `path` using the copy of given hash context
    prototype `ctx_proto`.

    A tqdm progressbar is also available.
    """
    if os.path.isdir(path):
        if dir_ok:
            return calc_hash_d(
                ctx_proto, path, chunk_size=chunk_size, **tqdm_args)
        raise IsDirectory('"{}" is a directory'.format(path))
    return calc_hash_f(ctx_proto, path, chunk_size=chunk_size, **tqdm_args)


def fhl(hash_value: ByteString, path: PathLike) -> str:
    """Format hash line.

    Require hash value and path; return hash line.
    """
    return '{} *{}\n'.format(hash_value.hex(), path)


def phl(hash_line: str) -> Tuple[bytes, str]:
    """Parse hash line.

    Require hash line; return hash value and path.
    """
    m = _HL_PAT.match(hash_line)
    if m is None:
        raise ParseHashLineError(hash_line)
    hash_value, path = m.groups()
    return bytes.fromhex(hash_value), path


def ghl(ctx_proto, path, *, inplace=False, **extra):
    """Generate hash line.

    Require path; return hash line.
    """
    hash_value = calc_hash(ctx_proto, path, **extra)
    if inplace:
        path = os.path.basename(path)
    return fhl(hash_value, path)


def chl(ctx_proto, hash_line, *, inplace=False, **extra):
    """Check hash line.

    Require hash line; return path.
    """
    hash_value, path = phl(hash_line)
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
