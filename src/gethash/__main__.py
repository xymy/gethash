from contextlib import suppress

import click
from importlib_metadata import entry_points

from . import __title__, __version__
from .utils.click import MultiCommand

try:
    import Cryptodome
except ImportError:
    PYCRYPTODOMEX_INSTALLED = False
else:
    PYCRYPTODOMEX_INSTALLED = True
    del Cryptodome

PLUGINS = entry_points(group="gethash.plugins")
LEGACY_PLUGINS = entry_points(group="gethash.legacy_plugins")


class Cli(MultiCommand):
    def list_commands(self, ctx):
        plugins = list(PLUGINS.names)
        if PYCRYPTODOMEX_INSTALLED:
            plugins.extend(LEGACY_PLUGINS.names)
        return sorted(plugins)

    def get_command(self, ctx, name):
        with suppress(KeyError, ImportError):
            return PLUGINS[name].load()
        if PYCRYPTODOMEX_INSTALLED:
            with suppress(KeyError, ImportError):
                return LEGACY_PLUGINS[name].load()
        return None


@click.command(__title__, cls=Cli)
@click.version_option(__version__, prog_name=__title__)
def main():
    """Generate or check various hash values."""


if __name__ == "__main__":
    main()
