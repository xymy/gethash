import os
from hashlib import sha256

import pytest

from gethash.core import (
    CheckHashLineError,
    HashFileReader,
    ParseHashLineError,
    check_hash_line,
    format_hash_line,
    generate_hash_line,
    parse_hash_line,
)


def sha256_digest(path: str) -> bytes:
    with open(path, "rb") as f:
        return sha256(f.read()).digest()


@pytest.fixture(scope="module")
def foo_hash_line() -> str:
    return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 *foo.txt\n"


@pytest.fixture(scope="module")
def foo_hash() -> str:
    return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


@pytest.fixture(scope="module")
def foo_name() -> str:
    return "foo.txt"


@pytest.fixture(scope="module")
def foo_path(root: str) -> str:
    return os.path.join(root, "foo.txt")


@pytest.fixture(scope="module")
def foo_hash_path(root: str) -> str:
    return os.path.join(root, "foo.txt.sha256")


def test_format_hash_line(foo_hash_line: str, foo_hash: str, foo_name: str) -> None:
    result = format_hash_line(foo_hash, foo_name)
    assert result == foo_hash_line


def test_parse_hash_line(foo_hash_line: str, foo_hash: str, foo_name: str) -> None:
    result = parse_hash_line(foo_hash_line)
    assert result == (foo_hash, foo_name)

    with pytest.raises(ParseHashLineError):
        parse_hash_line(foo_hash + foo_name)


def test_generate_hash_line(root: str, foo_path: str, foo_hash_line: str) -> None:
    result = generate_hash_line(foo_path, sha256_digest, root=root)
    assert result == foo_hash_line


def test_check_hash_line(root: str, foo_path: str, foo_hash_line: str) -> None:
    result = check_hash_line(foo_hash_line, sha256_digest, root=root)
    assert result == foo_path

    with pytest.raises(CheckHashLineError):
        check_hash_line("0" + foo_hash_line[1:], sha256_digest, root=root)


class TestHashFileReader:
    def test_iter(self, foo_hash_path: str, foo_hash_line: str) -> None:
        for hash_line in HashFileReader(foo_hash_path):
            assert hash_line == foo_hash_line

    def test_iter2(self, foo_hash_path: str, foo_hash: str, foo_name: str) -> None:
        for hash, name in HashFileReader(foo_hash_path).iter2():
            assert (hash, name) == (foo_hash, foo_name)

    def test_iter_hash(self, foo_hash_path: str, foo_hash: str) -> None:
        for hash in HashFileReader(foo_hash_path).iter_hash():
            assert hash == foo_hash

    def test_iter_name(self, foo_hash_path: str, foo_name: str) -> None:
        for name in HashFileReader(foo_hash_path).iter_name():
            assert name == foo_name
