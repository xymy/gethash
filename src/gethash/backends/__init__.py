from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any

from ..script import gethashcli, script_main

if TYPE_CHECKING:
    from click import Command

    from ..hasher import HashContext

__all__ = ["Backend"]


class Backend(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def algorithms_available(self) -> frozenset[str]:
        """Return a set containing the names of the hash algorithms that are
        available in the backend."""

    @abc.abstractmethod
    def load_ctx(self, name: str) -> HashContext:
        """Load context."""

    def load_cmd(self, name: str) -> Command:
        """Load command."""

        # Check `name` before invoking `main` for fast failure.
        if name not in self.algorithms_available:
            raise ValueError(f"unkown algorithm {name!r}")

        display_name = name.upper()
        doc = f"""Generate or check {display_name}."""

        @gethashcli(command_name=name, display_name=display_name, doc=doc)
        def main(files: tuple[str, ...], **kwargs: Any) -> None:
            ctx = self.load_ctx(name)
            script_main(ctx, files, **kwargs)

        return main
