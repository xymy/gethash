import functools
import os
import sys

import click
from click_option_group import MutuallyExclusiveOptionGroup

from . import __version__
from .core import CheckHashLineError, Hasher, check_hash_line, generate_hash_line
from .utils import cprint, glob_scanner, wrap_stream


class Output(object):
    """Determine the output mode and provide the output interface."""

    def __init__(self, sep, agg, null):
        if (sep and agg) or (sep and null) or (agg and null):
            raise ValueError

        # Use the sep mode by default.
        if not (sep or agg or null):
            sep = True

        if sep:
            self._dump = self.output_sep
        elif agg:
            self.agg_file = agg
            self._dump = self.output_agg
        elif null:
            self._dump = self.output_null

    @staticmethod
    def output_sep(hash_line, hash_path):
        with open(hash_path, "w", encoding="utf-8") as f:
            f.write(hash_line)

    def output_agg(self, hash_line, hash_path):
        self.agg_file.write(hash_line)

    @staticmethod
    def output_null(hash_line, hash_path):
        pass

    def dump(self, hash_line, hash_path):
        self._dump(hash_line, hash_path)


class GetHash(object):
    """Provide uniform interface for cli scripts."""

    def __init__(self, ctx, suffix=".sha", **kwargs):
        self.ctx = ctx
        self.suffix = suffix

        self.glob_mode = int(kwargs.pop("glob", 1))

        self.stdout = wrap_stream(kwargs.pop("stdout", sys.stdout))
        self.stderr = wrap_stream(kwargs.pop("stderr", sys.stderr))

        self.inplace = kwargs.pop("inplace", False)
        self.root = kwargs.pop("root", None)

        # Determine the output mode.
        sep = kwargs.pop("sep", None)
        agg = kwargs.pop("agg", None)
        null = kwargs.pop("null", None)
        self.dump = Output(sep, agg, null).dump

        # Prepare arguments and construct the hash function.
        start = kwargs.pop("start", None)
        stop = kwargs.pop("stop", None)
        dir_ok = kwargs.pop("dir", False)
        tqdm_args = {
            "file": self.stderr,
            "leave": kwargs.pop("tqdm-leave", False),
            "ascii": kwargs.pop("tqdm-ascii", True),
        }
        hasher = Hasher(ctx, tqdm_args=tqdm_args)
        self.hash_function = functools.partial(
            hasher, start=start, stop=stop, dir_ok=dir_ok
        )

    def echo(self, msg, **kwargs):
        cprint(msg, file=self.stdout, **kwargs)

    def echo_error(self, path, exc):
        msg = "[ERROR] {}\n\t{}: {}".format(path, type(exc).__name__, exc)
        cprint(msg, file=self.stderr, fg="red")

    def check_root(self, path):
        if self.root is not None:
            return self.root
        if self.inplace:
            return os.path.dirname(path)
        return None

    def generate_hash(self, patterns):
        for path in glob_scanner(patterns, mode=self.glob_mode):
            try:
                root = self.check_root(path)
                hash_line = generate_hash_line(path, self.hash_function, root=root)
                hash_path = path + self.suffix
                self.dump(hash_line, hash_path)
            except Exception as e:
                self.echo_error(path, e)
            else:
                # The hash line already has a newline.
                self.echo(hash_line, end='')

    def _check_hash(self, hash_line, hash_path):
        try:
            root = self.check_root(hash_path)
            path = check_hash_line(hash_line, self.hash_function, root=root)
        except CheckHashLineError as e:
            self.echo("[FAILURE] {}".format(e.path), fg="red")
        except Exception as e:
            self.echo_error(hash_path, e)
        else:
            self.echo("[SUCCESS] {}".format(path), fg="green")

    def check_hash(self, patterns):
        for hash_path in glob_scanner(patterns, mode=self.glob_mode):
            try:
                with open(hash_path, "r", encoding="utf-8") as f:
                    # This function can process multiple hash lines.
                    for hash_line in f:
                        if hash_line.isspace():
                            continue
                        self._check_hash(hash_line, hash_path)
            except Exception as e:
                self.echo_error(hash_path, e)

    def __call__(self, check, files):
        if check:
            self.check_hash(files)
        else:
            self.generate_hash(files)


def script_main(ctx, suffix, check, files, **options):
    """Generate the main body for the main function."""

    # Convert bool flags to streams.
    no_stdout = options.pop("no_stdout", False)
    no_stderr = options.pop("no_stderr", False)
    stdout = open(os.devnull, "w") if no_stdout else sys.stdout
    stderr = open(os.devnull, "w") if no_stderr else sys.stderr
    # Initialize and invoke.
    GetHash(ctx, suffix, stdout=stdout, stderr=stderr, **options)(check, files)


def gethashcli(name):
    """Generate click decorators for the main function."""

    def decorator(func):
        path_format = MutuallyExclusiveOptionGroup("Path Format")
        output_mode = MutuallyExclusiveOptionGroup(
            "Output Mode", help="Ignored when -c is set."
        )

        @click.command(no_args_is_help=True)
        @click.option(
            "-c",
            "--check",
            is_flag=True,
            help="Read {} from FILES and check them.".format(name),
        )
        @click.option(
            "-d", "--dir", is_flag=True, help="Allow checksum for directories."
        )
        @click.option("--start", type=click.INT, help="The start offset of files.")
        @click.option("--stop", type=click.INT, help="The stop offset of files.")
        @click.option(
            "--glob",
            type=click.Choice(["0", "1", "2"]),
            default="1",
            show_default=True,
            help="Set glob mode.",
        )
        @path_format.option(
            "-i", "--inplace", is_flag=True, help="Use basename in checksum files."
        )
        @path_format.option(
            "--root", default=None, help="Relative to root in checksum files."
        )
        @output_mode.option("--sep", is_flag=True, help="Separate output files.")
        @output_mode.option(
            "--agg",
            type=click.File("w", encoding="utf-8"),
            default=None,
            help="Specify the aggregate output file.",
        )
        @output_mode.option("--null", is_flag=True, help="Disable output files.")
        @click.option("--no-stdout", is_flag=True, help="Do not output to stdout.")
        @click.option("--no-stderr", is_flag=True, help="Do not output to stderr.")
        @click.option("--tqdm-leave", type=click.BOOL, default=False, show_default=True)
        @click.option("--tqdm-ascii", type=click.BOOL, default=True, show_default=True)
        @click.version_option(__version__)
        @click.argument("files", nargs=-1)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
