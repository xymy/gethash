from gethash.script import gethashcli, script_main

META = dict(cmdname="sha256", hashname="SHA256", suffix=".sha256")


@gethashcli(**META)
def main(files, **kwargs):
    """Generate or check SHA256."""

    from hashlib import sha256 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
