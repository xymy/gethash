import sys
from typing import Any, Optional, Sequence

import click
from click import Context, Parameter
from click_didyoumean import DYMMixin

__all__ = ["Command", "MultiCommand", "PathWithSuffix"]


class Command(click.Command):
    def main(self, args: Optional[Sequence[str]] = None, *pargs: Any, **kwargs: Any) -> Any:
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class MultiCommand(DYMMixin, click.MultiCommand):
    def main(self, args: Optional[Sequence[str]] = None, *pargs: Any, **kwargs: Any) -> Any:
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class PathWithSuffix(click.Path):
    def __init__(self, suffix: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.suffix = suffix

    def convert(self, value: str, param: Optional[Parameter], ctx: Optional[Context]) -> str:
        if self.file_okay and self.allow_dash and value == "-":
            return super().convert(value, param, ctx)

        suffix = self.suffix
        if value is not None and value[-len(suffix) :].lower() != suffix.lower():
            value += suffix
        return super().convert(value, param, ctx)
