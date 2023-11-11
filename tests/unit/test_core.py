from __future__ import annotations

from collections.abc import Iterable
from hashlib import sha256
from pathlib import Path
from typing import TypeVar

import pytest

from gethash.core import (
    CheckHashLineError,
    HashFileReader,
    HashFileWriter,
    ParseHashLineError,
    check_hash_line,
    format_hash_line,
    generate_hash_line,
    parse_hash_line,
)

from ..data import (
    DATA_DIR,
    FOO_TXT_A_SHA256_PATH,
    FOO_TXT_NAME,
    FOO_TXT_PATH,
    FOO_TXT_SHA256_HASH,
    FOO_TXT_SHA256_HASH_LINE,
    FOO_TXT_SHA256_PATH,
    FOO_ZIP_A_SHA256_PATH,
    FOO_ZIP_NAME,
    FOO_ZIP_PATH,
    FOO_ZIP_SHA256_HASH,
    FOO_ZIP_SHA256_HASH_LINE,
    FOO_ZIP_SHA256_PATH,
)


def sha256_digest(path: str | Path) -> bytes:
    with open(path, "rb") as f:
        return sha256(f.read()).digest()


def read_text(path: str | Path) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


T = TypeVar("T")


def pick_first(iterable: Iterable[T]) -> T:
    value = next(iterable)  # type: ignore [call-overload]
    try:
        next(iterable)  # type: ignore [call-overload]
    except StopIteration:
        return value
    else:
        raise AssertionError


@pytest.mark.parametrize(
    "hash_line, name, hash",
    [
        (FOO_TXT_SHA256_HASH_LINE, FOO_TXT_NAME, FOO_TXT_SHA256_HASH),
        (FOO_ZIP_SHA256_HASH_LINE, FOO_ZIP_NAME, FOO_ZIP_SHA256_HASH),
    ],
)
class TestFormatParseHashLine:
    def test_format_hash_line(self, hash_line: str, name: str, hash: str) -> None:
        result = format_hash_line(name, hash)
        assert result == hash_line

    def test_parse_hash_line(self, hash_line: str, name: str, hash: str) -> None:
        result = parse_hash_line(hash_line)
        assert result == (name, hash)

        with pytest.raises(ParseHashLineError):
            parse_hash_line(hash + name)


@pytest.mark.parametrize(
    "root, path, hash_line",
    [
        (DATA_DIR, FOO_TXT_PATH, FOO_TXT_SHA256_HASH_LINE),
        (DATA_DIR, FOO_ZIP_PATH, FOO_ZIP_SHA256_HASH_LINE),
    ],
)
class TestGenerateCheckHashLine:
    def test_generate_hash_line(self, root: Path, path: Path, hash_line: str) -> None:
        result = generate_hash_line(str(path), sha256_digest, root=root)
        assert result == hash_line

    def test_check_hash_line(self, root: Path, path: Path, hash_line: str) -> None:
        result = check_hash_line(hash_line, sha256_digest, root=root)
        assert result == str(path)

        with pytest.raises(CheckHashLineError):
            check_hash_line("0" + hash_line[1:], sha256_digest, root=root)


@pytest.mark.parametrize(
    "hash_path, a_hash_path, hash_line",
    [
        (FOO_TXT_SHA256_PATH, FOO_TXT_A_SHA256_PATH, FOO_TXT_SHA256_HASH_LINE),
        (FOO_ZIP_SHA256_PATH, FOO_ZIP_A_SHA256_PATH, FOO_ZIP_SHA256_HASH_LINE),
    ],
)
class TestHashFileReader:
    def test_read_hash_line(self, hash_path: Path, a_hash_path: Path, hash_line: str) -> None:
        with HashFileReader(hash_path) as hash_file:
            assert hash_file.read_hash_line() == hash_line
            assert hash_file.read_hash_line() == ""

        with HashFileReader(a_hash_path) as hash_file:
            assert hash_file.read_hash_line() == hash_line
            assert hash_file.read_hash_line() == ""

    def test_iter(self, hash_path: Path, a_hash_path: Path, hash_line: str) -> None:
        result = pick_first(HashFileReader(hash_path).iter())
        assert result == hash_line

        result = pick_first(HashFileReader(a_hash_path).iter())
        assert result == hash_line


@pytest.mark.parametrize(
    "hash_path, a_hash_path, name, hash",
    [
        (FOO_TXT_SHA256_PATH, FOO_TXT_A_SHA256_PATH, FOO_TXT_NAME, FOO_TXT_SHA256_HASH),
        (FOO_ZIP_SHA256_PATH, FOO_ZIP_A_SHA256_PATH, FOO_ZIP_NAME, FOO_ZIP_SHA256_HASH),
    ],
)
class TestHashFileReaderIter2:
    def test_iter2(self, hash_path: Path, a_hash_path: Path, name: str, hash: str) -> None:
        result = pick_first(HashFileReader(hash_path).iter2())
        assert result == (name, hash)

        result = pick_first(HashFileReader(a_hash_path).iter2())
        assert result == (name, hash)


@pytest.mark.parametrize(
    "hash_path, a_hash_path, name",
    [
        (FOO_TXT_SHA256_PATH, FOO_TXT_A_SHA256_PATH, FOO_TXT_NAME),
        (FOO_ZIP_SHA256_PATH, FOO_ZIP_A_SHA256_PATH, FOO_ZIP_NAME),
    ],
)
class TestHashFileReaderIterName:
    def test_iter_name(self, hash_path: Path, a_hash_path: Path, name: str) -> None:
        result = pick_first(HashFileReader(hash_path).iter_name())
        assert result == name

        result = pick_first(HashFileReader(a_hash_path).iter_name())
        assert result == name


@pytest.mark.parametrize(
    "hash_path, a_hash_path, hash",
    [
        (FOO_TXT_SHA256_PATH, FOO_TXT_A_SHA256_PATH, FOO_TXT_SHA256_HASH),
        (FOO_ZIP_SHA256_PATH, FOO_ZIP_A_SHA256_PATH, FOO_ZIP_SHA256_HASH),
    ],
)
class TestHashFileReaderIterHash:
    def test_iter_hash(self, hash_path: Path, a_hash_path: Path, hash: str) -> None:
        result = pick_first(HashFileReader(hash_path).iter_hash())
        assert result == hash

        result = pick_first(HashFileReader(a_hash_path).iter_hash())
        assert result == hash


@pytest.mark.parametrize(
    "hash_path, hash_line",
    [
        (FOO_TXT_SHA256_PATH, FOO_TXT_SHA256_HASH_LINE),
        (FOO_ZIP_SHA256_PATH, FOO_ZIP_SHA256_HASH_LINE),
    ],
)
class TestHashFileWriter:
    def test_write_hash_line(self, tmp_path: Path, hash_path: Path, hash_line: str) -> None:
        tmp_hash_path = tmp_path / hash_path.name
        with HashFileWriter(tmp_hash_path) as hash_file:
            hash_file.write_hash_line(hash_line)
        assert read_text(tmp_hash_path) == read_text(hash_path)
