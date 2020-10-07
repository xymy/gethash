from ._script import gethashcli, script_main

NAME = "MD2"
SUFFIX = ".md2"


@gethashcli(NAME)
def main(check, files, **kwargs):
    try:
        from Crypto.Hash import MD2 as H
    except ImportError:
        import sys

        sys.stderr.write("PyCryptodome is not found.\n")
        sys.exit(-1)

    script_main(H.new(), SUFFIX, check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
