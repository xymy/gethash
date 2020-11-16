import glob
import os
import sys

__all__ = ["color", "cprint", "wrap_stream", "glob_resolver", "glob_scanner"]

ANSI_COLORS_FORE = {
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

ANSI_COLORS_BACK = {
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

ANSI_RESET_ALL = "\033[0m"


def color(msg, *, fg=None, bg=None):
    """Add ANSI color sequence to message.

    Parameters
    ----------
    msg : str
        A message.
    fg : str, optional
        The foreground color.
    bg : str, optional
        The background color.

    Returns
    -------
    cmsg : A message with colors.
    """

    if fg is not None:
        try:
            msg = ANSI_COLORS_FORE[fg] + msg
        except KeyError:
            raise ValueError("invalid foreground color '{}'".format(fg))

    if bg is not None:
        try:
            msg = ANSI_COLORS_BACK[bg] + msg
        except KeyError:
            raise ValueError("invalid background color '{}'".format(bg))

    return msg + ANSI_RESET_ALL


def cprint(*objs, sep=" ", end="\n", file=sys.stdout, flush=False, fg=None, bg=None):
    msg = sep.join(str(obj) for obj in objs) + end
    msg = color(msg, fg=fg, bg=bg)
    file.write(msg)
    if flush:
        file.flush()


def wrap_stream(stream, *, convert=None, strip=None, autoreset=False):
    if sys.platform == "win32":
        # Use lazy loading so that colorama is only required on Windows.
        import colorama

        wrapper = colorama.AnsiToWin32(
            stream, convert=convert, strip=strip, autoreset=autoreset
        )
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream


def glob_resolver(pathname, *, mode=0, recursive=False):
    """Resolve glob pathname.

    Parameters
    ----------
    pathname : str or path-like
        A pathname with glob pattern.
    mode : int
        The mode of glob. If ``0``, disable glob pathname pattern; if ``1``,
        resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    recursive : bool
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.

    Yields
    ------
    path : str
        The matched path.
    """

    pathname = os.fspath(pathname)
    if mode == 0:
        yield pathname
    elif mode == 1:
        pathname = pathname.replace("[", glob.escape("["))
        yield from glob.iglob(pathname, recursive=recursive)
    elif mode == 2:
        yield from glob.iglob(pathname, recursive=recursive)
    else:
        raise ValueError("invalid mode {}".format(mode))


def glob_scanner(pathnames, *, mode=0, recursive=False):
    """Resolve a list of glob pathnames.

    Parameters
    ----------
    pathnames : str or path-like
        A list of pathnames with glob pattern.
    mode : int
        The mode of glob. If ``0``, disable glob pathname pattern; if ``1``,
        resolve ``*`` and ``?``; if ``2``, resolve ``*``, ``?`` and ``[]``.
    recursive : bool
        If ``True``, the pattern ``**`` will match any files and zero or more
        directories, subdirectories and symbolic links to directories.

    Yields
    ------
    path : str
        The matched path.
    """

    for pathname in pathnames:
        yield from glob_resolver(pathname, mode=mode, recursive=recursive)
