import asyncio
from typing import *

from hastalk import *

from ..log import *

__all__ = ["run_dbc_app", "make_dbc"]

logger = get_logger(__name__)


async def run_dbc_app(
    dbc_main: Callable[[Peer], Awaitable],
    service_addr: str = "127.0.0.1",
    service_port: int = 3721,
):
    async def __peer_init__(modu):
        logger.debug(f"DBC peer modu is loaded from: {modu['__file__']!s}")
        modu["__dbc_main__"] = dbc_main

    dbc = await EdhClient("haspyc.dbc", service_addr, service_port, init=__peer_init__,)
    await dbc.eol
    logger.info("Done with DB.")


async def make_dbc(
    service_addr: str = "127.0.0.1", service_port: int = 3721,
):
    loop = asyncio.get_running_loop()
    dbc_peer = loop.create_future()

    async def __dbc_main__(peer: Peer):
        dbc_peer.set_result(peer)
        await peer.join()

    async def __peer_init__(modu):
        logger.debug(f"DBC peer modu is loaded from: {modu['__file__']!s}")
        modu["__dbc_main__"] = __dbc_main__

    dbc = await EdhClient("haspyc.dbc", service_addr, service_port, init=__peer_init__,)
    peer = await dbc_peer
    return dbc, peer
