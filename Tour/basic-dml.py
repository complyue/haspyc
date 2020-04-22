import asyncio
from typing import *

from hastalk import *
from haspyc import *

logger = get_logger("haspyc.tour")


async def dbc_main(peer: Peer):

    logger.debug(f"db peer is: {peer}")


asyncio.run(run_dbc_app(dbc_main, "127.0.0.1", 3721))
