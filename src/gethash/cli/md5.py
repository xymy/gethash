from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {"cmdname": "md5", "hashname": "MD5", "suffix": ".md5", "package": "hashlib", "hasher": "md5"}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check MD5."""

    from hashlib import md5 as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
