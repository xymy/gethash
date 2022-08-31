from pathlib import Path
from typing import Dict, Iterator, Tuple

_vectors = [
    {
        "data": "",
        "crc32": "00000000",
        "md5": "d41d8cd98f00b204e9800998ecf8427e",
        "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "data": "The quick brown fox jumps over the lazy dog.",
        "crc32": "519025e9",
        "md5": "e4d909c290d0fb1ca068ffaddf22cbd0",
        "sha1": "408d94384216f890ff7a0c3528e8bed1e0b01621",
        "sha256": "ef537f25c895bfa782526529a9b63d97aa631564d5d789c2b765448c8635fb6c",
    },
]


class Vectors:
    def __init__(self, root: Path) -> None:
        self.root = root

    def iter_path_vector(self) -> Iterator[Tuple[Path, Dict[str, str]]]:
        for i, vector in enumerate(_vectors):
            path = self.root / str(i)
            yield path, vector
