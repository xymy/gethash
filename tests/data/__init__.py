from collections.abc import Sequence
from pathlib import Path


class HashData:
    def __init__(self, root: Path, name: str, hash: str, hash_suffix: str) -> None:
        self.root = root
        self.name = name
        self.path = root / name
        self.hash = hash
        self.hash_line = f"{hash} *{name}\n"
        self.hash_path = root / (name + hash_suffix)

    def get(self, argnames: Sequence[str]) -> tuple[str, ...]:
        return tuple(getattr(self, argname) for argname in argnames)


DATA_DIR = Path(__file__).parent

FOO_TXT_SHA256 = HashData(
    DATA_DIR,
    "foo.txt",
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ".sha256",
)
FOO_TXT_A_SHA256 = HashData(
    DATA_DIR,
    "foo.txt",
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    ".a.sha256",
)
FOO_ZIP_SHA256 = HashData(
    DATA_DIR,
    "foo.zip",
    "67e458e408a0e2da7f50b639d612f60e4c840e7175c7db707f22a9acc6df8427",
    ".sha256",
)
FOO_ZIP_A_SHA256 = HashData(
    DATA_DIR,
    "foo.zip",
    "67e458e408a0e2da7f50b639d612f60e4c840e7175c7db707f22a9acc6df8427",
    ".a.sha256",
)
