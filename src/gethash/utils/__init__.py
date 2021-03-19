def _check_int(obj, name):
    if not isinstance(obj, int):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be int, not {tname}")


def _check_int_opt(obj, name, default=None):
    if obj is None:
        return default

    if not isinstance(obj, int):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be int or None, not {tname}")
    return obj


def _check_str(obj, name):
    if not isinstance(obj, str):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be str, not {tname}")


def _check_str_opt(obj, name, default=None):
    if obj is None:
        return default

    if not isinstance(obj, str):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be str or None, not {tname}")
    return obj


def _check_bytes(obj, name):
    if not isinstance(obj, (bytes, bytearray)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be bytes or bytearray, not {tname}")


def _check_bytes_opt(obj, name, default=None):
    if obj is None:
        return default

    if not isinstance(obj, (bytes, bytearray)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be bytes, bytearray or None, not {tname}")
    return obj


def _check_bytearray(obj, name):
    if not isinstance(obj, bytearray):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be bytearray, not {tname}")


def _check_bytearray_opt(obj, name, default=None):
    if obj is None:
        return default

    if not isinstance(obj, bytearray):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be bytearray or None, not {tname}")
    return obj
