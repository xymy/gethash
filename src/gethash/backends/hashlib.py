from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from . import Backend

if TYPE_CHECKING:
    from ..hasher import HashContext


class HashlibBackend(Backend):
    _algorithms = frozenset(
        {name.replace("_", "-") for name in hashlib.algorithms_available} - {"shake-128", "shake-256"}
    )

    @property
    def algorithms_available(self) -> frozenset[str]:
        return self._algorithms

    def load_ctx(self, name: str) -> HashContext:
        # The `name` has been checked in `load_cmd`.
        try:
            return hashlib.new(name.replace("-", "_"))
        except ValueError:
            return hashlib.new(name)


def load() -> HashlibBackend:
    return HashlibBackend()
