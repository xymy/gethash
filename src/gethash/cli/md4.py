from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {"cmdname": "md4", "hashname": "MD4", "suffix": ".md4", "package": "Cryptodome.Hash.MD4", "hasher": "new"}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check MD4."""

    from Cryptodome.Hash.MD4 import new as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
