from importlib import import_module
from typing import Set

from ..hasher import HashContext
from . import Backend


class WrappersBackend(Backend):
    _algorithms = {"crc32"}

    @property
    def algorithms_available(self) -> Set[str]:
        return self._algorithms

    def load_ctx(self, name: str) -> HashContext:
        # The `name` has been checked in `load_cmd`.
        module = import_module(f"gethash.wrappers.{name}")
        return module.new()


def load() -> WrappersBackend:
    return WrappersBackend()
