from gethash.script import gethashcli, script_main

META = {"cmdname": "md4", "hashname": "MD4", "suffix": ".md4"}


@gethashcli(**META)
def main(files, **kwargs):
    """Generate or check MD4."""

    from Cryptodome.Hash.MD4 import new as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
