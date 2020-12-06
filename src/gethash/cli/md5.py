from gethash.script import gethashcli, script_main

NAME = "MD5"
SUFFIX = ".md5"


@gethashcli(NAME, SUFFIX)
def main(files, **kwargs):
    """Generate and check MD5."""

    from hashlib import md5 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
