from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

import Crypto  # noqa: F401

from . import Backend

if TYPE_CHECKING:
    from ..hasher import HashContext


class PyCryptodomeBackend(Backend):
    _algorithms = frozenset({"md2", "md4", "ripemd160"})

    @property
    def algorithms_available(self) -> frozenset[str]:
        return self._algorithms

    def load_ctx(self, name: str) -> HashContext:
        # The `name` has been checked in `load_cmd`.
        module = import_module(f"Crypto.Hash.{name.upper()}")
        return module.new()


def load() -> PyCryptodomeBackend:
    return PyCryptodomeBackend()
