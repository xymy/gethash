from typing import Any, Tuple

from gethash.script import gethashcli, script_main

META = {"cmdname": "md2", "hashname": "MD2", "suffix": ".md2", "package": "Cryptodome.Hash.MD2", "hasher": "new"}


@gethashcli(**META)
def main(files: Tuple[str, ...], **kwargs: Any) -> None:
    """Generate or check MD2."""

    from Cryptodome.Hash.MD2 import new as H

    script_main(H(), files, **kwargs)


if __name__ == "__main__":
    main()
