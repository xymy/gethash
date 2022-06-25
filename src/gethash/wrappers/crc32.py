import zlib
from typing import Optional, cast

from ..utils import _check_bytes, _check_bytes_opt, _check_int, _check_int_opt

__all__ = ["CRC32"]


class CRC32:
    """Hash functions API wrapper for CRC32.

    The context exposes the ``value`` attribute for the current CRC32 value.

    References:
        - PEP 247 -- API for Cryptographic Hash Functions
          https://www.python.org/dev/peps/pep-0247/
        - PEP 452 -- API for Cryptographic Hash Functions v2.0
          https://www.python.org/dev/peps/pep-0452/
    """

    name = "CRC32"
    digest_size = 4

    def __init__(self, data: Optional[bytes] = None, value: Optional[int] = None) -> None:
        data = _check_bytes_opt(data, "data", b"")
        value = _check_int_opt(value, "value", 0)
        self._value = zlib.crc32(cast(bytes, data), cast(int, value))

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        _check_int(value, "value")
        self._value = value & 0xFFFFFFFF

    def update(self, data: bytes) -> None:
        _check_bytes(data, "data")
        self._value = zlib.crc32(data, self._value)

    def digest(self) -> bytes:
        return self._value.to_bytes(4, "big")

    def hexdigest(self) -> str:
        return self._value.to_bytes(4, "big").hex()

    def copy(self) -> "CRC32":
        return type(self)(value=self._value)


def new() -> CRC32:
    return CRC32()
