from importlib import import_module
from pathlib import Path

import click

PLUGINS_DIR = Path(__file__).parent / "cli"


class Cli(click.MultiCommand):
    def list_commands(self, ctx):
        scripts = PLUGINS_DIR.glob("[!_]*.py")
        return sorted(script.stem for script in scripts)

    def get_command(self, ctx, name):
        entry_point = None
        try:  # import from plugins directory
            module = import_module(f".{name}", "gethash.cli")
        except ImportError:
            pass
        else:
            try:  # get `main` function as entry point
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
