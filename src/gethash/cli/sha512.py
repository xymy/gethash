# This file is automatically generated. Do not edit it.
from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {"command_name": "sha512", "display_name": "SHA512", "package": "hashlib", "hasher": "sha512"}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check SHA512."""

    from hashlib import sha512 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
