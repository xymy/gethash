import zlib

from . import _check_bytes, _check_bytes_opt, _check_int_opt


class CRC32(object):
    def __init__(self, data=None, value=None):
        data = _check_bytes_opt(data, "data", b"")
        value = _check_int_opt(value, "value", 0)
        self.value = zlib.crc32(data, value)

    def update(self, data):
        _check_bytes(data, "data")
        self.value = zlib.crc32(data, self.value)

    def digest(self):
        return self.value.to_bytes(4, "big")

    def hexdigest(self):
        return self.value.to_bytes(4, "big").hex()

    def copy(self):
        return type(self)(value=self.value)
