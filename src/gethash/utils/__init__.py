from typing import Any

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
]


def _check_int(obj: object, name: str) -> None:
    if not isinstance(obj, int):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be int, not {tname}")


def _check_int_opt(obj: object, name: str, default: object = None) -> Any:
    if obj is None:
        return default

    if not isinstance(obj, int):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be int or None, not {tname}")
    return obj


def _check_float(obj: object, name: str) -> None:
    if not isinstance(obj, float):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be float, not {tname}")


def _check_float_opt(obj: object, name: str, default: object = None) -> Any:
    if obj is None:
        return default

    if not isinstance(obj, float):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be float or None, not {tname}")
    return obj


def _check_str(obj: object, name: str) -> None:
    if not isinstance(obj, str):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be str, not {tname}")


def _check_str_opt(obj: object, name: str, default: object = None) -> Any:
    if obj is None:
        return default

    if not isinstance(obj, str):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be str or None, not {tname}")
    return obj


def _check_bytes(obj: object, name: str) -> None:
    if not isinstance(obj, (bytes, bytearray, memoryview)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be bytes-like, not {tname}")


def _check_bytes_opt(obj: object, name: str, default: object = None) -> Any:
    if obj is None:
        return default

    if not isinstance(obj, (bytes, bytearray, memoryview)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be bytes-like or None, not {tname}")
    return obj


def _check_bytes_w(obj: object, name: str) -> None:
    if not (isinstance(obj, bytearray) or _is_writable_memoryview(obj)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be writable bytes-like, not {tname}")


def _check_bytes_w_opt(obj: object, name: str, default: object = None) -> Any:
    if obj is None:
        return default

    if not (isinstance(obj, bytearray) or _is_writable_memoryview(obj)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be writable bytes-like or None, not {tname}")
    return obj


def _is_writable_memoryview(obj):
    # TODO: _is_*
    return isinstance(obj, memoryview) and not obj.readonly
