import os
import re
import sys
from glob import iglob
from hmac import compare_digest
from os import PathLike
from typing import ByteString, Tuple

import click
from tqdm import tqdm

DEFAULT_CHUNK_SIZE = 0x100000


class MissingFile(FileNotFoundError):
    """For the filename listed in checksum file but the file not exists."""


def _echo_error(path, exc):
    message = '[ERROR] {}\n\t{}: {}'.format(path, type(exc).__name__, exc)
    click.secho(message, err=True, fg='red')


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


def calculate_hash(
    ctx,
    path: PathLike,
    *,
    chunk_size=DEFAULT_CHUNK_SIZE,
    file=None,
    disable=False
) -> bytes:
    """Calculate the hash value of `path` using given hash context `ctx`.

    A progressbar is available when `file` is a tty and `disable` is `False`.
    """
    file_size = os.path.getsize(path)
    bar = tqdm(total=file_size, leave=False,
               file=file, ascii=True, disable=disable)
    with bar as bar, open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            ctx.update(chunk)
            bar.update(len(chunk))
        return ctx.digest()


def _generate_hash_line(ctx, path):
    hash_value = calculate_hash(ctx.copy(), path)
    return fhash(hash_value, path)


def generate_hash(ctx, patterns, *, suffix='.sha'):
    for pattern in patterns:
        for path in map(os.path.normpath, iglob(pattern)):
            try:
                hash_line = _generate_hash_line(ctx, path)
                hash_path = path + suffix
                with open(hash_path, 'w', encoding='utf-8') as f:
                    f.write(hash_line)
            except Exception as e:
                _echo_error(path, e)
            else:
                click.echo(hash_line, nl=False)


def _check_hash_line(ctx, hash_line):
    hash_value, path = phash(hash_line)

    # If we cannot find the file listed in hash line, raise `MissingFile`.
    try:
        current_hash_value = calculate_hash(ctx.copy(), path)
    except FileNotFoundError:
        raise MissingFile(path)

    is_ok = compare_digest(hash_value, current_hash_value)
    return is_ok, path


def _check_hash(ctx, hash_line, hash_path):
    try:
        is_ok, path = _check_hash_line(ctx, hash_line)
    except Exception as e:
        _echo_error(hash_path, e)
    else:
        if is_ok:
            click.secho('[SUCCESS] {}'.format(path), fg='green')
        else:
            click.secho('[FAILURE] {}'.format(path), fg='red')


def check_hash(ctx, patterns):
    for pattern in patterns:
        for hash_path in map(os.path.normpath, iglob(pattern)):
            try:
                with open(hash_path, 'r', encoding='utf-8') as f:
                    for hash_line in f:
                        if hash_line.isspace():
                            continue
                        _check_hash(ctx, hash_line, hash_path)
            except Exception as e:
                _echo_error(hash_path, e)


def script_main(command, ctx, suffix, check, files, **kwargs):
    # When no argument, print help.
    if not files:
        sys.argv.append('--help')
        command()

    if check:
        check_hash(ctx, files)
    else:
        generate_hash(ctx, files, suffix=suffix)
