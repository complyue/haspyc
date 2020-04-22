import asyncio
from typing import *

from hastalk import *
from haspyc import *

logger = get_logger("haspyc.tour")


async def db_app():
    dbc = await DbClient(data_dir="demo", service_addr="127.0.0.1", service_port=3721,)
    peer = await dbc.peer

    logger.debug(f"db peer is: {peer}")

    dbc.stop()
    await dbc.join()  # reraise any error encountered


asyncio.run(db_app())
