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
