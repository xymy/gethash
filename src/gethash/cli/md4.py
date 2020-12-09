from gethash.script import gethashcli, script_main

NAME = "MD4"
SUFFIX = ".md4"


@gethashcli(NAME, SUFFIX)
def main(files, **kwargs):
    """Generate or check MD4."""

    from Cryptodome.Hash.MD4 import new as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
