import glob
import hmac
import os
import re
import sys

import click

DEFAULT_CHUNK_SIZE = 0x100000


def fhash(hash_value, path):
    return '{} *{}\n'.format(hash_value.hex(), path)


def phash(hash_line):
    m = re.match(r'([0-9a-fA-F]+) \*(.+)', hash_line)
    if m is None:
        raise ValueError('unexpected hash line')
    hash_value, path = m.groups()
    return bytes.fromhex(hash_value), path


def gethash(ctx, path, *, chunk_size=DEFAULT_CHUNK_SIZE):
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            ctx.update(chunk)
        return ctx.digest()


def generate_hash(ctx, patterns, *, suffix='.sha'):
    for pattern in patterns:
        for path in map(os.path.normpath, glob.iglob(pattern)):
            hash_value = gethash(ctx.copy(), path)
            hash_line = fhash(hash_value, path)
            hash_path = os.path.splitext(path)[0] + suffix
            with open(hash_path, 'w', encoding='utf-8') as f:
                f.write(hash_line)

            click.echo(hash_line, nl=False)


def check_hash(ctx, patterns):
    for pattern in patterns:
        for hash_path in map(os.path.normpath, glob.iglob(pattern)):
            with open(hash_path, 'r', encoding='utf-8') as f:
                hash_line = f.read()
            hash_value, path = phash(hash_line)
            current_hash_value = gethash(ctx.copy(), path)

            if hmac.compare_digest(hash_value, current_hash_value):
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
