import hashlib
from pathlib import Path

from gethash.hasher import HashContext, Hasher
from gethash.wrappers.crc32 import CRC32

from ..utils import vectors


class TestHasher:
    def _assert(self, data_dir: Path, ctx: HashContext, name: str) -> None:
        hasher = Hasher(ctx)
        for i, vector in enumerate(vectors):
            path = data_dir / str(i)
            assert hasher(path).hex() == vector[name]

    def test_crc32(self, data_dir: Path) -> None:
        ctx = CRC32()
        self._assert(data_dir, ctx, "crc32")

    def test_md5(self, data_dir: Path) -> None:
        ctx = hashlib.md5()
        self._assert(data_dir, ctx, "md5")

    def test_sha1(self, data_dir: Path) -> None:
        ctx = hashlib.sha1()
        self._assert(data_dir, ctx, "sha1")

    def test_sha256(self, data_dir: Path) -> None:
        ctx = hashlib.sha256()
        self._assert(data_dir, ctx, "sha256")
