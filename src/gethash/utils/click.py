import sys

import click


class Command(click.Command):
    def main(self, args=None, *pargs, **kwargs):
        args = args or sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class MultiCommand(click.MultiCommand):
    def main(self, args=None, *pargs, **kwargs):
        args = args or sys.argv[1:]
        return super().main(args, *pargs, **kwargs)
