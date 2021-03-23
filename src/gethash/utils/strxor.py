from . import _check_bytes, _check_bytes_w_opt

__all__ = ["strxor"]


def _py_strxor(term1, term2, output=None):
    if output is None:
        return bytes(x1 ^ x2 for x1, x2 in zip(term1, term2))
    else:
        for i, (x1, x2) in enumerate(zip(term1, term2)):
            output[i] = x1 ^ x2


try:
    from Cryptodome.Util.strxor import strxor as _strxor  # NOQA: F811
except ImportError:
    _strxor = _py_strxor


def strxor(term1, term2, output=None):
    """XOR two byte strings.

    Parameters
    ----------
    term1 : bytes-like
        The first term of the XOR operation.
    term2 : bytes-like
        The second term of the XOR operation.
    output : writable bytes-like or None, optional
        The location where the result must be written to. If ``None``, the
        result is returned.

    Returns
    -------
    result : bytes or None
        If `output` is ``None``, return a new byte string; otherwise return
        ``None``.
    """

    _check_bytes(term1, "term1")
    _check_bytes(term2, "term2")
    _check_bytes_w_opt(output, "output")
    if len(term1) != len(term2):
        raise ValueError("term1 and term2 must have the same length")
    if output is not None and len(output) != len(term1):
        raise ValueError("output must have the same length as the input")
    return _strxor(term1, term2, output)
