import sys

from gethash.script import gethashcli, script_main

META = {
    "cmdname": "blake2s",
    "hashname": "BLAKE2s",
    "suffix": ".blake2s",
    "package": "hashlib",
    "hasher": "blake2s",
}


@gethashcli(**META)
def _main(files, **kwargs):
    """Generate or check BLAKE2s."""

    from hashlib import blake2s as H

    script_main(H(), files, **kwargs)


def main():
    # Since Click 8, glob patterns, user home directory and environment variables will
    # be expanded automatically on Windows, which causes unexpected behaviour. What's
    # more, there is no way to disable expansion through quotation marks on command
    # line. So we suppress this feature by passing arguments explicitly.
    return _main(sys.argv[1:])


if __name__ == "__main__":
    main()
