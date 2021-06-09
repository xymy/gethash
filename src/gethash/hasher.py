import io
import os
from os import PathLike
from typing import Any, AnyStr, Mapping, Optional, Union, cast

from tqdm import tqdm

from .utils.strxor import strxor

__all__ = ["IsADirectory", "Hasher"]

_CHUNKSIZE = 0x100000  # 1 MiB


class IsADirectory(OSError):
    """Raised by :meth:`Hasher.__call__`."""


class Hasher(object):
    """General hash values generator.

    Generate hash values via the given hash context prototype. In addition, a
    ``tqdm`` progressbar is available.

    Parameters
    ----------
    ctx_proto : hash context
        The hash context prototype used for generating hash values.
    chunksize : int or None, optional
        The size of each data block in bytes used for chunking.
    tqdm_args : dict or None, optional
        The arguments passed to the ``tqdm`` constructor.
    """

    def __init__(
        self,
        ctx_proto,  # TODO
        *,
        chunksize: Optional[int] = None,
        tqdm_args: Optional[Mapping[str, Any]] = None,
    ) -> None:
        self.ctx_proto = ctx_proto.copy()
        self.chunksize = _CHUNKSIZE if chunksize is None else int(chunksize)
        self.tqdm_args = {} if tqdm_args is None else dict(tqdm_args)
        self.tqdm_args.setdefault("unit", "B")
        self.tqdm_args.setdefault("unit_scale", True)
        self.tqdm_args.setdefault("unit_divisor", 1024)

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
        hash_value : bytes
            The hash value of the file or the directory.
        """

        if os.path.isdir(path):
            if dir_ok:
                return self._hash_dir(path, start, stop)
            path_str = str(os.fspath(path))
            raise IsADirectory(f"'{path_str}' is a directory")
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
                path = cast(PathLike[str], entry)
                if entry.is_dir():
                    other = self._hash_dir(path, start, stop)
                else:
                    other = self._hash_file(path, start, stop)
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
        filesize = os.path.getsize(filepath)
        if start is None or start < 0:
            start = 0
        if stop is None or stop > filesize:
            stop = filesize
        if start > stop:
            raise ValueError(f"require start <= stop, but {start} > {stop}")

        # Precompute some arguments for chunking.
        total = stop - start
        chunksize = self.chunksize
        count, remainsize = divmod(total, chunksize)

        ctx = self.ctx_proto.copy()
        with open(filepath, "rb") as f, tqdm(total=total, **self.tqdm_args) as bar:
            f.seek(start, io.SEEK_SET)
            for _ in range(count):
                chunk = f.read(chunksize)
                ctx.update(chunk)
                bar.update(chunksize)
            remain = f.read(remainsize)
            ctx.update(remain)
            bar.update(remainsize)
        return ctx.digest()
