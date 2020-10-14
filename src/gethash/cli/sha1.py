from gethash.script import gethashcli, script_main

NAME = "SHA1"
SUFFIX = ".sha1"


@gethashcli(NAME)
def main(check, files, **kwargs):
    from hashlib import sha1 as H

    script_main(H(), SUFFIX, check, files, **kwargs)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
