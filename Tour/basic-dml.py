import asyncio
from typing import *

from hastalk import *
from haspyc import *

logger = get_logger("haspyc.tour")


async def db_app():
    dbc = await DbClient(
        data_dir="/var/tmp/demo", service_addr="127.0.0.1", service_port=3721,
    )
    peer = await dbc.peer

    await peer.post_command(
        expr(
            r"""
peer.p2c({$ CONMSG $}, repr('Starting...'))
"""
        )
    )

    data_chan = "data1"
    data_sink = peer.arm_channel(data_chan)
    data_sink.run_producer(
        peer.post_command(
            expr(
                r"""
case db.deptByName[ 'Dev' ] of {
    { dev } -> { pass }

    peer.p2c({$ CONMSG $}, repr(
        'Populating DB contents.'
    ))

    dev = Depart('Dev')

    compl = Person( name = 'Compl', age = 41 )
    jim = Person( name = 'Jim', age = 11 )

    WorkFor( compl, dev, 12345 )
    WorkFor( jim, dev, 54321 )
}

case db.personByName['Compl'] of { compl=>_ } -> {
    peer.p2c({$ data_chan $}, repr(
        {"name": compl.name, 'description': repr(compl)}
    ))
}
case db.personByName['Jim'] of { jim=>_ } -> {
    peer.p2c({$ data_chan $}, repr(
        {"name": jim.name, 'version': repr( jim.version $=> 'legacy' )}
    ))
}

peer.p2c({$ data_chan $}, repr(
    {
        'name': dev.name, 
        'workers': ([] =< for (ixk, workRel) from dev.workers.range() do
            {'name': workRel.person.name, 'ixk': repr(ixk), }
        ),

    }
))

peer.p2c({$ CONMSG $}, repr("That's it atm."))
peer.p2c({$ data_chan $}, expr EndOfStream)
    """
            )
        )
    )
    async for record in data_sink.stream():
        print("Got data:", record)

    await peer.post_command(
        expr(
            r"""
peer.p2c({$ CONMSG $}, repr('Done.'))
"""
        )
    )

    dbc.stop()
    await dbc.join()  # reraise any error encountered


asyncio.run(db_app())
