from importlib import import_module

import click

from . import __title__, __version__

PYCRYPTODOMEX_INSTALLED = True
try:
    import Cryptodome
except ImportError:
    PYCRYPTODOMEX_INSTALLED = False
else:
    del Cryptodome

PLUGINS = [
    "crc32",
    "md5",
    "sha1",
    "sha256",
    "sha512",
    "sha3-256",
    "sha3-512",
    "blake2b",
    "blake2s",
]

LEGACY_PLUGINS = ["md2", "md4", "ripemd160"]

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


class Cli(click.MultiCommand):
    def list_commands(self, ctx):
        plugins = list(PLUGINS)
        if PYCRYPTODOMEX_INSTALLED:
            plugins.extend(LEGACY_PLUGINS)
        return plugins

    def get_command(self, ctx, name):
        name = name.replace("-", "_")  # fix dash to underline
        entry_point = None
        try:
            module = import_module(f"gethash.cli.{name}")
        except ImportError:
            pass
        else:
            main = getattr(module, "main", None)
            if isinstance(main, click.Command):
                entry_point = main
        return entry_point


@click.command(
    __title__, cls=Cli, context_settings=CONTEXT_SETTINGS, no_args_is_help=True
)
@click.version_option(__version__, prog_name=__title__)
def main():
    pass


if __name__ == "__main__":
    main()
