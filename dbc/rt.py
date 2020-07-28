import asyncio
from typing import *

import os.path
import mmap
import numpy as np

from hastalk import *

from ..log import *

__all__ = ["ArrayMeta", "DbArray"]

logger = get_logger(__name__)


class ArrayMeta(NamedTuple):
    data_dir: str
    data_path: str
    shape: Tuple[int, ...]
    dtype: str
    len1d: int


class DbArray:
    __slots__ = "meta", "mm"

    def __init__(
        self,
        data_dir: str,
        data_path: str,
        shape: Tuple[int, ...],
        dtype: str = "f8",
        len1d: int = 0,
    ):
        self.meta = ArrayMeta(data_dir, data_path, shape, dtype, len1d)

        dt = np.dtype(dtype)
        nbytes = dt.itemsize * np.prod(shape)

        data_file_path = f"{data_dir}/{data_path}.edf"
        data_file_dir = os.path.dirname(data_file_path)
        os.makedirs(data_file_dir, mode=0o755, exist_ok=True)
        fd = os.open(data_file_path, os.O_RDWR | os.O_CREAT, mode=0o644)
        try:
            os.ftruncate(fd, nbytes)
            self.mm = mmap.mmap(
                fileno=fd,
                length=nbytes,
                flags=mmap.MAP_SHARED,
                access=mmap.ACCESS_WRITE,
            )
        finally:
            os.close(fd)

    def __repr__(self):
        meta = self.meta
        return (
            f"db.Array({meta.data_path!r},{meta.shape!r},{meta.dtype!r},{meta.len1d!r})"
        )

    @property
    def ndarray(self):
        meta = self.meta
        return np.ndarray(shape=meta.shape, dtype=meta.dtype, buffer=self.mm,)
