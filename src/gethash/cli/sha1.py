from gethash.script import gethashcli, script_main

META = dict(cmdname="sha1", hashname="SHA1", suffix=".sha1")


@gethashcli(**META)
def main(files, **kwargs):
    """Generate or check SHA1."""

    from hashlib import sha1 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
