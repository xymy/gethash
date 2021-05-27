from gethash.script import gethashcli, script_main

META = {
    "cmdname": "sha512",
    "hashname": "SHA512",
    "suffix": ".sha512",
    "package": "hashlib",
    "hasher": "sha512",
}


@gethashcli(**META)
def main(files, **kwargs):
    """Generate or check SHA512."""

    from hashlib import sha512 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
