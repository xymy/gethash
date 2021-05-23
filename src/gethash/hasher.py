import io
import os

from tqdm import tqdm

from .utils.strxor import strxor

__all__ = ["IsADirectory", "Hasher"]

_CHUNKSIZE = 0x100000  # 1 MiB


class IsADirectory(OSError):
    """Raised by :meth:`Hasher.hash`."""


class Hasher(object):
    """General hash values generator.

    Generate hash values via given hash context prototype. In addition, a
    ``tqdm`` progressbar is available.

    Parameters
    ----------
    ctx_proto : hash context
        The hash context prototype used for generating hash values.
    chunksize : int or None, optional
        The size of data blocks used when reading data from files.
    tqdm_args : dict or None, optional
        The arguments passed to the underlying ``tqdm`` constructor.
    """

    def __init__(self, ctx_proto, *, chunksize=None, tqdm_args=None):
        # We use the copies of parameters for avoiding potential side-effects.
        self.ctx_proto = ctx_proto.copy()
        self.chunksize = _CHUNKSIZE if chunksize is None else int(chunksize)
        self.tqdm_args = {} if tqdm_args is None else dict(tqdm_args)
        # Set the unit of iterations as byte.
        self.tqdm_args.setdefault("unit", "B")
        self.tqdm_args.setdefault("unit_scale", True)
        self.tqdm_args.setdefault("unit_divisor", 1024)

    def hash_file(self, filepath, start=None, stop=None):
        """Return the hash value of a file.

        Parameters
        ----------
        filepath : str or path-like
            The path of a file.
        start : int or None, optional
            The start offset of the file.
        stop : int or None, optional
            The stop offset of the file.

        Returns
        -------
        hash_value : bytes
            The hash value of the file.
        """

        # Decide the range of current file. Use (0, filesize) by default.
        # The (start, stop) will be shrinked to (0, filesize) if necessary.
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
        # Precompute chunk count and remaining size.
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

    def hash_dir(self, dirpath, start=None, stop=None):
        """Return the hash value of a directory.

        Parameters
        ----------
        dirpath : str or path-like
            The path of a directory.
        start : int or None, optional
            The start offset of files belonging to the directory.
        stop : int or None, optional
            The stop offset of files belonging to the directory.

        Returns
        -------
        hash_value : bytes
            The hash value of the directory.
        """

        # The initial hash value is all zeros.
        value = bytearray(self.ctx_proto.digest_size)
        with os.scandir(dirpath) as it:
            for entry in it:
                if entry.is_dir():
                    other = self.hash_dir(entry, start, stop)
                else:
                    other = self.hash_file(entry, start, stop)
                # Just XOR each byte string as hash value.
                strxor(value, other, value)
        return bytes(value)

    def hash(self, path, start=None, stop=None, *, dir_ok=False):
        """Return the hash value of a file or a directory.

        Parameters
        ----------
        path : str or path-like
            The path of a file or a directory.
        start : int or None, optional
            The start offset of the file or files belonging to the directory.
        stop : int or None, optional
            The stop offset of the file or files belonging to the directory.
        dir_ok : bool, default=False
            If ``True``, enable directory hashing.

        Returns
        -------
        hash_value : bytes
            The hash value of the file or the directory.
        """

        if os.path.isdir(path):
            if dir_ok:
                return self.hash_dir(path, start, stop)
            raise IsADirectory(f"'{path}' is a directory")
        return self.hash_file(path, start, stop)

    __call__ = hash
