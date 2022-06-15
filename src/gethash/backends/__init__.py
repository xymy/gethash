import abc
from typing import Any, Set, Tuple

from click import Command

from ..hasher import HashContext
from ..script import gethashcli, script_main

__all__ = ["Backend"]


class Backend(metaclass=abc.ABCMeta):
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
