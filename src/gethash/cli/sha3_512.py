import sys

from gethash.script import gethashcli, script_main

META = {
    "cmdname": "sha3-512",
    "hashname": "SHA3-512",
    "suffix": ".sha3_512",
    "package": "hashlib",
    "hasher": "sha3_512",
}


@gethashcli(**META)
def _main(files, **kwargs):
    """Generate or check SHA3-512."""

    from hashlib import sha3_512 as H

    script_main(H(), files, **kwargs)


def main():
    # Since Click 8, glob patterns, user home directory and environment variables will
    # be expanded automatically on Windows, which causes unexpected behaviour. What's
    # more, there is no way to disable expansion through quotation marks on Windows
    # command line. So we suppress this feature by passing arguments explicitly.
    return _main(sys.argv[1:])


if __name__ == "__main__":
    main()
