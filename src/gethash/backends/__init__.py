import abc
from contextlib import suppress
from typing import Any, List, Set, Tuple

from click import Command

from gethash.hasher import HashContext
from gethash.script import gethashcli, script_main

__all__ = ["Backend"]


class Backend(metaclass=abc.ABCMeta):
    _registry: List["Backend"] = []

    @classmethod
    def register_backend(cls) -> None:
        cls._registry.append(cls())

    @classmethod
    def list_backends(cls) -> List["Backend"]:
        return cls._registry

    @property
    @abc.abstractmethod
    def algorithms_available(self) -> Set[str]:
        """Return a set containing the names of the hash algorithms that are
        available in the backend."""

    @abc.abstractmethod
    def load_ctx(self, name: str) -> HashContext:
        """Load context."""

    def load_cmd(self, name: str) -> Command:
        """Load command."""

        if name not in self.algorithms_available:
            raise ValueError(f"unkown algorithm {name!r}")

        display_name = name.upper()
        doc = f"""Generate or check {display_name}."""

        @gethashcli(command_name=name, display_name=display_name, doc=doc)
        def main(files: Tuple[str, ...], **kwargs: Any) -> None:

            ctx = self.load_ctx(name)
            script_main(ctx, files, **kwargs)

        return main


def _load_backend() -> None:
    from .hashlib import HashlibBackend

    HashlibBackend.register_backend()

    # For optional cryptographic backend.
    with suppress(ImportError):
        from .pycryptodome import PyCryptodomeBackend

        PyCryptodomeBackend.register_backend()


_load_backend()
