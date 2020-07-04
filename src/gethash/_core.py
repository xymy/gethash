import os
import re
from hmac import compare_digest
from os import PathLike
from typing import ByteString, Tuple

from tqdm import tqdm

_CHUNK_SIZE = 0x100000
_HL_PAT = re.compile(r'([0-9a-fA-F]+) \*(.+)')


class ParseHashLineError(ValueError):
    """Raised by function `phl`."""


class CheckHashLineError(ValueError):
    """Raised by function `chl`."""


def calc_hash(
    ctx_proto,
    path,
    *,
    chunk_size=_CHUNK_SIZE,
    **tqdm_args
) -> bytes:
    """Calculate the hash value of `path` using the copy of given hash context
    prototype `ctx_proto`.

    A tqdm progressbar is also available.
    """
    ctx = ctx_proto.copy()
    file_size = os.path.getsize(path)
    leave = tqdm_args.pop('leave', False)
    ascii = tqdm_args.pop('ascii', True)
    bar = tqdm(total=file_size, leave=leave, ascii=ascii, **tqdm_args)
    with bar as bar, open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            ctx.update(chunk)
            bar.update(len(chunk))
        return ctx.digest()


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


def ghl(ctx_proto, path, **tqdm_args):
    """Generate hash line.

    Require path; return hash line.
    """
    hash_value = calc_hash(ctx_proto, path, **tqdm_args)
    return fhl(hash_value, path)


def chl(ctx_proto, hash_line, **tqdm_args):
    """Check hash line.

    Require hash line; return path.
    """
    hash_value, path = phl(hash_line)
    curr_hash_value = calc_hash(ctx_proto, path, **tqdm_args)
    if not compare_digest(hash_value, curr_hash_value):
        raise CheckHashLineError(hash_line)
    return path
