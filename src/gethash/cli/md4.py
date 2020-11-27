from gethash.script import gethashcli, script_main

NAME = "MD4"
SUFFIX = ".md4"


@gethashcli(NAME, SUFFIX)
def main(check, files, **kwargs):
    """Generate and check MD4."""

    from Cryptodome.Hash.MD4 import new as H

    script_main(H(), check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
