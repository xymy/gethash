from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {"cmdname": "sha256", "hashname": "SHA256", "suffix": ".sha256", "package": "hashlib", "hasher": "sha256"}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check SHA256."""

    from hashlib import sha256 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
