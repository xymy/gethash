import sys

from gethash.script import gethashcli, script_main

META = {
    "cmdname": "crc32",
    "hashname": "CRC32",
    "suffix": ".crc32",
    "package": "gethash.utils.crc32",
    "hasher": "CRC32",
}


@gethashcli(**META)
def _main(files, **kwargs):
    """Generate or check CRC32."""

    from gethash.utils.crc32 import CRC32 as H

    script_main(H(), files, **kwargs)


def main():
    # Since Click 8, glob patterns, user home directory and environment variables will
    # be expanded automatically on Windows, which causes unexpected behaviour. What's
    # more, there is no way to disable expansion through quotation marks on Windows
    # command line. So we suppress this feature by passing arguments explicitly.
    return _main(sys.argv[1:])


if __name__ == "__main__":
    main()
