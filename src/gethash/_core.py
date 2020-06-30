import os
import re
import sys
from glob import iglob
from hmac import compare_digest
from os import PathLike
from typing import ByteString, Tuple

import click
from tqdm import tqdm

_CHUNK_SIZE = 0x100000


def calculate_hash(
    ctx,
    path: PathLike,
    *,
    chunk_size=_CHUNK_SIZE,
    **tqdm_args
) -> bytes:
    """Calculate the hash value of `path` using given hash context `ctx`.

    A tqdm progressbar is also available.
    """
    file_size = os.path.getsize(path)
    leave = tqdm_args.pop('leave', False)
    ascii = tqdm_args.pop('ascii', True)
    bar = tqdm(total=file_size, leave=leave, ascii=ascii, **tqdm_args)
    with bar as bar, open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            ctx.update(chunk)
            bar.update(len(chunk))
        return ctx.digest()


def fhash(hash_value: ByteString, path: PathLike) -> str:
    """Format `hash_value` and `path` to `hash_line`."""
    return '{} *{}\n'.format(hash_value.hex(), path)


def phash(hash_line: str) -> Tuple[bytes, str]:
    """Parse `hash_line` to `hash_value` and `path`."""
    m = re.match(r'([0-9a-fA-F]+) \*(.+)', hash_line)
    if m is None:
        raise ValueError('unexpected hash line')
    hash_value, path = m.groups()
    return bytes.fromhex(hash_value), path


class MissingFile(FileNotFoundError):
    """For the filename listed in checksum file but the file not exists."""


def _echo_error(path, exc):
    message = '[ERROR] {}\n\t{}: {}'.format(path, type(exc).__name__, exc)
    click.secho(message, err=True, fg='red')


class GetHash(object):
    def __init__(self, ctx, *, file=sys.stdout, suffix='.sha', **kwargs):
        self.ctx = ctx
        self.file = file
        self.suffix = suffix
        self.tqdm_args = {'file': file, **kwargs}

    def generate_hash_line(self, path):
        ctx = self.ctx.copy()
        hash_value = calculate_hash(ctx, path, **self.tqdm_args)
        return fhash(hash_value, path)

    def check_hash_line(self, hash_line):
        hash_value, path = phash(hash_line)

        # If we cannot find the file listed in hash line, raise `MissingFile`.
        try:
            ctx = self.ctx.copy()
            current_hash_value = calculate_hash(ctx, path, **self.tqdm_args)
        except FileNotFoundError:
            raise MissingFile(path)

        is_ok = compare_digest(hash_value, current_hash_value)
        return is_ok, path


def generate_hash_line(ctx, path, **tqdm_args):
    hash_value = calculate_hash(ctx.copy(), path, **tqdm_args)
    return fhash(hash_value, path)


def generate_hash(ctx, patterns, *, file=sys.stdout, suffix='.sha'):
    for pattern in patterns:
        for path in map(os.path.normpath, iglob(pattern)):
            try:
                hash_line = generate_hash_line(ctx, path, file=file)
                hash_path = path + suffix
                with open(hash_path, 'w', encoding='utf-8') as f:
                    f.write(hash_line)
            except Exception as e:
                _echo_error(path, e)
            else:
                click.echo(hash_line, file=file, nl=False)


def check_hash_line(ctx, hash_line, **tqdm_args):
    hash_value, path = phash(hash_line)

    # If we cannot find the file listed in hash line, raise `MissingFile`.
    try:
        current_hash_value = calculate_hash(ctx.copy(), path, **tqdm_args)
    except FileNotFoundError:
        raise MissingFile(path)

    is_ok = compare_digest(hash_value, current_hash_value)
    return is_ok, path


def _check_hash(ctx, hash_line, hash_path, *, file=sys.stdout):
    try:
        is_ok, path = check_hash_line(ctx, hash_line, file=file)
    except Exception as e:
        _echo_error(hash_path, e)
    else:
        if is_ok:
            click.secho('[SUCCESS] {}'.format(path), file=file, fg='green')
        else:
            click.secho('[FAILURE] {}'.format(path), file=file, fg='red')


def check_hash(ctx, patterns, *, file=sys.stdout):
    for pattern in patterns:
        for hash_path in map(os.path.normpath, iglob(pattern)):
            try:
                with open(hash_path, 'r', encoding='utf-8') as f:
                    for hash_line in f:
                        if hash_line.isspace():
                            continue
                        _check_hash(ctx, hash_line, hash_path, file=file)
            except Exception as e:
                _echo_error(hash_path, e)


def script_main(command, ctx, suffix, check, files, **kwargs):
    # When no argument, print help.
    if not files:
        sys.argv.append('--help')
        command()

    no_stdout = kwargs.pop('no_stdout', False)
    file = open(os.devnull, 'w') if no_stdout else sys.stdout

    if check:
        check_hash(ctx, files, file=file)
    else:
        generate_hash(ctx, files, file=file, suffix=suffix)
