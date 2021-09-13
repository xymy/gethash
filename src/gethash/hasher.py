import io
import os
import stat
from os import PathLike
from typing import Any, AnyStr, Dict, Mapping, Optional, Union

from tqdm import tqdm

from .utils.strxor import strxor

__all__ = ["IsADirectory", "Hasher"]

_CHUNKSIZE = 0x100000  # 1 MiB


class IsADirectory(OSError):
    """Raised by :meth:`Hasher.__call__`."""


class Hasher(object):
    """General hash values generator.

    Generate hash values via the given hash context prototype. Additionally,
    when calculating the hash value, a ``tqdm`` progress bar will be displayed.

    Parameters
    ----------
    ctx_proto : hash context
        The hash context prototype used to generate hash values.
    chunksize : int or None, optional
        The chunk size in bytes.
    tqdm_args : mapping or None, optional
        The arguments passed to the ``tqdm`` constructor.
    tqdm_class : tqdm or None, optional
        The ``tqdm`` class.
    """

    def __init__(
        self,
        ctx_proto: Any,
        *,
        chunksize: Optional[int] = None,
        tqdm_args: Optional[Mapping[str, Any]] = None,
        tqdm_class: Any = None,
    ) -> None:
        if chunksize is None:
            chunksize = _CHUNKSIZE
        elif not isinstance(chunksize, int):
            tn = type(chunksize).__name__
            raise TypeError(f"chunksize must be int or None, got {tn}")
        elif chunksize == 0:
            chunksize = _CHUNKSIZE
        elif chunksize < 0:
            chunksize = -1

        if tqdm_args is None:
            tqdm_args = {}
        elif not isinstance(tqdm_args, Mapping):
            tn = type(tqdm_args).__name__
            raise TypeError(f"tqdm_args must be Mapping or None, got {tn}")
        else:
            tqdm_args = dict(tqdm_args)

        # Set the progress bar meter style.
        tqdm_args.setdefault("unit", "B")
        tqdm_args.setdefault("unit_scale", True)
        tqdm_args.setdefault("unit_divisor", 1024)

        if tqdm_class is None:
            tqdm_class = tqdm

        self.ctx_proto = ctx_proto.copy()
        self.chunksize: int = chunksize
        self.tqdm_args: Dict[str, Any] = tqdm_args
        self.tqdm_class: tqdm = tqdm_class

    def __call__(
        self,
        path: Union[AnyStr, PathLike[AnyStr]],
        start: Optional[int] = None,
        stop: Optional[int] = None,
        *,
        dir_ok: bool = False,
    ) -> bytes:
        """Return the hash value of a file or a directory.

        Parameters
        ----------
        path : str, bytes or path-like
            The path of a file or a directory.
        start : int or None, optional
            The start offset of the file or files in the directory.
        stop : int or None, optional
            The stop offset of the file or files in the directory.
        dir_ok : bool, default=False
            If ``True``, enable directory hashing.

        Raises
        ------
        IsADirectory
            If ``dir_ok`` is ``False`` and ``path`` is a directory.

        Returns
        -------
        bytes
            The hash value of the file or the directory.
        """

        if not isinstance(start, (int, type(None))):
            tn = type(start).__name__
            raise TypeError(f"start must be int or None, got {tn!r}")
        if not isinstance(stop, (int, type(None))):
            tn = type(stop).__name__
            raise TypeError(f"stop must be int or None, got {tn!r}")

        st = os.stat(path)
        if stat.S_ISDIR(st.st_mode):
            if dir_ok:
                return self._hash_dir(path, start, stop)
            raise IsADirectory(f"{path!r} is a directory")
        return self._hash_file(path, start, stop)

    def _hash_dir(
        self,
        dirpath: Union[AnyStr, PathLike[AnyStr]],
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> bytes:
        # The initial hash value is all zeros.
        value = bytearray(self.ctx_proto.digest_size)
        with os.scandir(dirpath) as it:
            for entry in it:
                if entry.is_dir():
                    other = self._hash_dir(entry.path, start, stop)
                else:
                    other = self._hash_file(entry.path, start, stop)
                # Just XOR each byte string as the result of hashing.
                strxor(value, other, value)
        return bytes(value)

    def _hash_file(
        self,
        filepath: Union[AnyStr, PathLike[AnyStr]],
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> bytes:
        # Clamp ``(start, stop)`` to ``(0, filesize)``.
        filesize = os.stat(filepath).st_size
        if start is None or start < 0:
            start = 0
        if stop is None or stop > filesize:
            stop = filesize
        if start > stop:
            raise ValueError(f"require start <= stop, but {start!r} > {stop!r}")

        # Precompute some arguments for chunking.
        total = stop - start
        chunksize = self.chunksize
        count, remainsize = divmod(total, chunksize)

        ctx = self.ctx_proto.copy()
        with open(filepath, "rb") as f:
            f.seek(start, io.SEEK_SET)
            with self.tqdm_class(total=total, **self.tqdm_args) as bar:
                for _ in range(count):
                    chunk = f.read(chunksize)
                    ctx.update(chunk)
                    bar.update(chunksize)
                remain = f.read(remainsize)
                ctx.update(remain)
                bar.update(remainsize)
        return ctx.digest()
