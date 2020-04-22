import asyncio
from typing import *

from hastalk import *
from haspyc import *


# this will be filled by per-connection peer module preparation
# performed by EdhClient() on connection
peer: EdhClient = None


# this ought to be overwritten by the per-connection peer module
# initialization method passed to the EdhClient() ctor
async def __dbc_main__(peer: Peer):
    raise RuntimeError("No __dbc_main__() installed")


async def __edh_consumer__():
    await __dbc_main__(peer)
