from gethash.script import gethashcli, script_main

NAME = "BLAKE2b"
SUFFIX = ".blake2b"


@gethashcli(NAME)
def main(check, files, **kwargs):
    """Generate and check BLAKE2b."""

    from hashlib import blake2b as H

    script_main(H(), SUFFIX, check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
