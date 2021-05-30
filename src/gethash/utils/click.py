import sys

import click


class Context(click.Context):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_content_width", 120)
        kwargs.setdefault("help_option_names", ["-h", "--help"])
        super().__init__(*args, **kwargs)


class Command(click.Command):
    context_class = Context

    def main(self, args=None, *pargs, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class MultiCommand(click.MultiCommand):
    context_class = Context

    def main(self, args=None, *pargs, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class Group(click.Group):
    context_class = Context

    def main(self, args=None, *pargs, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class CommandCollection(click.CommandCollection):
    context_class = Context

    def main(self, args=None, *pargs, **kwargs):
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)
