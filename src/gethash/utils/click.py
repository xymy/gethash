import sys
from typing import Any, Optional, Sequence

import click


class Command(click.Command):
    def main(
        self, args: Optional[Sequence[str]] = None, *pargs: Any, **kwargs: Any
    ) -> Any:
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class MultiCommand(click.MultiCommand):
    def main(
        self, args: Optional[Sequence[str]] = None, *pargs: Any, **kwargs: Any
    ) -> Any:
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class Group(click.Group):
    def main(
        self, args: Optional[Sequence[str]] = None, *pargs: Any, **kwargs: Any
    ) -> Any:
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class CommandCollection(click.CommandCollection):
    def main(
        self, args: Optional[Sequence[str]] = None, *pargs: Any, **kwargs: Any
    ) -> Any:
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)
