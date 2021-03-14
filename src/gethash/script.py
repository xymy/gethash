import functools
import os
import sys

import click
from click_option_group import MutuallyExclusiveOptionGroup

from . import __version__
from .core import (
    CheckHashLineError,
    Hasher,
    HashFileReader,
    HashFileWriter,
    check_hash_line,
    generate_hash_line,
)
from .utils.glob import glob_filters


class FilePath(click.Path):
    def __init__(
        self,
        exists=False,
        writable=False,
        readable=False,
        resolve_path=False,
        allow_dash=False,
        path_type=None,
        suffix=".sha",
    ):
        super().__init__(
            exists=exists,
            file_okay=True,
            dir_okay=False,
            writable=writable,
            readable=readable,
            resolve_path=resolve_path,
            allow_dash=allow_dash,
            path_type=path_type,
        )
        self.suffix = suffix

    def convert(self, value, param, ctx):
        suffix = self.suffix
        # Add suffix automatically.
        if value is not None and value[-len(suffix) :].lower() != suffix.lower():
            value += suffix
        return super().convert(value, param, ctx)


class Output(object):
    """Determine the output mode and provide the output interface."""

    def __init__(self, sep=None, agg=None, null=None):
        if (sep and agg) or (sep and null) or (agg and null):
            raise ValueError("require exactly one argument")

        # Use the null mode by default.
        if not (sep or agg or null):
            null = True

        # Determine the output mode and dump method.
        if sep:
            self._dump = self.output_sep
        elif agg:
            self.agg_file = HashFileWriter(agg)
            self._dump = self.output_agg
        elif null:
            self._dump = self.output_null

    def close(self):
        try:
            agg_file = self.agg_file
        except AttributeError:
            pass
        else:
            agg_file.close()

    def dump(self, hash_line, hash_path):
        self._dump(hash_line, hash_path)

    def output_sep(self, hash_line, hash_path):
        with HashFileWriter(hash_path) as f:
            f.write_hash_line(hash_line)

    def output_agg(self, hash_line, hash_path):
        self.agg_file.write_hash_line(hash_line)

    @staticmethod
    def output_null(hash_line, hash_path):
        pass


class GetHash(object):
    """Provide uniform interface for CLI scripts."""

    def __init__(self, ctx, **kwargs):
        self.ctx = ctx

        self.glob_mode = kwargs.pop("glob", 1)
        self.glob_type = kwargs.pop("type", "a")
        self.suffix = kwargs.pop("suffix", ".sha")

        # Determine the path format.
        self.inplace = kwargs.pop("inplace", False)
        self.root = kwargs.pop("root", None)

        # Determine the output mode.
        sep = kwargs.pop("sep", None)
        agg = kwargs.pop("agg", None)
        null = kwargs.pop("null", None)
        self.output = Output(sep, agg, null)
        self.dump = self.output.dump

        self.stdout = kwargs.pop("stdout", sys.stdout)
        self.stderr = kwargs.pop("stderr", sys.stderr)

        # Prepare arguments and construct the hash function.
        start = kwargs.pop("start", None)
        stop = kwargs.pop("stop", None)
        dir_ok = kwargs.pop("dir", False)
        tqdm_args = {
            "file": self.stderr,
            "ascii": kwargs.pop("tqdm-ascii", True),
            "disable": kwargs.pop("tqdm-disable", False),
            "leave": kwargs.pop("tqdm-leave", False),
        }
        hasher = Hasher(ctx, tqdm_args=tqdm_args)
        self.hash_function = functools.partial(
            hasher, start=start, stop=stop, dir_ok=dir_ok
        )

    def echo(self, msg, **kwargs):
        click.secho(msg, file=self.stdout, **kwargs)

    def echo_error(self, path, exc):
        msg = f"[ERROR] {path}\n\t{type(exc).__name__}: {exc}"
        click.secho(msg, file=self.stderr, fg="red")

    def check_root(self, path):
        if self.inplace:
            return os.path.dirname(path)
        if self.root is not None:
            return self.root
        return None

    def generate_hash(self, patterns):
        for path in glob_filters(patterns, mode=self.glob_mode, type=self.glob_type):
            try:
                root = self.check_root(path)
                hash_line = generate_hash_line(path, self.hash_function, root=root)
                hash_path = path + self.suffix
                self.dump(hash_line, hash_path)
            except Exception as e:
                self.echo_error(path, e)
            else:
                # The hash line already has a newline.
                self.echo(hash_line, nl=False)

    def _check_hash(self, hash_path):
        for hash_line in HashFileReader(hash_path):
            try:
                root = self.check_root(hash_path)
                path = check_hash_line(hash_line, self.hash_function, root=root)
            except CheckHashLineError as e:
                self.echo(f"[FAILURE] {e.path}", fg="red")
            except Exception as e:
                self.echo_error(hash_path, e)
            else:
                self.echo(f"[SUCCESS] {path}", fg="green")

    def check_hash(self, patterns):
        for hash_path in glob_filters(
            patterns, mode=self.glob_mode, type=self.glob_type
        ):
            try:
                self._check_hash(hash_path)
            except Exception as e:
                self.echo_error(hash_path, e)

    def close(self):
        self.output.close()

    def __call__(self, check, files):
        if check:
            self.check_hash(files)
        else:
            self.generate_hash(files)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def script_main(ctx, files, **options):
    """Generate the body for the main function."""

    check = options.pop("check", False)
    # Convert bool flags to streams.
    no_stdout = options.pop("no_stdout", False)
    no_stderr = options.pop("no_stderr", False)
    stdout = open(os.devnull, "w") if no_stdout else sys.stdout
    stderr = open(os.devnull, "w") if no_stderr else sys.stderr

    with GetHash(ctx, stdout=stdout, stderr=stderr, **options) as gh:
        gh(check, files)


def gethashcli(cmdname, hashname, suffix):
    """Generate click decorators for the main function."""

    def decorator(func):
        path_format = MutuallyExclusiveOptionGroup(
            "Path Format", help="Set the path format in checksum files."
        )
        output_mode = MutuallyExclusiveOptionGroup(
            "Output Mode", help="Ignored when -c is set."
        )

        @click.command(
            cmdname,
            context_settings=dict(help_option_names=["-h", "--help"]),
            no_args_is_help=True,
        )
        @click.argument("files", nargs=-1)
        @click.option(
            "-c",
            "--check",
            is_flag=True,
            help=f"Read {hashname} from FILES and check them.",
        )
        @click.option("--start", type=click.INT, help="The start offset of files.")
        @click.option("--stop", type=click.INT, help="The stop offset of files.")
        @click.option(
            "-d",
            "--dir",
            is_flag=True,
            help="Allow checksum for directories. "
            "Just xor each checksum of files in a given directory.",
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
        @click.option(
            "--suffix",
            metavar="SUFFIX",
            default=suffix,
            show_default=True,
            help="Set the filename extension of checksum files.",
        )
        @path_format.option(
            "-i", "--inplace", is_flag=True, help="Use basename in checksum files."
        )
        @path_format.option(
            "-z",
            "--root",
            type=click.Path(
                exists=True,
                file_okay=False,
                dir_okay=True,
                writable=False,
                readable=False,
            ),
            default=None,
            help="The path field in checksum files is relative to the root directory.",
        )
        @output_mode.option("-s", "--sep", is_flag=True, help="Separate output files.")
        @output_mode.option(
            "-o",
            "--agg",
            type=FilePath(suffix=suffix),
            default=None,
            help="Set the aggregate output file.",
        )
        @output_mode.option(
            "-n",
            "--null",
            is_flag=True,
            help="Do not output to files. This is the default output mode.",
        )
        @click.option("--tqdm-ascii", type=click.BOOL, default=False, show_default=True)
        @click.option(
            "--tqdm-disable", type=click.BOOL, default=False, show_default=True
        )
        @click.option("--tqdm-leave", type=click.BOOL, default=False, show_default=True)
        @click.option("--no-stdout", is_flag=True, help="Do not output to stdout.")
        @click.option("--no-stderr", is_flag=True, help="Do not output to stderr.")
        @click.version_option(__version__, prog_name=cmdname)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
