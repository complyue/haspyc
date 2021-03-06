import asyncio
from typing import *

from hastalk import *
from haspyc import *

from numpy import float64, float32, int64, int32, intp, int8, bool

logger = get_logger(__package__)

# this will be filled by per-connection peer module preparation
# performed by EdhClient() on connection
peer: EdhClient = None


# this ought to be overwritten by the per-connection peer module
# initialization method passed to the EdhClient() ctor
db: DbClient = None


async def __edh_consumer__():
    logger.debug(f"Consuming DB service via: {peer!r}")

    # TODO support cmd prompt change request ?
    conin_sink = peer.arm_channel(CONIN)

    async def conout_intake(sink):
        async for con_out in sink.stream():
            print(con_out)

    asyncio.create_task(conout_intake(peer.arm_channel(CONOUT)))

    async def conmsg_intake(sink):
        async for con_msg in sink.stream():
            logger.info(con_msg)

    asyncio.create_task(conmsg_intake(peer.arm_channel(CONMSG)))

    async def peer_err_intake(sink):
        async for peer_err in sink.stream():
            logger.error(peer_err)
            if not peer.eol.done():
                peer.eol.set_exception(RuntimeError(peer_err))

    asyncio.create_task(peer_err_intake(peer.arm_channel(ERR_CHAN)))

    try:

        while True:
            cmd_val = await peer.read_command()
            if cmd_val is EndOfStream:
                break
            if cmd_val is not None:
                logger.warn(
                    f"Unexpected peer command from DB service via: {peer!r}\n  {cmd_val!r}"
                )

    except Exception:
        logger.error("Error occurred with the DB.", exc_info=True)

    finally:
        logger.debug(f"Done with DB servie via: {peer!r}")

        await peer.armed_channel(0).publish(EndOfStream)
        await peer.armed_channel(1).publish(EndOfStream)
        await peer.armed_channel(2).publish(EndOfStream)
