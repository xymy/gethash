from __future__ import annotations

from typing import cast

__all__ = [
    "_check_int",
    "_check_int_opt",
    "_check_float",
    "_check_float_opt",
    "_check_str",
    "_check_str_opt",
    "_check_bytes",
    "_check_bytes_opt",
    "_check_bytes_w",
    "_check_bytes_w_opt",
    "_is_writable_memoryview",
]


def _check_int(obj: object, name: str) -> None:
    if not isinstance(obj, int):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be int, not {tn}")


def _check_int_opt(obj: object, name: str, default: int | None = None) -> int | None:
    if obj is None:
        return default

    if not isinstance(obj, int):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be int or None, not {tn}")
    return obj


def _check_float(obj: object, name: str) -> None:
    if not isinstance(obj, float):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be float, not {tn}")


def _check_float_opt(obj: object, name: str, default: float | None = None) -> float | None:
    if obj is None:
        return default

    if not isinstance(obj, float):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be float or None, not {tn}")
    return obj


def _check_str(obj: object, name: str) -> None:
    if not isinstance(obj, str):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be str, not {tn}")


def _check_str_opt(obj: object, name: str, default: str | None = None) -> str | None:
    if obj is None:
        return default

    if not isinstance(obj, str):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be str or None, not {tn}")
    return obj


def _check_bytes(obj: object, name: str) -> None:
    if not isinstance(obj, (bytes, bytearray, memoryview)):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be bytes-like, not {tn}")


def _check_bytes_opt(obj: object, name: str, default: bytes | None = None) -> bytes | None:
    if obj is None:
        return default

    if not isinstance(obj, (bytes, bytearray, memoryview)):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be bytes-like or None, not {tn}")
    return obj


def _check_bytes_w(obj: object, name: str) -> None:
    if not (isinstance(obj, bytearray) or _is_writable_memoryview(obj)):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be writable bytes-like, not {tn}")


def _check_bytes_w_opt(obj: object, name: str, default: bytearray | None = None) -> bytearray | None:
    if obj is None:
        return default

    if not (isinstance(obj, bytearray) or _is_writable_memoryview(obj)):
        tn = type(obj).__name__
        raise TypeError(f"{name} must be writable bytes-like or None, not {tn}")
    return cast(bytearray, obj)


def _is_writable_memoryview(obj: object) -> bool:
    return isinstance(obj, memoryview) and not obj.readonly
