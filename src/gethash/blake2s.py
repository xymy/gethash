from ._script import gethashcli, script_main

NAME = "BLAKE2s"
SUFFIX = ".blake2s"


@gethashcli(NAME)
def main(check, files, **kwargs):
    from hashlib import blake2s as H

    script_main(H(), SUFFIX, check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
