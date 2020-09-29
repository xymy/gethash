import os
import sys
from functools import partial, wraps
from glob import iglob

import click

from . import __version__
from ._core import CheckHashLineError, Hasher, check_hash_line, generate_hash_line


class GetHash(object):
    """Provide script interfaces."""

    def __init__(self, ctx, suffix=".sha", **kwargs):
        self.ctx = ctx
        self.suffix = suffix

        self.inplace = kwargs.pop("inplace", False)
        self.no_file = kwargs.pop("no_file", False)
        self.no_glob = kwargs.pop("no_glob", False)
        self.stdout = kwargs.pop("stdout", sys.stdout)
        self.stderr = kwargs.pop("stderr", sys.stderr)

        # Prepare arguments and construct the hash function.
        dir_ok = kwargs.pop("dir", False)
        start = kwargs.pop("start", None)
        stop = kwargs.pop("stop", None)
        tqdm_args = {
            "file": self.stderr,
            "leave": kwargs.pop("tqdm-leave", False),
            "ascii": kwargs.pop("tqdm-ascii", True),
        }
        hasher = Hasher(ctx, tqdm_args=tqdm_args)
        self.hash_function = partial(
            hasher.calc_hash, start=start, stop=stop, dir_ok=dir_ok
        )

    def echo(self, msg, **kwargs):
        click.echo(msg, file=self.stdout, **kwargs)

    def secho(self, msg, **kwargs):
        click.secho(msg, file=self.stdout, **kwargs)

    def echo_error(self, path, exc):
        message = "[ERROR] {}\n\t{}: {}".format(path, type(exc).__name__, exc)
        click.secho(message, file=self.stderr, fg="red")

    def glob(self, patterns):
        if self.no_glob:

            def glob_func(pattern):
                yield pattern

        else:
            glob_func = iglob

        for pattern in patterns:
            for path in map(os.path.normpath, glob_func(pattern)):
                yield path

    def generate_hash(self, patterns):
        for path in self.glob(patterns):
            try:
                hash_line = generate_hash_line(
                    self.hash_function, path, inplace=self.inplace
                )
                hash_path = path + self.suffix
                if not self.no_file:
                    with open(hash_path, "w", encoding="utf-8") as f:
                        f.write(hash_line)
            except Exception as e:
                self.echo_error(path, e)
            else:
                # The hash line already has a newline.
                self.echo(hash_line, nl=False)

    def _check_hash(self, hash_line, hash_path):
        try:
            path = check_hash_line(self.hash_function, hash_line, inplace=hash_path)
        except CheckHashLineError as e:
            self.secho("[FAILURE] {}".format(e.path), fg="red")
        except Exception as e:
            self.echo_error(hash_path, e)
        else:
            self.secho("[SUCCESS] {}".format(path), fg="green")

    def check_hash(self, patterns):
        for hash_path in self.glob(patterns):
            try:
                with open(hash_path, "r", encoding="utf-8") as f:
                    # This function can process multiple hash lines.
                    for hash_line in f:
                        if hash_line.isspace():
                            continue
                        self._check_hash(hash_line, hash_path)
            except Exception as e:
                self.echo_error(hash_path, e)


def script_main(ctx, suffix, check, files, **options):
    """Generate the main body of the main function."""
    no_stdout = options.pop("no_stdout", False)
    no_stderr = options.pop("no_stderr", False)
    stdout = open(os.devnull, "w") if no_stdout else sys.stdout
    stderr = open(os.devnull, "w") if no_stderr else sys.stderr
    gh = GetHash(ctx, suffix, stdout=stdout, stderr=stderr, **options)

    if check:
        gh.check_hash(files)
    else:
        gh.generate_hash(files)


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
            "-l", "--start", type=click.INT, help="The start offset of file(s)."
        )
        @click.option(
            "-r", "--stop", type=click.INT, help="The stop offset of file(s)."
        )
        @click.option(
            "-d", "--dir", is_flag=True, help="Allow checksum for directories."
        )
        @click.option(
            "-i", "--inplace", is_flag=True, help="Use basename in checksum files."
        )
        @click.option("--no-file", is_flag=True, help="Do not output checksum files.")
        @click.option("--no-glob", is_flag=True, help="Do not resolve glob patterns.")
        @click.option("--no-stdout", is_flag=True, help="Do not output to stdout.")
        @click.option("--no-stderr", is_flag=True, help="Do not output to stderr.")
        @click.option('--tqdm-leave', type=click.BOOL, default=False, show_default=True)
        @click.option('--tqdm-ascii', type=click.BOOL, default=True, show_default=True)
        @click.version_option(__version__)
        @click.argument("files", nargs=-1)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
