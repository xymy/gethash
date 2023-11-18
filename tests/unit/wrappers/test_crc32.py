from __future__ import annotations

from pathlib import Path

import pytest

from gethash.core import check_hash_line, generate_hash_line
from gethash.hasher import Hasher
from gethash.wrappers.crc32 import new

from ...data import FOO_TXT_CRC32, FOO_ZIP_CRC32

_test_crc32_ARGNAMES = ("root", "path", "hash_line", "hash")


@pytest.mark.parametrize(
    _test_crc32_ARGNAMES,
    [
        FOO_TXT_CRC32.get(_test_crc32_ARGNAMES),
        FOO_ZIP_CRC32.get(_test_crc32_ARGNAMES),
    ],
)
def test_crc32(root: Path, path: Path, hash_line: str, hash: str) -> None:
    ctx = new()
    hasher = Hasher(ctx)
    assert generate_hash_line(str(path), hasher, root=root) == hash_line
    assert check_hash_line(hash_line, hasher, root=root) == str(path)

    # `hasher` should not mutate `ctx`.
    ctx.update(path.read_bytes())
    assert ctx.hexdigest() == hash
