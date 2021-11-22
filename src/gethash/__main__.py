from contextlib import suppress
from typing import List, Optional

import click
from click import Command, Context
from importlib_metadata import entry_points

from . import __version__
from .utils.click import MultiCommand

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
        return sorted(plugins)

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
