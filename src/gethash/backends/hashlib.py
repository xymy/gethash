import hashlib
from typing import Set

from gethash.hasher import HashContext

from . import Backend


class HashlibBackend(Backend):
    _algorithms = {name.replace("_", "-") for name in hashlib.algorithms_available} - {"shake-128", "shake-256"}

    @property
    def algorithms_available(self) -> Set[str]:
        return self._algorithms

    def load_ctx(self, name: str) -> HashContext:
        # The ``name`` has been checked in ``load_cmd``.
        try:
            return hashlib.new(name.replace("-", "_"))
        except ValueError:
            return hashlib.new(name)
