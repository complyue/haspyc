import asyncio
from typing import *

from hastalk import *

from ..log import *

from .rt import *

__all__ = ["DbClient"]

logger = get_logger(__name__)


class DbClient:
    __slots__ = ("data_dir", "clnt", "peer")

    def __init__(
        self, data_dir: str, service_addr: str = "127.0.0.1", service_port: int = 3721,
    ):
        loop = asyncio.get_running_loop()
        self.data_dir = data_dir
        self.clnt = EdhClient(
            "haspyc.dbc", service_addr, service_port, init=self.__peer_init__,
        )
        self.peer = loop.create_future()

        async def dbc_cleanup():
            try:
                await self.clnt.eol
                if not self.peer.done():
                    self.peer.set_result(None)
            except Exception as exc:
                if not self.peer.done():
                    self.peer.set_exception(exc)

        asyncio.create_task(dbc_cleanup())

    def __repr__(self):
        clnt = self.clnt
        return f"DbClient({clnt.service_addr!r}, {clnt.service_port!r})"

    async def __peer_init__(self, modu):
        if not self.peer.done():
            self.peer.set_result(modu["peer"])
        modu["db"] = self

    def __await__(self):
        yield from self.clnt.service_addrs
        return self

    async def join(self):
        await self.clnt.eol

    def stop(self):
        self.clnt.stop()

    def Array(
        self, data_path: str, shape: Tuple[int, ...], dtype: str = "f8", len1d: int = 0,
    ):
        return DbArray(self.data_dir, data_path, shape, dtype, len1d,)
