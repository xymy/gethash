import os
import sys
from glob import iglob

import click

from . import __version__
from ._core import CheckHashLineError, chl, ghl


class GetHash(object):
    """Provide script interfaces."""

    def __init__(self, ctx, *, suffix='.sha', **kwargs):
        self.ctx = ctx
        self.suffix = suffix
        self.file = kwargs.pop('file', sys.stdout)
        self.errfile = kwargs.pop('errfile', sys.stderr)
        self.no_glob = kwargs.pop('no_glob', False)
        self.tqdm_args = {'file': self.file, **kwargs}

    def echo(self, msg, **kwargs):
        click.echo(msg, file=self.file, **kwargs)

    def secho(self, msg, **kwargs):
        click.secho(msg, file=self.file, **kwargs)

    def echo_error(self, path, exc):
        message = '[ERROR] {}\n\t{}: {}'.format(path, type(exc).__name__, exc)
        click.secho(message, file=self.errfile, fg='red')

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
                hash_line = ghl(self.ctx, path, **self.tqdm_args)
                hash_path = path + self.suffix
                with open(hash_path, 'w', encoding='utf-8') as f:
                    f.write(hash_line)
            except Exception as e:
                self.echo_error(path, e)
            else:
                self.echo(hash_line, nl=False)

    def _check_hash(self, hash_line, hash_path):
        try:
            path = chl(self.ctx, hash_line, **self.tqdm_args)
        except CheckHashLineError as e:
            self.secho('[FAILURE] {}'.format(e.path), fg='red')
        except Exception as e:
            self.echo_error(hash_path, e)
        else:
            self.secho('[SUCCESS] {}'.format(path), fg='green')

    def check_hash(self, patterns):
        for hash_path in self.glob(patterns):
            try:
                with open(hash_path, 'r', encoding='utf-8') as f:
                    for hash_line in f:
                        if hash_line.isspace():
                            continue
                        self._check_hash(hash_line, hash_path)
            except Exception as e:
                self.echo_error(hash_path, e)


def script_main(command, ctx, suffix, check, files, **options):
    # When no argument, print help.
    if not files:
        sys.argv.append('--help')
        command()

    # Resolve command-line options.

    no_stdout = options.pop('no_stdout', False)
    file = open(os.devnull, 'w') if no_stdout else sys.stdout

    no_stderr = options.pop('no_stderr', False)
    errfile = open(os.devnull, 'w') if no_stderr else sys.stderr

    no_glob = options.pop('no_glob', False)

    args = {'file': file, 'errfile': errfile, 'no_glob': no_glob}
    gh = GetHash(ctx, suffix=suffix, **args)

    if check:
        gh.check_hash(files)
    else:
        gh.generate_hash(files)


def gethashcli(name):
    def decorator(func):
        @click.command()
        @click.option('-c', '--check', is_flag=True,
                      help='Read {} from FILES and check them.'.format(name))
        @click.option('--no-stdout', is_flag=True,
                      help='Do not output to stdout.')
        @click.option('--no-stderr', is_flag=True,
                      help='Do not output to stderr.')
        @click.option('--no-glob', is_flag=True,
                      help='Do not resolve glob patterns.')
        @click.version_option(__version__)
        @click.argument('files', nargs=-1)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator
