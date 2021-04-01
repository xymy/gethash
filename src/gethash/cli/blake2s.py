from gethash.script import gethashcli, script_main

META = dict(cmdname="blake2s", hashname="BLAKE2s", suffix=".blake2s")


@gethashcli(**META)
def main(files, **kwargs):
    """Generate or check BLAKE2s."""

    from hashlib import blake2s as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
