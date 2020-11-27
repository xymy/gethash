from importlib import import_module

import click

PYCRYPTODOMEX_INSTALLED = True
try:
    import Cryptodome
except ImportError:
    PYCRYPTODOMEX_INSTALLED = False
else:
    del Cryptodome

PLUGINS = (
    "md5",
    "sha1",
    "sha256",
    "sha512",
    "sha3-256",
    "sha3-512",
    "blake2b",
    "blake2s",
)

LEGACY_PLUGINS = ("md2", "md4", "ripemd160")


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
            # Import from plugins directory.
            module = import_module("gethash.cli.{}".format(name))
        except ImportError:
            pass
        else:
            try:
                # Get `main` function as entry point.
                main = module.main
            except AttributeError:
                pass
            else:
                # Is `main` a valid command?
                if isinstance(main, click.Command):
                    entry_point = main
        return entry_point


@click.command(cls=Cli, no_args_is_help=True)
def main():
    pass


if __name__ == "__main__":
    main()
