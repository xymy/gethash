from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

from . import Backend

if TYPE_CHECKING:
    from ..hasher import HashContext


class WrappersBackend(Backend):
    _algorithms = frozenset({"crc32"})

    @property
    def algorithms_available(self) -> frozenset[str]:
        return self._algorithms

    def load_ctx(self, name: str) -> HashContext:
        # The `name` has been checked in `load_cmd`.
        module = import_module(f"gethash.wrappers.{name}")
        return module.new()


def load() -> WrappersBackend:
    return WrappersBackend()
