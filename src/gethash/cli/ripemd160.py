from gethash.script import gethashcli, script_main

NAME = "RIPEMD160"
SUFFIX = ".ripemd160"


@gethashcli(NAME, SUFFIX)
def main(files, **kwargs):
    """Generate or check RIPEMD160."""

    from Cryptodome.Hash.RIPEMD160 import new as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
