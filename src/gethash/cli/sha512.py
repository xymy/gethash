from gethash.script import gethashcli, script_main

NAME = "SHA512"
SUFFIX = ".sha512"


@gethashcli(NAME, SUFFIX)
def main(files, **kwargs):
    """Generate or check SHA512."""

    from hashlib import sha512 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
