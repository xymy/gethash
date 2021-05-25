from pathlib import Path

META_LIST = [
    {
        "cmdname": "crc32",
        "hashname": "CRC32",
        "suffix": ".crc32",
        "package": "gethash.utils.crc32",
        "hasher": "CRC32",
    },
    {
        "cmdname": "md2",
        "hashname": "MD2",
        "suffix": ".md2",
        "package": "Cryptodome.Hash.MD2",
        "hasher": "new",
    },
    {
        "cmdname": "md4",
        "hashname": "MD4",
        "suffix": ".md4",
        "package": "Cryptodome.Hash.MD4",
        "hasher": "new",
    },
    {
        "cmdname": "md5",
        "hashname": "MD5",
        "suffix": ".md5",
        "package": "hashlib",
        "hasher": "md5",
    },
    {
        "cmdname": "ripemd160",
        "hashname": "RIPEMD160",
        "suffix": ".ripemd160",
        "package": "Cryptodome.Hash.RIPEMD160",
        "hasher": "new",
    },
    {
        "cmdname": "sha1",
        "hashname": "SHA1",
        "suffix": ".sha1",
        "package": "hashlib",
        "hasher": "sha1",
    },
    {
        "cmdname": "sha256",
        "hashname": "SHA256",
        "suffix": ".sha256",
        "package": "hashlib",
        "hasher": "sha256",
    },
    {
        "cmdname": "sha512",
        "hashname": "SHA512",
        "suffix": ".sha512",
        "package": "hashlib",
        "hasher": "sha512",
    },
    {
        "cmdname": "sha3-256",
        "hashname": "SHA3-256",
        "suffix": ".sha3_256",
        "package": "hashlib",
        "hasher": "sha3_256",
    },
    {
        "cmdname": "sha3-512",
        "hashname": "SHA3-512",
        "suffix": ".sha3_512",
        "package": "hashlib",
        "hasher": "sha3_512",
    },
    {
        "cmdname": "blake2b",
        "hashname": "BLAKE2b",
        "suffix": ".blake2b",
        "package": "hashlib",
        "hasher": "blake2b",
    },
    {
        "cmdname": "blake2s",
        "hashname": "BLAKE2s",
        "suffix": ".blake2s",
        "package": "hashlib",
        "hasher": "blake2s",
    },
]

TEMPLATE = """\
import sys

from gethash.script import gethashcli, script_main

META = {meta}


@gethashcli(**META)
def _main(files, **kwargs):
    \"""Generate or check {hashname}.\"""

    from {package} import {hasher} as H

    script_main(H(), files, **kwargs)


def main():
    # Since Click 8, glob patterns, user home directory and environment variables will
    # be expanded automatically on Windows, which causes unexpected behaviour. What's
    # more, there is no way to disable expansion through quotation marks on Windows
    # command line. So we suppress this feature by passing arguments explicitly.
    return _main(sys.argv[1:])


if __name__ == "__main__":
    main()
"""


def main():
    for meta in META_LIST:
        cmdname = meta["cmdname"]
        hashname = meta["hashname"]
        package = meta["package"]
        hasher = meta["hasher"]
        code = TEMPLATE.format(
            meta=str(meta), hashname=hashname, package=package, hasher=hasher
        )
        path = Path(__file__).with_stem(cmdname.replace("-", "_"))
        path.write_text(code)


if __name__ == "__main__":
    main()
