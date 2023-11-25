from __future__ import annotations

import sys
from collections.abc import Sequence
from typing import Any

import click
from click_didyoumean import DYMMixin


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
