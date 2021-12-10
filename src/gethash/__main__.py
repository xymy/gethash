import sys
from contextlib import suppress
from typing import List, Optional

import click
from click import Command, Context
from natsort import natsort_keygen

from . import __version__
from .utils.click import MultiCommand

if sys.version_info[:2] < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

try:
    import Crypto
except ImportError:
    PYCRYPTODOMEX_INSTALLED = False
else:
    PYCRYPTODOMEX_INSTALLED = True
    del Crypto

PROGRAM_NAME = "gethash"

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)

COMMANDS = entry_points(group="gethash.commands")
LEGACY_COMMANDS = entry_points(group="gethash.legacy_commands")


class Cli(MultiCommand):
    def list_commands(self, ctx: Context) -> List[str]:
        commands = list(COMMANDS.names)
        if PYCRYPTODOMEX_INSTALLED:
            commands.extend(LEGACY_COMMANDS.names)
        commands.sort(key=natsort_keygen())
        return commands

    def get_command(self, ctx: Context, name: str) -> Optional[Command]:
        with suppress(KeyError, ImportError):
            return COMMANDS[name].load()
        if PYCRYPTODOMEX_INSTALLED:
            with suppress(KeyError, ImportError):
                return LEGACY_COMMANDS[name].load()
        return None


@click.command(PROGRAM_NAME, cls=Cli, context_settings=CONTEXT_SETTINGS, max_suggestions=5, cutoff=0.2)
@click.version_option(__version__, "-V", "--version", prog_name=PROGRAM_NAME)
def main() -> None:
    """Generate or check various hash values."""


if __name__ == "__main__":
    main()
