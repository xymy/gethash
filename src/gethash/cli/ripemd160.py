from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {
    "cmdname": "ripemd160",
    "hashname": "RIPEMD160",
    "suffix": ".ripemd160",
    "package": "Cryptodome.Hash.RIPEMD160",
    "hasher": "new",
}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check RIPEMD160."""

    from Cryptodome.Hash.RIPEMD160 import new as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
