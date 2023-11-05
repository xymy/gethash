from __future__ import annotations

import zlib

from typing_extensions import Self


class CRC32:
    """Hash functions API wrapper for CRC32.

    The context exposes the ``value`` attribute for the current CRC32 value.

    References:
        - PEP 247 -- API for Cryptographic Hash Functions
          https://peps.python.org/pep-0247/
        - PEP 452 -- API for Cryptographic Hash Functions v2.0
          https://peps.python.org/pep-0452/
    """

    name = "CRC32"

    digest_size = 4

    def __init__(self, data: bytes = b"", value: int = 0) -> None:
        self._value = zlib.crc32(data, value)

    def copy(self) -> Self:
        return type(self)(value=self._value)

    def digest(self) -> bytes:
        return self._value.to_bytes(4, "big")

    def hexdigest(self) -> str:
        return self._value.to_bytes(4, "big").hex()

    def update(self, data: bytes) -> None:
        self._value = zlib.crc32(data, self._value)


def new() -> CRC32:
    return CRC32()
