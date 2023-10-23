import os
from typing import Generator

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


@pytest.fixture(scope="session")
def root() -> str:
    return os.path.join(os.path.dirname(__file__), "data")
