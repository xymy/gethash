from gethash.script import gethashcli, script_main

NAME = "BLAKE2b"
SUFFIX = ".blake2b"


@gethashcli(NAME, SUFFIX)
def main(files, **kwargs):
    """Generate and check BLAKE2b."""

    from hashlib import blake2b as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
