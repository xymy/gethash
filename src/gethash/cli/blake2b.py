from gethash.script import gethashcli, script_main

META = {
    "cmdname": "blake2b",
    "hashname": "BLAKE2b",
    "suffix": ".blake2b",
    "package": "hashlib",
    "hasher": "blake2b",
}


@gethashcli(**META)
def main(files, **kwargs):
    """Generate or check BLAKE2b."""

    from hashlib import blake2b as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
