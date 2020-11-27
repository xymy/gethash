from gethash.script import gethashcli, script_main

NAME = "SHA3-512"
SUFFIX = ".sha3_512"


@gethashcli(NAME)
def main(check, files, **kwargs):
    """Generate and check SHA3-512."""

    from hashlib import sha3_512 as H

    script_main(H(), SUFFIX, check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
