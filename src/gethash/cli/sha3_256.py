from gethash.script import gethashcli, script_main

NAME = "SHA3-256"
SUFFIX = ".sha3_256"


@gethashcli(NAME, SUFFIX)
def main(check, files, **kwargs):
    """Generate and check SHA3-256."""

    from hashlib import sha3_256 as H

    script_main(H(), check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
