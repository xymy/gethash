from gethash.script import gethashcli, script_main

NAME = "SHA1"
SUFFIX = ".sha1"


@gethashcli(NAME, SUFFIX)
def main(check, files, **kwargs):
    """Generate and check SHA1."""

    from hashlib import sha1 as H

    script_main(H(), check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
