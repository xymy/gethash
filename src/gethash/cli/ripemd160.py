from gethash.script import gethashcli, script_main

META = dict(cmdname="ripemd160", hashname="RIPEMD160", suffix=".ripemd160")


@gethashcli(**META)
def main(files, **kwargs):
    """Generate or check RIPEMD160."""

    from Cryptodome.Hash.RIPEMD160 import new as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
