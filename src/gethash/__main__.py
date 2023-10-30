from __future__ import annotations

from collections.abc import Iterator
from contextlib import suppress
from typing import Any

import click
from click import Command, Context
from importlib_metadata import entry_points
from natsort import natsort_keygen

from . import __version__
from .backends import Backend
from .utils.click import MultiCommandX

PROGRAM_NAME = "gethash"
CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"], "max_content_width": 120}
EXTRA_SETTINGS = {"max_suggestions": 5, "cutoff": 0.2}


class Cli(MultiCommandX):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._ep_commands = entry_points(group="gethash.commands")
        self._ep_backends = entry_points(group="gethash.backends")

    def _iter_backends(self) -> Iterator[Backend]:
        for ep in self._ep_backends:
            with suppress(ImportError):
                backend = ep.load()()
                assert isinstance(backend, Backend)
                yield backend

    def list_commands(self, ctx: Context) -> list[str]:
        commands = set(self._ep_commands.names)
        for backend in self._iter_backends():
            commands.update(backend.algorithms_available)
        return sorted(commands, key=natsort_keygen())

    def get_command(self, ctx: Context, name: str) -> Command | None:
        with suppress(KeyError, ImportError):
            cmd = self._ep_commands[name].load()
            assert isinstance(cmd, Command)
            return cmd
        for backend in self._iter_backends():
            with suppress(Exception):
                return backend.load_cmd(name)
        return None


@click.command(PROGRAM_NAME, cls=Cli, context_settings=CONTEXT_SETTINGS, **EXTRA_SETTINGS)
@click.version_option(__version__, "-V", "--version", prog_name=PROGRAM_NAME)
def main() -> None:
    """Generate or check various hash values."""


if __name__ == "__main__":
    main()
