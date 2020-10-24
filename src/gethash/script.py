import functools
import os
import sys
from glob import iglob

import click

from . import __version__
from .core import CheckHashLineError, Hasher, check_hash_line, generate_hash_line


class GetHash(object):
    """Provide uniform interface for cli scripts."""

    def __init__(self, ctx, suffix=".sha", **kwargs):
        self.ctx = ctx
        self.suffix = suffix

        self.inplace = kwargs.pop("inplace", False)
        self.glob_flag = kwargs.pop("glob", True)
        self.out_mode = kwargs.pop("out", "sep")
        self.agg_file = kwargs.pop("agg", None)

        if self.agg_file is not None:
            self.out_mode = "agg"

        self.stdout = kwargs.pop("stdout", sys.stdout)
        self.stderr = kwargs.pop("stderr", sys.stderr)

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
        click.echo(msg, file=self.stdout, **kwargs)

    def secho(self, msg, **kwargs):
        click.secho(msg, file=self.stdout, **kwargs)

    def echo_error(self, path, exc):
        message = "[ERROR] {}\n\t{}: {}".format(path, type(exc).__name__, exc)
        click.secho(message, file=self.stderr, fg="red")

    @property
    def glob(self):
        if self.glob_flag:
            return iglob

        def dummy_glob(pattern):
            yield pattern

        return dummy_glob

    def scan(self, patterns):
        for pattern in patterns:
            for path in map(os.path.normpath, self.glob(pattern)):
                yield path

    def output_file(self, hash_line, hash_path):
        out_mode = self.out_mode
        if out_mode == "sep":
            with open(hash_path, "w", encoding="utf-8") as f:
                f.write(hash_line)
        elif out_mode == "agg":
            self.agg_file.write(hash_line)
        elif out_mode == "null":
            pass

    def generate_hash(self, patterns):
        for path in self.scan(patterns):
            try:
                root = None
                if self.inplace:
                    root = os.path.dirname(path)
                hash_line = generate_hash_line(
                    self.hash_function, path, root=root
                )
                hash_path = path + self.suffix
                self.output_file(hash_line, hash_path)
            except Exception as e:
                self.echo_error(path, e)
            else:
                # The hash line already has a newline.
                self.echo(hash_line, nl=False)

    def _check_hash(self, hash_line, hash_path):
        try:
            root = None
            if self.inplace:
                root = os.path.dirname(hash_path)
            path = check_hash_line(self.hash_function, hash_line, root=root)
        except CheckHashLineError as e:
            self.secho("[FAILURE] {}".format(e.path), fg="red")
        except Exception as e:
            self.echo_error(hash_path, e)
        else:
            self.secho("[SUCCESS] {}".format(path), fg="green")

    def check_hash(self, patterns):
        for hash_path in self.scan(patterns):
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

    # Convert bool flags to io streams.
    no_stdout = options.pop("no_stdout", False)
    no_stderr = options.pop("no_stderr", False)
    stdout = open(os.devnull, "w") if no_stdout else sys.stdout
    stderr = open(os.devnull, "w") if no_stderr else sys.stderr
    # Initialize and invoke.
    GetHash(ctx, suffix, stdout=stdout, stderr=stderr, **options)(check, files)


def gethashcli(name):
    """Generate click decorators for the main function."""

    def decorator(func):
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
        @click.option(
            "-i", "--inplace", is_flag=True, help="Use basename in checksum files."
        )
        @click.option("--start", type=click.INT, help="The start offset of files.")
        @click.option("--stop", type=click.INT, help="The stop offset of files.")
        @click.option(
            "--glob",
            type=click.BOOL,
            default=True,
            show_default=True,
            help="Whether resolving glob patterns.",
        )
        @click.option(
            "--out",
            type=click.Choice(["sep", "agg", "null"]),
            default="sep",
            show_default=True,
            help="Specify the output mode.",
        )
        @click.option(
            "--agg",
            type=click.File("w", encoding="utf-8"),
            default=None,
            help="The aggregate output file. This option will set --out=agg.",
        )
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
