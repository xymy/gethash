from pathlib import Path
from typing import Iterator, List, Tuple, TypedDict


class Vector(TypedDict):
    data: bytes
    crc32: str
    md5: str
    sha1: str
    sha256: str


class Vectors:
    def __init__(self, root: Path) -> None:
        self.root = root

    def iter_path_vector(self) -> Iterator[Tuple[Path, Vector]]:
        for i, vector in enumerate(_vectors):
            yield self.root.joinpath(str(i)), vector

    def init_data_files(self) -> None:
        for path, vector in self.iter_path_vector():
            path.write_bytes(vector["data"])

    def finalize_data_files(self) -> None:
        for path, _ in self.iter_path_vector():
            path.unlink(missing_ok=True)


_vectors: List[Vector] = [
    {
        "data": b"",
        "crc32": "00000000",
        "md5": "d41d8cd98f00b204e9800998ecf8427e",
        "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    },
    {
        "data": b" ",
        "crc32": "e96ccf45",
        "md5": "7215ee9c7d9dc229d2921a40e899ec5f",
        "sha1": "b858cb282617fb0956d960215c8e84d1ccf909c6",
        "sha256": "36a9e7f1c95b82ffb99743e0c5c4ce95d83c9a430aac59f84ef3cbfab6145068",
    },
    {
        "data": b"\t",
        "crc32": "abde5729",
        "md5": "5e732a1878be2342dbfeff5fe3ca5aa3",
        "sha1": "ac9231da4082430afe8f4d40127814c613648d8e",
        "sha256": "2b4c342f5433ebe591a1da77e013d1b72475562d48578dca8b84bac6651c3cb9",
    },
    {
        "data": b"\n",
        "crc32": "32d70693",
        "md5": "68b329da9893e34099c7d8ad5cb9c940",
        "sha1": "adc83b19e793491b1c6ea0fd8b46cd9f32e592fc",
        "sha256": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b",
    },
    {
        "data": b"\x00",
        "crc32": "d202ef8d",
        "md5": "93b885adfe0da089cdf634904fd59f71",
        "sha1": "5ba93c9db0cff93f52b521d7420e43f6eda2784f",
        "sha256": "6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d",
    },
    {
        "data": b"The quick brown fox jumps over the lazy dog.",
        "crc32": "519025e9",
        "md5": "e4d909c290d0fb1ca068ffaddf22cbd0",
        "sha1": "408d94384216f890ff7a0c3528e8bed1e0b01621",
        "sha256": "ef537f25c895bfa782526529a9b63d97aa631564d5d789c2b765448c8635fb6c",
    },
]
