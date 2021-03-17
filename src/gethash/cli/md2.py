from gethash.script import gethashcli, script_main

META = dict(cmdname="md2", hashname="MD2", suffix=".md2")


@gethashcli(**META)
def main(files, **kwargs):
    """Generate or check MD2."""

    from Cryptodome.Hash.MD2 import new as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
