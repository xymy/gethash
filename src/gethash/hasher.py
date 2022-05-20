import io
import os
from os import PathLike
from typing import Any, AnyStr, Dict, Optional, Union, cast

from tqdm import tqdm

from .utils.strxor import strxor

__all__ = ["IsADirectory", "Hasher"]

_CHUNKSIZE = 0x100000  # 1 MiB


class IsADirectory(OSError):
    """Raised by :meth:`Hasher.__call__`."""


class Hasher:
    """General hash values generator.

    Generate hash values via the given hash context prototype. Additionally,
    when calculating the hash value, a ``tqdm`` progress bar will be displayed.

    Parameters:
        ctx (hash-context):
            The hash context prototype used to generate hash values.
        chunksize (int | None, default=None):
            The chunk size for reading data from files.
        tqdm_args (Dict | None, default=None):
            The arguments passed to the ``tqdm_class``.
        tqdm_class (tqdm-class | None, default=None):
            The ``tqdm`` class.
    """

    def __init__(
        self,
        ctx: Any,
        *,
        chunksize: Optional[int] = None,
        tqdm_args: Optional[Dict[str, Any]] = None,
        tqdm_class: Any = None,
    ) -> None:
        if chunksize is None:
            chunksize = _CHUNKSIZE
        elif isinstance(chunksize, int):
            if chunksize == 0:
                chunksize = _CHUNKSIZE
            elif chunksize < 0:
                chunksize = -1  # -1 for read all bytes
        else:
            tn = type(chunksize).__name__
            raise TypeError(f"chunksize must be int or None, not {tn}")

        if tqdm_args is None:
            tqdm_args = {}
        elif isinstance(tqdm_args, Dict):
            tqdm_args = dict(tqdm_args)
        else:
            tn = type(tqdm_args).__name__
            raise TypeError(f"tqdm_args must be Dict or None, not {tn}")

        # Set the progress bar meter style.
        tqdm_args.setdefault("unit", "B")
        tqdm_args.setdefault("unit_scale", True)
        tqdm_args.setdefault("unit_divisor", 1024)

        if tqdm_class is None:
            tqdm_class = tqdm

        self._ctx = ctx.copy()
        self.chunksize = chunksize
        self.tqdm_args = tqdm_args
        self.tqdm_class = tqdm_class

    def __call__(
        self,
        path: "Union[AnyStr, PathLike[AnyStr]]",
        start: Optional[int] = None,
        stop: Optional[int] = None,
        *,
        dir_ok: bool = False,
    ) -> bytes:
        """Return the hash value of a file or a directory.

        Parameters:
            path (AnyStr | PathLike[AnyStr]):
                The path of a file or a directory.
            start (int | None, default=None):
                The start offset of the file or files in the directory.
            stop (int | None, default=None):
                The stop offset of the file or files in the directory.
            dir_ok (bool, default=False):
                If ``True``, enable directory hashing.

        Raises:
            IsADirectory
                If ``dir_ok`` is ``False`` and ``path`` is a directory.

        Returns:
            bytes:
                The hash value of the file or the directory.
        """

        if start is not None and not isinstance(start, int):
            tn = type(start).__name__
            raise TypeError(f"start must be int or None, not {tn}")
        if stop is not None and not isinstance(stop, int):
            tn = type(stop).__name__
            raise TypeError(f"stop must be int or None, not {tn}")

        if os.path.isdir(path):
            if dir_ok:
                return self._hash_dir(path, start, stop)
            raise IsADirectory(f"{path!r} is a directory")
        return self._hash_file(path, start, stop)

    def _hash_dir(
        self,
        dirpath: "Union[AnyStr, PathLike[AnyStr]]",
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> bytes:
        # The initial hash value is all zeros.
        value = bytearray(self._ctx.digest_size)
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
        filepath: "Union[AnyStr, PathLike[AnyStr]]",
        start: Optional[int] = None,
        stop: Optional[int] = None,
    ) -> bytes:
        # Clamp ``(start, stop)`` to ``(0, filesize)``.
        filesize = os.path.getsize(filepath)
        if start is None or start < 0:
            start = 0
        if stop is None or stop > filesize:
            stop = filesize
        if start > stop:
            raise ValueError(f"require start <= stop, but {start!r} > {stop!r}")

        # Precompute some arguments for chunking.
        total = stop - start
        chunksize = self.chunksize
        if chunksize > 0:
            count, remainsize = divmod(total, chunksize)
        else:
            count = 1
            remainsize = 0

        ctx = self._ctx.copy()
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
        return cast(bytes, ctx.digest())
