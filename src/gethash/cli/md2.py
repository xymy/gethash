from gethash.script import gethashcli, script_main

NAME = "MD2"
SUFFIX = ".md2"


@gethashcli(NAME, SUFFIX)
def main(check, files, **kwargs):
    """Generate and check MD2."""

    from Cryptodome.Hash.MD2 import new as H

    script_main(H(), check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
