import functools
import os
import sys
from typing import Any, Callable, Iterable, Optional, TextIO, Tuple

import click
from click import Command
from click_option_group import MutuallyExclusiveOptionGroup

from . import __version__
from .core import (
    CheckHashLineError,
    HashFileReader,
    HashFileWriter,
    ParseHashLineError,
    check_hash_line,
    generate_hash_line,
)
from .hasher import Hasher
from .utils.click import CommandX, PathWithSuffix
from .utils.glob import glob_filters, sorted_path


class ParseHashFileError(ValueError):
    def __init__(self, hash_line: str, lineno: int) -> None:
        super().__init__(hash_line, lineno)
        self.hash_line = hash_line
        self.lineno = lineno


class Output:
    """Determine the output mode and provide the output interface."""

    def __init__(
        self, agg: Optional[str] = None, sep: Optional[bool] = None, null: Optional[bool] = None, sync: bool = False
    ) -> None:
        if (agg and sep) or (agg and null) or (sep and null):
            raise ValueError("require exactly one argument")

        # Use the null mode by default.
        if not (agg or sep or null):
            null = True

        # Determine the output mode and dump method.
        if agg:
            self.agg_file = HashFileWriter(agg)
            self._dump = self.output_agg
        elif sep:
            self._dump = self.output_sep
        elif null:
            self._dump = self.output_null

        self.sync = sync
        self.maxmtime = 0.0

    def close(self) -> None:
        try:
            agg_file = self.agg_file
        except AttributeError:
            pass
        else:
            agg_file.close()
            if self.sync:
                os.utime(agg_file.name, (self.maxmtime, self.maxmtime))

    def dump(self, hash_line: str, hash_path: str, path: str) -> None:
        self._dump(hash_line, hash_path, path)

    def output_agg(self, hash_line: str, hash_path: str, path: str) -> None:
        self.agg_file.write_hash_line(hash_line)
        if self.sync:
            mtime = os.path.getmtime(path)
            self.maxmtime = max(self.maxmtime, mtime)

    def output_sep(self, hash_line: str, hash_path: str, path: str) -> None:
        with HashFileWriter(hash_path) as f:
            f.write_hash_line(hash_line)
        if self.sync:
            mtime = os.path.getmtime(path)
            os.utime(hash_path, (mtime, mtime))

    def output_null(self, hash_line: str, hash_path: str, path: str) -> None:
        pass


class Gethash:
    """Provide uniform interface for CLI scripts."""

    stdout: TextIO
    stderr: TextIO

    glob_mode: int
    glob_type: str

    inplace: bool
    root: Optional[str]

    start: Optional[int]
    stop: Optional[int]
    dir_ok: bool

    def __init__(self, ctx: Any, **kwargs: Any) -> None:
        self.ctx = ctx
        self.sync = kwargs.pop("sync", False)
        self.suffix = kwargs.pop("suffix", ".sha")

        self.stdout = kwargs.pop("stdout", sys.stdout)
        self.stderr = kwargs.pop("stderr", sys.stderr)

        self.glob_mode = kwargs.pop("glob", 1)
        self.glob_type = kwargs.pop("type", "a")

        # Determine the path format.
        self.inplace = kwargs.pop("inplace", False)
        self.root = kwargs.pop("root", None)

        # Determine the output mode.
        agg = kwargs.pop("agg", None)
        sep = kwargs.pop("sep", None)
        null = kwargs.pop("null", None)
        self.output = Output(agg, sep, null, sync=self.sync)

        # Prepare arguments and construct the hash function.
        self.start = kwargs.pop("start", None)
        self.stop = kwargs.pop("stop", None)
        self.dir_ok = kwargs.pop("dir", False)
        tqdm_args = {
            "file": self.stderr,
            "ascii": kwargs.pop("tqdm_ascii", False),
            "disable": kwargs.pop("tqdm_disable", False),
            "leave": kwargs.pop("tqdm_leave", False),
        }
        self.hasher = Hasher(ctx, tqdm_args=tqdm_args)

    def __call__(self, files: Iterable[str], *, check: bool) -> None:
        if check:
            self.check_hash(files)
        else:
            self.generate_hash(files)

    def __enter__(self) -> "Gethash":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def close(self) -> None:
        self.output.close()

    def generate_hash(self, patterns: Iterable[str]) -> None:
        for path in self.glob_function(patterns):
            try:
                root = self.check_root(path)
                hash_line = generate_hash_line(path, self.hash_function, root=root)
                hash_path = path + self.suffix
                self.output.dump(hash_line, hash_path, path)
            except Exception as e:
                self.echo_exception(path, e)
            else:
                # The hash line already has a newline.
                self.echo(hash_line, nl=False)

    def check_hash(self, patterns: Iterable[str]) -> None:
        for hash_path in self.glob_function(patterns):
            try:
                self._check_hash(hash_path)
            except ParseHashFileError as e:
                # Strip newline for pretty printing.
                hash_line = e.hash_line.rstrip("\n")
                msg = f"[ERROR] invalid hash '{hash_line}' in '{hash_path}' at line {e.lineno}"
                self.echo_error(msg, fg="white", bg="red")
            except Exception as e:
                self.echo_exception(hash_path, e)

    def _check_hash(self, hash_path: str) -> None:
        maxmtime = 0.0
        for i, hash_line in enumerate(HashFileReader(hash_path)):
            try:
                root = self.check_root(hash_path)
                path = check_hash_line(hash_line, self.hash_function, root=root)
                maxmtime = max(maxmtime, os.path.getmtime(path))
            except ParseHashLineError as e:
                raise ParseHashFileError(e.hash_line, i)
            except CheckHashLineError as e:
                self.echo(f"[FAILURE] {e.path}", fg="red")
            else:
                self.echo(f"[SUCCESS] {path}", fg="green")
        if self.sync:
            os.utime(hash_path, (maxmtime, maxmtime))

    def check_root(self, path: str) -> Optional[str]:
        if self.inplace:
            return os.path.dirname(path)
        return self.root

    def glob_function(self, paths: Iterable[str]) -> Iterable[str]:
        return sorted_path(
            glob_filters(paths, mode=self.glob_mode, type=self.glob_type, recursive=True, user=True, vars=True)
        )

    def hash_function(self, path: str) -> bytes:
        return self.hasher(path, self.start, self.stop, dir_ok=self.dir_ok)

    def echo(self, msg: str, **kwargs: Any) -> None:
        click.secho(msg, file=self.stdout, **kwargs)

    def echo_error(self, msg: str, **kwargs: Any) -> None:
        click.secho(msg, file=self.stderr, **kwargs)

    def echo_exception(self, path: str, exc: Exception) -> None:
        msg = f"[ERROR] {path}\n\t{type(exc).__name__}: {exc}"
        click.secho(msg, file=self.stderr, fg="red")


def script_main(ctx: Any, files: Tuple[str, ...], **options: Any) -> None:
    """Execute the body for the main function."""

    no_stdout = options.pop("no_stdout", False)
    no_stderr = options.pop("no_stderr", False)
    stdout = open(os.devnull, "w") if no_stdout else sys.stdout
    stderr = open(os.devnull, "w") if no_stderr else sys.stderr

    check = options.pop("check", False)
    with Gethash(ctx, stdout=stdout, stderr=stderr, **options) as gethash:
        gethash(files, check=check)


def gethashcli(command_name: str, display_name: str, **extras: Any) -> Callable[[Callable], Command]:
    """Apply click decorators to the main function."""

    suffix = extras.pop("suffix", "." + command_name.replace("-", "_"))
    doc = extras.pop("doc", None)

    def decorator(func: Callable) -> Command:
        if doc is not None:
            func.__doc__ = doc

        context_settings = dict(help_option_names=["-h", "--help"], max_content_width=120)

        path_format = MutuallyExclusiveOptionGroup("Path Format")
        output_mode = MutuallyExclusiveOptionGroup("Output Mode")

        @click.command(command_name, cls=CommandX, context_settings=context_settings, no_args_is_help=True)
        @click.argument("files", nargs=-1)
        @click.option(
            "-c",
            "--check",
            is_flag=True,
            help=f"Read {display_name} from FILES and check them.",
        )
        @click.option(
            "-y",
            "--sync",
            is_flag=True,
            help="Update mtime of hash files to the same as data files.",
        )
        @click.option(
            "-g",
            "--glob",
            type=click.IntRange(0, 2),
            metavar="[0|1|2]",
            default=1,
            show_default=True,
            help="Set glob mode. If ``0``, disable glob pathname pattern; if ``1``, "
            "resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.",
        )
        @click.option(
            "-t",
            "--type",
            type=click.Choice(["a", "d", "f"]),
            default="a",
            show_default=True,
            help="Set file type. If ``a``, include all types; if ``d``, include "
            "directories; if ``f``, include files.",
        )
        @path_format.option("-i", "--inplace", is_flag=True, help="Use basename in checksum files.")
        @path_format.option(
            "-z",
            "--root",
            type=click.Path(exists=True, file_okay=False),
            help="The path field in checksum files is relative to the root directory.",
        )
        @output_mode.option(
            "-o",
            "--agg",
            type=PathWithSuffix(suffix=suffix, dir_okay=False),
            help="Set the aggregate output file.",
        )
        @output_mode.option("-s", "--sep", is_flag=True, help="Separate output files.")
        @output_mode.option(
            "-n",
            "--null",
            is_flag=True,
            help="Do not output to files. This is the default output mode.",
        )
        @click.option("--start", type=click.IntRange(min=0), help="The start offset of files.")
        @click.option("--stop", type=click.IntRange(min=0), help="The stop offset of files.")
        @click.option(
            "-d",
            "--dir",
            is_flag=True,
            help="Allow checksum for directories. Just xor each checksum of files in a given directory.",
        )
        @click.option("--no-stdout", is_flag=True, help="Do not output to stdout.")
        @click.option("--no-stderr", is_flag=True, help="Do not output to stderr.")
        @click.option("--tqdm-ascii", type=click.BOOL, default=False, show_default=True)
        @click.option("--tqdm-disable", type=click.BOOL, default=False, show_default=True)
        @click.option("--tqdm-leave", type=click.BOOL, default=False, show_default=True)
        @click.version_option(__version__, "-V", "--version", prog_name=command_name)
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            kwargs.setdefault("suffix", suffix)
            return func(*args, **kwargs)

        return wrapper

    return decorator
