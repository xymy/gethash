def _check_int(obj, name):
    if not isinstance(obj, int):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be an integer, not {tname}")


def _check_int_opt(obj, name, default=None):
    if obj is None:
        return default

    if not isinstance(obj, int):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be None or an integer, not {tname}")
    return obj


def _check_str(obj, name):
    if not isinstance(obj, str):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be a string, not {tname}")


def _check_str_opt(obj, name, default=None):
    if obj is None:
        return default

    if not isinstance(obj, str):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be None or a string, not {tname}")
    return obj


def _check_bytes(obj, name):
    if not isinstance(obj, (bytes, bytearray)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be a byte string, not {tname}")


def _check_bytes_opt(obj, name, default=None):
    if obj is None:
        return default

    if not isinstance(obj, (bytes, bytearray)):
        tname = type(obj).__name__
        raise TypeError(f"{name} must be None or a byte string, not {tname}")
    return obj
