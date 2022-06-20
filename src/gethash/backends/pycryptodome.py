from importlib import import_module
from typing import Set

import Crypto  # noqa

from ..hasher import HashContext
from . import Backend


class PyCryptodomeBackend(Backend):
    _algorithms = {"md2", "md4", "ripemd160"}

    @property
    def algorithms_available(self) -> Set[str]:
        return self._algorithms

    def load_ctx(self, name: str) -> HashContext:
        # The `name` has been checked in `load_cmd`.
        module = import_module(f"Crypto.Hash.{name.upper()}")
        return module.new()


def load() -> PyCryptodomeBackend:
    return PyCryptodomeBackend()
