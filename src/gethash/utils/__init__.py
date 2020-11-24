def _check_int(obj, name):
    if not isinstance(obj, int):
        tname = type(obj).__name__
        raise TypeError("{} must be an integer, not {}".format(name, tname))


def _check_int_opt(obj, name, default):
    if obj is None:
        return default

    if not isinstance(obj, int):
        tname = type(obj).__name__
        raise TypeError("{} must be None or an integer, not {}".format(name, tname))
    return obj


def _check_str(obj, name):
    if not isinstance(obj, str):
        tname = type(obj).__name__
        raise TypeError("{} must be a string, not {}".format(name, tname))


def _check_str_opt(obj, name, default):
    if obj is None:
        return default

    if not isinstance(obj, str):
        tname = type(obj).__name__
        raise TypeError("{} must be None or a string, not {}".format(name, tname))
    return obj
