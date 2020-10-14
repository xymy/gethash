from gethash.script import gethashcli, script_main

NAME = "MD4"
SUFFIX = ".md4"


@gethashcli(NAME)
def main(check, files, **kwargs):
    try:
        from Crypto.Hash.MD4 import new as H
    except ImportError:
        import sys

        sys.stderr.write("PyCryptodome is not found.\n")
        sys.exit(-1)

    script_main(H(), SUFFIX, check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
