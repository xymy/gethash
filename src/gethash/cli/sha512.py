from gethash.script import gethashcli, script_main

NAME = "SHA512"
SUFFIX = ".sha512"


@gethashcli(NAME)
def main(check, files, **kwargs):
    """Generate and check SHA512."""

    from hashlib import sha512 as H

    script_main(H(), SUFFIX, check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
