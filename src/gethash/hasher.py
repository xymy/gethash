import io
import os

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
        The hash context prototype used to generate hash values.
    chunksize : int or None, optional
        The size of data blocks in bytes used when reading data from files.
    tqdm_args : dict or None, optional
        The arguments passed to the ``tqdm`` constructor.
    """

    def __init__(self, ctx_proto, *, chunksize=None, tqdm_args=None):
        # Use the copies of parameters for avoiding potential side-effects.
        self.ctx_proto = ctx_proto.copy()
        self.chunksize = _CHUNKSIZE if chunksize is None else int(chunksize)
        self.tqdm_args = {} if tqdm_args is None else dict(tqdm_args)
        # Set the unit of iterations as byte.
        self.tqdm_args.setdefault("unit", "B")
        self.tqdm_args.setdefault("unit_scale", True)
        self.tqdm_args.setdefault("unit_divisor", 1024)

    def __call__(self, path, start=None, stop=None, *, dir_ok=False):
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

        Returns
        -------
        hash_value : bytes
            The hash value of the file or the directory.
        """

        if os.path.isdir(path):
            if dir_ok:
                return bytes(self._hash_dir(path, start, stop))
            raise IsADirectory(f"'{path}' is a directory")
        return self._hash_file(path, start, stop)

    def _hash_dir(self, dirpath, start=None, stop=None):
        # The initial hash value is all zeros.
        value = bytearray(self.ctx_proto.digest_size)
        with os.scandir(dirpath) as it:
            for entry in it:
                if entry.is_dir():
                    other = self._hash_dir(entry, start, stop)
                else:
                    other = self._hash_file(entry, start, stop)
                # Just XOR each byte string as the result of hashing.
                strxor(value, other, value)
        return value

    def _hash_file(self, filepath, start=None, stop=None):
        # Clamp ``(start, stop)`` to ``(0, filesize)``.
        filesize = os.path.getsize(filepath)
        if start is None or start < 0:
            start = 0
        if stop is None or stop > filesize:
            stop = filesize
        if start > stop:
            raise ValueError(f"require start <= stop, but {start} > {stop}")

        # Setup the context.
        ctx = self.ctx_proto.copy()
        chunksize = self.chunksize
        total = stop - start
        # Precompute the chunk count and the remaining size.
        count, remainsize = divmod(total, chunksize)
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
