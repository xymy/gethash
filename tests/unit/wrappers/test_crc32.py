from __future__ import annotations

from pathlib import Path

import pytest

from gethash.core import check_hash_line, generate_hash_line
from gethash.hasher import Hasher
from gethash.wrappers.crc32 import new


@pytest.fixture(scope="module")
def foo_path(root: Path) -> Path:
    return root / "foo.txt"


@pytest.fixture(scope="module")
def foo_hash_line() -> str:
    return "00000000 *foo.txt\n"


def test_crc32(root: Path, foo_path: Path, foo_hash_line: str) -> None:
    hasher = Hasher(new())
    assert generate_hash_line(str(foo_path), hasher, root=root) == foo_hash_line
    assert check_hash_line(foo_hash_line, hasher, root=root) == str(foo_path)
