import os
from hashlib import md5

from gethash.core import check_hash_line, format_hash_line, generate_hash_line, parse_hash_line


def md5_digest(path: str) -> bytes:
    with open(path, "rb") as f:
        return md5(f.read()).digest()


def test_format_hash_line() -> None:
    result = format_hash_line("d41d8cd98f00b204e9800998ecf8427e", "foo.txt")
    assert result == "d41d8cd98f00b204e9800998ecf8427e *foo.txt\n"


def test_parse_hash_line() -> None:
    result = parse_hash_line("d41d8cd98f00b204e9800998ecf8427e *foo.txt\n")
    assert result == ("d41d8cd98f00b204e9800998ecf8427e", "foo.txt")


def test_generate_hash_line(root: str) -> None:
    result = generate_hash_line(os.path.join(root, "foo.txt"), md5_digest, root=root)
    assert result == "d41d8cd98f00b204e9800998ecf8427e *foo.txt\n"


def test_check_hash_line(root: str) -> None:
    result = check_hash_line("d41d8cd98f00b204e9800998ecf8427e *foo.txt\n", md5_digest, root=root)
    assert result == os.path.join(root, "foo.txt")
