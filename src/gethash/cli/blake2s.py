from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {"cmdname": "blake2s", "hashname": "BLAKE2s", "suffix": ".blake2s", "package": "hashlib", "hasher": "blake2s"}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check BLAKE2s."""

    from hashlib import blake2s as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
