import sys

from gethash.script import gethashcli, script_main

META = {
    "cmdname": "md5",
    "hashname": "MD5",
    "suffix": ".md5",
    "package": "hashlib",
    "hasher": "md5",
}


@gethashcli(**META)
def _main(files, **kwargs):
    """Generate or check MD5."""

    from hashlib import md5 as H

    script_main(H(), files, **kwargs)


def main():
    # Since Click 8, glob patterns, user home directory and environment variables will
    # be expanded automatically on Windows, which causes unexpected behaviour. What's
    # more, there is no way to disable expansion through quotation marks on Windows
    # command line. So we suppress this feature by passing arguments explicitly.
    return _main(sys.argv[1:])


if __name__ == "__main__":
    main()
