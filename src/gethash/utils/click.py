from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import Any, cast

import click
from click import Context, Parameter
from click_didyoumean import DYMMixin

__all__ = ["CommandX", "MultiCommandX", "PathWithSuffix"]


class CommandX(click.Command):
    def main(self, args: Sequence[str] | None = None, *pargs: Any, **kwargs: Any) -> Any:
        # Avoid command-line arguments expansion on Windows.
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class MultiCommandX(DYMMixin, click.MultiCommand):
    def main(self, args: Sequence[str] | None = None, *pargs: Any, **kwargs: Any) -> Any:
        # Avoid command-line arguments expansion on Windows.
        if args is None:
            args = sys.argv[1:]
        return super().main(args, *pargs, **kwargs)


class PathWithSuffix(click.Path):
    def __init__(self, suffix: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.suffix = suffix

    def convert(self, value: str, param: Parameter | None, ctx: Context | None) -> str:
        if self.file_okay and self.allow_dash and value == "-":
            return cast(str, super().convert(value, param, ctx))

        suffix = self.suffix
        if value is not None and value[-len(suffix) :].lower() != suffix.lower():
            value += suffix
        return cast(str, super().convert(value, param, ctx))
