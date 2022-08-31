from pathlib import Path

import pytest
from pytest import TempPathFactory

from .utils import vectors


@pytest.fixture(scope="session")
def data_dir(tmp_path_factory: TempPathFactory) -> Path:
    dir = tmp_path_factory.mktemp("data")
    for i, vector in enumerate(vectors):
        path = dir / str(i)
        path.write_text(vector["data"], encoding="utf-8")
    return dir
