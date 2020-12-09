import sys

from . import _check_str, _check_str_opt

__all__ = ["add_color", "cprint", "wrap_stream"]

_ANSI_COLORS_FORE = {
    "black": "\x1b[30m",
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "blue": "\x1b[34m",
    "magenta": "\x1b[35m",
    "cyan": "\x1b[36m",
    "white": "\x1b[37m",
    "reset": "\x1b[39m",
    "bright_black": "\x1b[90m",
    "bright_red": "\x1b[91m",
    "bright_green": "\x1b[92m",
    "bright_yellow": "\x1b[93m",
    "bright_blue": "\x1b[94m",
    "bright_magenta": "\x1b[95m",
    "bright_cyan": "\x1b[96m",
    "bright_white": "\x1b[97m",
}

_ANSI_COLORS_BACK = {
    "black": "\x1b[40m",
    "red": "\x1b[41m",
    "green": "\x1b[42m",
    "yellow": "\x1b[43m",
    "blue": "\x1b[44m",
    "magenta": "\x1b[45m",
    "cyan": "\x1b[46m",
    "white": "\x1b[47m",
    "reset": "\x1b[49m",
    "bright_black": "\x1b[100m",
    "bright_red": "\x1b[101m",
    "bright_green": "\x1b[102m",
    "bright_yellow": "\x1b[103m",
    "bright_blue": "\x1b[104m",
    "bright_magenta": "\x1b[105m",
    "bright_cyan": "\x1b[106m",
    "bright_white": "\x1b[107m",
}

_ANSI_RESET_ALL = "\033[0m"


def add_color(msg, *, fg=None, bg=None):
    """Add ANSI color sequence to a message.

    Parameters
    ----------
    msg : str
        A message.
    fg : str or None, optional (default: None)
        The foreground color in ``{'black', 'red', 'green', 'yellow', 'blue',
        'magenta', 'cyan', 'white', 'reset', 'bright_black', 'bright_red',
        'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta',
        'bright_cyan', 'bright_white'}``.
    bg : str or None, optional (default: None)
        The background color in ``{'black', 'red', 'green', 'yellow', 'blue',
        'magenta', 'cyan', 'white', 'reset', 'bright_black', 'bright_red',
        'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta',
        'bright_cyan', 'bright_white'}``.

    Returns
    -------
    cmsg : str
        A colorful message.
    """

    _check_str(msg, "msg")

    if fg is not None:
        try:
            msg = _ANSI_COLORS_FORE[fg] + msg
        except KeyError:
            raise ValueError("invalid foreground color '{}'".format(fg))

    if bg is not None:
        try:
            msg = _ANSI_COLORS_BACK[bg] + msg
        except KeyError:
            raise ValueError("invalid background color '{}'".format(bg))

    return msg + _ANSI_RESET_ALL


def cprint(
    *objs, sep=" ", end="\n", file=sys.stdout, flush=False, fg=None, bg=None, tty=False
):
    """Print a colorful message.

    Parameters
    ----------
    objs : any
        Any objects.
    sep : str or None, optional (default: " ")
        The same as builtin `print`.
    end : str or None, optional (default: "\n")
        The same as builtin `print`.
    file : file-like or None, optional (default: sys.stdout)
        The same as builtin `print`.
    flush : bool, optional (default: False)
        The same as builtin `print`.
    fg : str or None, optional (default: None)
        The foreground color in ``{'black', 'red', 'green', 'yellow', 'blue',
        'magenta', 'cyan', 'white', 'reset', 'bright_black', 'bright_red',
        'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta',
        'bright_cyan', 'bright_white'}``.
    bg : str or None, optional (default: None)
        The background color in ``{'black', 'red', 'green', 'yellow', 'blue',
        'magenta', 'cyan', 'white', 'reset', 'bright_black', 'bright_red',
        'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta',
        'bright_cyan', 'bright_white'}``.
    tty : bool, optional (default: False)
        If ``True``, always add ANSI color sequence. If ``False``, add ANSI
        color sequence if and only if `file` is a tty.
    """

    sep = _check_str_opt(sep, "sep", " ")
    end = _check_str_opt(end, "end", "\n")
    if file is None:
        file = sys.stdout

    msg = sep.join(str(obj) for obj in objs) + end
    if tty or file.isatty():
        msg = add_color(msg, fg=fg, bg=bg)
    file.write(msg)
    if flush:
        file.flush()


def wrap_stream(stream):
    """Wrap stream using `colorama.AnsiToWin32` on Windows. No effect on other
    platforms.

    Parameters
    ----------
    stream : file-like
        The output stream that will be wrapped.

    Returns
    -------
    wrapped_stream : file-like
        The wrapped output stream.
    """

    if sys.platform == "win32":
        # Use lazy loading so that ``colorama`` is only required on Windows.
        import colorama

        # Disable auto strip for file stream.
        wrapper = colorama.AnsiToWin32(stream, strip=False)
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream
