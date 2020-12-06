from gethash.script import gethashcli, script_main

NAME = "BLAKE2s"
SUFFIX = ".blake2s"


@gethashcli(NAME, SUFFIX)
def main(files, **kwargs):
    """Generate and check BLAKE2s."""

    from hashlib import blake2s as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
