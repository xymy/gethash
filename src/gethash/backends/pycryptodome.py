from importlib import import_module
from typing import Any, Set

import Crypto  # noqa

from . import Backend


class PyCryptodomeBackend(Backend):
    _algorithms = {"md2", "md4", "ripemd160"}

    @property
    def algorithms_available(self) -> Set[str]:
        return self._algorithms

    def load_ctx(self, name: str) -> Any:
        if name not in self.algorithms_available:
            raise ValueError(f"unkown algorithm {name!r}")

        module = import_module(f"Crypto.Hash.{name.upper()}")
        return module.new()  # type: ignore
