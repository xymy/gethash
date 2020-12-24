__all__ = ["strxor"]


def _strxor(b1, b2):
    return bytes(x1 ^ x2 for x1, x2 in zip(b1, b2))


try:
    from Cryptodome.Util.strxor import strxor as _strxor  # NOQA: F811
except ImportError:
    pass


def strxor(b1, b2):
    """XOR two byte strings.

    Parameters
    ----------
    b1 : bytes-like
        A byte string.
    b2 : bytes-like
        A byte string.

    Returns
    -------
    bytes
        The result of `b1` xor `b2`.
    """

    return _strxor(b1, b2)
