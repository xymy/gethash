from gethash.script import gethashcli, script_main

NAME = "SHA1"
SUFFIX = ".sha1"


@gethashcli(NAME, SUFFIX)
def main(files, **kwargs):
    """Generate or check SHA1."""

    from hashlib import sha1 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
