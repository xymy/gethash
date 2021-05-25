import sys

from gethash.script import gethashcli, script_main

META = {
    "cmdname": "md4",
    "hashname": "MD4",
    "suffix": ".md4",
    "package": "Cryptodome.Hash.MD4",
    "hasher": "new",
}


@gethashcli(**META)
def _main(files, **kwargs):
    """Generate or check MD4."""

    from Cryptodome.Hash.MD4 import new as H

    script_main(H(), files, **kwargs)


def main():
    # Since Click 8, glob patterns, user home directory and environment variables will
    # be expanded automatically on Windows, which causes unexpected behaviour. What's
    # more, there is no way to disable expansion through quotation marks on command
    # line. So we suppress this feature by passing arguments explicitly.
    return _main(sys.argv[1:])


if __name__ == "__main__":
    main()
