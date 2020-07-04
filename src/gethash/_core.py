import os
import re
from hmac import compare_digest
from os import PathLike
from typing import ByteString, Tuple

from tqdm import tqdm

_CHUNK_SIZE = 0x100000
_HL_PAT = re.compile(r'([0-9a-fA-F]+) \*(.+)')


class ParseHashLineError(ValueError):
    pass


class CheckHashLineError(ValueError):
    pass


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


def fhash(hash_value: ByteString, path: PathLike) -> str:
    """Format `hash_value` and `path` to `hash_line`."""
    return '{} *{}\n'.format(hash_value.hex(), path)


def phash(hash_line: str) -> Tuple[bytes, str]:
    """Parse `hash_line` to `hash_value` and `path`."""
    m = _HL_PAT.match(hash_line)
    if m is None:
        raise ParseHashLineError(hash_line)
    hash_value, path = m.groups()
    return bytes.fromhex(hash_value), path


def ghl(ctx_proto, path, **tqdm_args):
    """Generate hash line."""
    hash_value = calc_hash(ctx_proto, path, **tqdm_args)
    return fhash(hash_value, path)


def chl(ctx_proto, hash_line, **tqdm_args):
    """Check hash line."""
    hash_value, path = phash(hash_line)
    curr_hash_value = calc_hash(ctx_proto, path, **tqdm_args)
    if not compare_digest(hash_value, curr_hash_value):
        raise CheckHashLineError(hash_line)
    return path
