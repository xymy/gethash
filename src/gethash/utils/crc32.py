import zlib

from . import _check_bytes, _check_bytes_opt, _check_int, _check_int_opt


class CRC32(object):
    """Hash functions API wrapper for CRC32."""

    name = "CRC32"
    digest_size = 4

    def __init__(self, data=None, value=None):
        data = _check_bytes_opt(data, "data", b"")
        value = _check_int_opt(value, "value", 0)
        self._value = zlib.crc32(data, value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        _check_int(value, "value")
        self._value = value

    def update(self, data):
        _check_bytes(data, "data")
        self._value = zlib.crc32(data, self._value)

    def digest(self):
        return self._value.to_bytes(4, "big")

    def hexdigest(self):
        return self._value.to_bytes(4, "big").hex()

    def copy(self):
        return type(self)(value=self._value)
