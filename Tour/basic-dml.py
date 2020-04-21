import asyncio
from typing import *

from hastalk import *
from haspyc import *

logger = get_logger(__name__)

__all__ = ()


async def __peer_init__(modu):
    logger.info(
        "peer modu is loaded from: ", file=modu.__file__,
    )


async def main():

    dbc = EdhClient("dbc", "127.0.0.1", 3721, init=__peer_init__,)

    addrs = await dbc.addrs()

    logger.info("Connected to DB", addrs=addrs)


asyncio.run(main())
