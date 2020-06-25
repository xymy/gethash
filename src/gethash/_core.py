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


def fhash(hash_value: ByteString, path: PathLike) -> str:
    """Format hash_value and path to hash_line."""
    return '{} *{}\n'.format(hash_value.hex(), path)


def phash(hash_line: str) -> Tuple[bytes, str]:
    """Parse hash_line to hash_value and path."""
    m = re.match(r'([0-9a-fA-F]+) \*(.+)', hash_line)
    if m is None:
        raise ValueError('unexpected hash line')
    hash_value, path = m.groups()
    return bytes.fromhex(hash_value), path


def gethash(ctx, path, *, chunk_size=DEFAULT_CHUNK_SIZE):
    file_size = os.path.getsize(path)
    bar = tqdm(total=file_size, leave=False, ascii=True)
    with bar as bar, open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            ctx.update(chunk)
            bar.update(len(chunk))
        return ctx.digest()


def generate_hash(ctx, patterns, *, suffix='.sha'):
    for pattern in patterns:
        for path in map(os.path.normpath, iglob(pattern)):
            hash_value = gethash(ctx.copy(), path)
            hash_line = fhash(hash_value, path)
            hash_path = path + suffix
            with open(hash_path, 'w', encoding='utf-8') as f:
                f.write(hash_line)

            click.echo(hash_line, nl=False)


def check_hash(ctx, patterns):
    for pattern in patterns:
        for hash_path in map(os.path.normpath, iglob(pattern)):
            with open(hash_path, 'r', encoding='utf-8') as f:
                hash_line = f.read()
            hash_value, path = phash(hash_line)
            current_hash_value = gethash(ctx.copy(), path)

            if compare_digest(hash_value, current_hash_value):
                click.secho('[SUCCESS] {}'.format(path), fg='green')
            else:
                click.secho('[FAILURE] {}'.format(path), fg='red')


def script_main(command, ctx, suffix, check, files):
    # When no argument, print help.
    if not files:
        sys.argv.append('--help')
        command()

    if check:
        check_hash(ctx, files)
    else:
        generate_hash(ctx, files, suffix=suffix)
