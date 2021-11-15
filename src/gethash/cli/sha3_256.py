from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {
    "cmdname": "sha3-256",
    "hashname": "SHA3-256",
    "suffix": ".sha3_256",
    "package": "hashlib",
    "hasher": "sha3_256",
}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check SHA3-256."""

    from hashlib import sha3_256 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
