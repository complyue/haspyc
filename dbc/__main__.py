import asyncio
from typing import *

from hastalk import *


peer: EdhClient = None


async def __edh_consumer__():

    print("peer is: ", peer)
