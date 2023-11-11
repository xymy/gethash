from collections.abc import Generator
from pathlib import Path

import pytest
from pytest import TempPathFactory

from .utils import Vectors


@pytest.fixture(scope="session")
def vectors(tmp_path_factory: TempPathFactory) -> Generator[Vectors, None, None]:
    root = tmp_path_factory.mktemp("vectors")
    vectors = Vectors(root)
    vectors.init_data_files()
    yield vectors
    vectors.finalize_data_files()


@pytest.fixture(scope="module")
def root() -> Path:
    return Path(__file__).parent / "data"


@pytest.fixture(scope="module")
def foo_txt_path(root: Path) -> Path:
    return root / "foo.txt"


@pytest.fixture(scope="module")
def foo_txt_sha256_path(root: Path) -> Path:
    return root / "foo.txt.sha256"


@pytest.fixture(scope="module")
def foo_txt_a_sha256_path(root: Path) -> Path:
    return root / "foo.txt.a.sha256"


@pytest.fixture(scope="module")
def foo_zip_path(root: Path) -> Path:
    return root / "foo.zip"


@pytest.fixture(scope="module")
def foo_zip_sha256_path(root: Path) -> Path:
    return root / "foo.zip.sha256"


@pytest.fixture(scope="module")
def foo_zip_sha256_a_path(root: Path) -> Path:
    return root / "foo.zip.a.sha256"
