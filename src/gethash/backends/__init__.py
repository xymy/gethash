import abc
from contextlib import suppress
from typing import Any, List, Set, Tuple

import click

from gethash.script import gethashcli, script_main

__all__ = ["Backend"]


class Backend(metaclass=abc.ABCMeta):
    _registry: List["Backend"] = []

    @classmethod
    def register_backend(cls, backend: "Backend") -> None:
        cls._registry.append(backend)

    @classmethod
    def list_backends(cls) -> List["Backend"]:
        return cls._registry

    @property
    @abc.abstractmethod
    def algorithms_available(self) -> Set[str]:
        """Return a set containing the names of the hash algorithms that are
        available in the backend."""

    @abc.abstractmethod
    def load_ctx(self, name: str) -> Any:
        """Load context."""

    def load_cmd(self, name: str) -> click.Command:
        """Load command."""

        doc = f"""Generate or check {name.upper()}."""

        @gethashcli(command_name=name, display_name=name.upper(), doc=doc)
        def main(files: Tuple[str, ...], **kwargs: Any) -> None:

            ctx = self.load_ctx(name)
            script_main(ctx, files, **kwargs)

        return main


def _load_backend() -> None:
    from .hashlib import HashlibBackend

    Backend.register_backend(HashlibBackend())

    # For optional cryptographic backend.
    with suppress(ImportError):
        from .pycryptodome import PyCryptodomeBackend

        Backend.register_backend(PyCryptodomeBackend())


_load_backend()
