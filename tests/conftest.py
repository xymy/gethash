import pytest
from pytest import TempPathFactory

from .utils import Vectors


@pytest.fixture(scope="session")
def vectors(tmp_path_factory: TempPathFactory) -> Vectors:
    root = tmp_path_factory.mktemp("vectors")
    vectors = Vectors(root)
    for path, vector in vectors.iter_path_vector():
        path.write_text(vector["data"], encoding="utf-8")
    return vectors
