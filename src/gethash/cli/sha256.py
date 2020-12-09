from gethash.script import gethashcli, script_main

NAME = "SHA256"
SUFFIX = ".sha256"


@gethashcli(NAME, SUFFIX)
def main(files, **kwargs):
    """Generate or check SHA256."""

    from hashlib import sha256 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
