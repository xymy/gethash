from collections.abc import Generator

import pytest

from .utils import Vectors


@pytest.fixture(scope="session")
def vectors(tmp_path_factory: pytest.TempPathFactory) -> Generator[Vectors, None, None]:
    root = tmp_path_factory.mktemp("vectors")
    vectors = Vectors(root)
    vectors.init_data_files()
    yield vectors
    vectors.finalize_data_files()
