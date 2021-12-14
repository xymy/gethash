# This file is automatically generated. Do not edit it.
from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {"command_name": "blake2b", "display_name": "BLAKE2b", "package": "hashlib", "hasher": "blake2b"}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check BLAKE2b."""

    from hashlib import blake2b as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
