import sys
from contextlib import suppress
from typing import List, Optional

import click
from click import Command, Context
from natsort import natsort_keygen

from . import __version__
from .backends import Backend
from .utils.click import MultiCommandX

if sys.version_info[:2] < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

PROGRAM_NAME = "gethash"

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)
EXTRA_SETTINGS = dict(max_suggestions=5, cutoff=0.2)

COMMANDS = entry_points(group="gethash.commands")


class Cli(MultiCommandX):
    def list_commands(self, ctx: Context) -> List[str]:
        commands = set(COMMANDS.names)
        for backend in Backend.list_backends():
            commands.update(backend.algorithms_available)
        return sorted(commands, key=natsort_keygen())

    def get_command(self, ctx: Context, name: str) -> Optional[Command]:
        with suppress(KeyError, ImportError):
            return COMMANDS[name].load()
        for backend in Backend.list_backends():
            with suppress(Exception):
                return backend.load_cmd(name)
        return None


@click.command(PROGRAM_NAME, cls=Cli, context_settings=CONTEXT_SETTINGS, **EXTRA_SETTINGS)
@click.version_option(__version__, "-V", "--version", prog_name=PROGRAM_NAME)
def main() -> None:
    """Generate or check various hash values."""


if __name__ == "__main__":
    main()
