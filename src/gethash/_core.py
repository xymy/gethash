import glob
import hmac
import os
import re

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


def generate_hash(ctx, patterns):
    for pattern in patterns:
        for path in map(os.path.normpath, glob.iglob(pattern)):
            hash_value = gethash(ctx.copy(), path)
            hash_line = fhash(hash_value, path)
            hash_path = os.path.splitext(path)[0] + '.' + ctx.name
            with open(hash_path, 'w', encoding='utf-8') as f:
                f.write(hash_line)


def check_hash(ctx, patterns):
    for pattern in patterns:
        for hash_path in map(os.path.normpath, glob.iglob(pattern)):
            with open(hash_path, 'r', encoding='utf-8') as f:
                hash_line = f.read()
            hash_value, path = phash(hash_line)
            current_hash_value = gethash(ctx.copy(), path)
            if hmac.compare_digest(hash_value, current_hash_value):
                print('[SUCCESS] {}'.format(path))
            else:
                print('[FAILURE] {}'.format(path))


def script_main(ctx, check, files):
    if check:
        check_hash(ctx, files)
    else:
        generate_hash(ctx, files)
