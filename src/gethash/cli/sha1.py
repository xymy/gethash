# This file is automatically generated. Do not edit it.
from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {"command_name": "sha1", "display_name": "SHA1", "package": "hashlib", "hasher": "sha1"}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check SHA1."""

    from hashlib import sha1 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
