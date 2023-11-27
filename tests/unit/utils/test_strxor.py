from __future__ import annotations

import pytest

from gethash.utils.strxor import _py_strxor, strxor


@pytest.mark.parametrize(
    ("term1", "term2", "expected"),
    [
        (
            bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"),
            bytes.fromhex("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"),
            bytes.fromhex("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"),
        ),
        (
            bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"),
            bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"),
            bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000"),
        ),
        (
            bytes.fromhex("54974d6a31b907910fb6bf679825ed5d678b7d65d4ae15c8b2a024723299ac80"),
            bytes.fromhex("8696ac14f1f1e6a7219326a6b3b2c10a47464185a6d30f224caa800d5e69dd8e"),
            bytes.fromhex("d201e17ec048e1362e2599c12b972c5720cd3ce0727d1aeafe0aa47f6cf0710e"),
        ),
    ],
)
class TestStrxor:
    def test__py_strxor(self, term1: bytes, term2: bytes, expected: bytes) -> None:
        result = _py_strxor(term1, term2)
        assert result == expected

        output = bytearray(len(expected))
        _py_strxor(term1, term2, output)
        assert output == expected

    def test_strxor(self, term1: bytes, term2: bytes, expected: bytes) -> None:
        result = strxor(term1, term2)
        assert result == expected

        output = bytearray(len(expected))
        strxor(term1, term2, output)
        assert output == expected

    def test_strxor__error(self, term1: bytes, term2: bytes, expected: bytes) -> None:
        with pytest.raises(ValueError, match="term1 and term2 must have the same length"):
            strxor(term1, term2[1:])

        output = bytearray(len(expected) - 1)
        with pytest.raises(ValueError, match="output must have the same length as the input"):
            strxor(term1, term2, output)
