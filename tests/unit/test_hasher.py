import hashlib

from gethash.hasher import HashContext, Hasher
from gethash.wrappers.crc32 import CRC32

from ..utils import Vectors


class TestHasher:
    def _assert(self, vectors: Vectors, ctx: HashContext, name: str) -> None:
        hasher = Hasher(ctx)
        for path, vector in vectors.iter_path_vector():
            assert hasher(path).hex() == vector[name]

    def test_crc32(self, vectors: Vectors) -> None:
        ctx = CRC32()
        self._assert(vectors, ctx, "crc32")

    def test_md5(self, vectors: Vectors) -> None:
        ctx = hashlib.md5()
        self._assert(vectors, ctx, "md5")

    def test_sha1(self, vectors: Vectors) -> None:
        ctx = hashlib.sha1()
        self._assert(vectors, ctx, "sha1")

    def test_sha256(self, vectors: Vectors) -> None:
        ctx = hashlib.sha256()
        self._assert(vectors, ctx, "sha256")
