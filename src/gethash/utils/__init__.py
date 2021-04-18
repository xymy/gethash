from typing import Any


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
    if not (isinstance(obj, bytearray) or (isinstance(obj, memoryview) and not obj.readonly)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be writable bytes-like, not {tname}")


def _check_bytes_w_opt(obj: object, name: str, default: object = None) -> Any:
    if obj is None:
        return default

    if not (isinstance(obj, bytearray) or (isinstance(obj, memoryview) and not obj.readonly)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be writable bytes-like or None, not {tname}")
    return obj
