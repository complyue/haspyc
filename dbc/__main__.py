import asyncio
from typing import *

from hastalk import *
from haspyc import *

logger = get_logger(__package__)

# this will be filled by per-connection peer module preparation
# performed by EdhClient() on connection
peer: EdhClient = None


# this ought to be overwritten by the per-connection peer module
# initialization method passed to the EdhClient() ctor
db: DbClient = None


async def __edh_consumer__():
    # TODO support cmd prompt change request ?
    conin_sink = peer.arm_channel(0)

    async def conout_intake(sink):
        async for con_out in sink.stream():
            print(con_out)

    asyncio.create_task(conout_intake(peer.arm_channel(1)))

    async def conlog_intake(sink):
        async for con_log in sink.stream():
            logger.info(con_log)

    asyncio.create_task(conlog_intake(peer.arm_channel(2)))

    while True:
        cmd_val = await peer.read_command(globals())
        if cmd_val is EndOfStream:
            break
        if cmd_val is not None:
            logger.warn(f"Unexpected peer command from DB server: {cmd_val!r}")
