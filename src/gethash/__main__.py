import sys
from contextlib import suppress
from typing import List, Optional, cast

import click
from click import Command, Context
from natsort import natsorted

from . import __version__
from .utils.click import MultiCommand

if sys.version_info[:2] < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

try:
    import Cryptodome
except ImportError:
    PYCRYPTODOMEX_INSTALLED = False
else:
    PYCRYPTODOMEX_INSTALLED = True
    del Cryptodome

PROGRAM_NAME = "gethash"

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], max_content_width=120)

PLUGINS = entry_points(group="gethash.plugins")
LEGACY_PLUGINS = entry_points(group="gethash.legacy_plugins")


class Cli(MultiCommand):
    def list_commands(self, ctx: Context) -> List[str]:
        plugins = list(PLUGINS.names)
        if PYCRYPTODOMEX_INSTALLED:
            plugins.extend(LEGACY_PLUGINS.names)
        return cast(List[str], natsorted(plugins))

    def get_command(self, ctx: Context, name: str) -> Optional[Command]:
        with suppress(KeyError, ImportError):
            return PLUGINS[name].load()
        if PYCRYPTODOMEX_INSTALLED:
            with suppress(KeyError, ImportError):
                return LEGACY_PLUGINS[name].load()
        return None


@click.command(PROGRAM_NAME, cls=Cli, context_settings=CONTEXT_SETTINGS, max_suggestions=5, cutoff=0.2)
@click.version_option(__version__, "-V", "--version", prog_name=PROGRAM_NAME)
def main() -> None:
    """Generate or check various hash values."""


if __name__ == "__main__":
    main()
