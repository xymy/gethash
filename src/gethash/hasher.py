from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Protocol

from tqdm import tqdm
from typing_extensions import Self

from .utils.strxor import strxor

__all__ = ["IsADirectory", "HashContext", "Hasher"]

_CHUNKSIZE = 0x100000  # 1 MiB


class IsADirectory(OSError):
    """Raised by :meth:`Hasher.__call__`."""


class HashContext(Protocol):
    """Typing for hash context."""

    @property
    def digest_size(self) -> int:
        ...

    def update(self, data: bytes) -> None:
        ...

    def digest(self) -> bytes:
        ...

    def copy(self: Self) -> Self:
        ...


class Hasher:
    """General hash values generator.

    Generate hash values via the given hash context prototype. Additionally,
    when calculating the hash value, a ``tqdm`` progress bar will be displayed.

    Parameters:
        ctx (HashContext):
            The hash context prototype used to generate hash values.
        chunksize (int | None, default=None):
            The chunk size for reading data from files.
        tqdm_args (Dict[str, Any] | None, default=None):
            The arguments passed to the ``tqdm_type``.
        tqdm_type (Type[tqdm] | None, default=None):
            The ``tqdm`` type.
    """

    def __init__(
        self,
        ctx: HashContext,
        *,
        chunksize: int | None = None,
        tqdm_args: dict[str, Any] | None = None,
        tqdm_type: type[tqdm] | None = None,
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
        elif isinstance(tqdm_args, dict):
            tqdm_args = dict(tqdm_args)
        else:
            tn = type(tqdm_args).__name__
            raise TypeError(f"tqdm_args must be dict or None, not {tn}")

        # Set the progress bar meter style.
        tqdm_args.setdefault("unit", "B")
        tqdm_args.setdefault("unit_scale", True)
        tqdm_args.setdefault("unit_divisor", 1024)

        if tqdm_type is None:
            tqdm_type = tqdm

        self._ctx = ctx.copy()
        self.chunksize = chunksize
        self.tqdm_args = tqdm_args
        self.tqdm_type = tqdm_type

    def __call__(
        self, path: str | Path, start: int | None = None, stop: int | None = None, *, dir_ok: bool = False
    ) -> bytes:
        """Return the hash value of a file or a directory.

        Parameters:
            path (str | Path):
                The path of a file or a directory.
            start (int | None, default=None):
                The start offset of the file or files in the directory.
            stop (int | None, default=None):
                The stop offset of the file or files in the directory.
            dir_ok (bool, default=False):
                If ``True``, enable directory hashing.

        Raises:
            IsADirectory:
                If ``dir_ok`` is ``False`` and ``path`` is a directory.

        Returns:
            bytes:
                The hash value of the file or the directory.
        """

        path = Path(path)
        if path.is_dir():
            if dir_ok:
                return self._hash_dir(path, start, stop)
            raise IsADirectory(f"{str(path)!r} is a directory")
        return self._hash_file(path, start, stop)

    def _hash_dir(self, dirpath: Path, start: int | None = None, stop: int | None = None) -> bytes:
        # The initial hash value is all zeros.
        value = bytearray(self._ctx.digest_size)
        for entry in dirpath.iterdir():
            if entry.is_dir():
                other = self._hash_dir(entry, start, stop)
            else:
                other = self._hash_file(entry, start, stop)
            # Just XOR each byte string as the result of hashing.
            strxor(value, other, value)
        return bytes(value)

    def _hash_file(self, filepath: Path, start: int | None = None, stop: int | None = None) -> bytes:
        # Clamp `(start, stop)` to `(0, filesize)`.
        filesize = filepath.stat().st_size
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
            f.seek(start, os.SEEK_SET)
            with self.tqdm_type(total=total, **self.tqdm_args) as bar:
                for _ in range(count):
                    chunk = f.read(chunksize)
                    ctx.update(chunk)
                    bar.update(chunksize)
                remain = f.read(remainsize)
                ctx.update(remain)
                bar.update(remainsize)
        return ctx.digest()
