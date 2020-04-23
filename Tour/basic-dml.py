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
        r"""
peer.p2c(2, repr('Starting...'))
"""
    )

    await peer.post_command(
        r"""
case db.deptByName[ 'Dev' ] of {
    { dev } -> { pass }

    peer.p2c(2, repr(
        'Populating DB contents.'
    ))

    dev = Depart('Dev')

    compl = Person( name = 'Compl', age = 41 )
    jim = Person( name = 'Jim', age = 11 )

    WorkFor( compl, dev, 12345 )
    WorkFor( jim, dev, 54321 )
}

case db.personByName['Compl'] of { compl=>_ } -> {
    peer.p2c(1, repr(
        "Compl's record is: " ++ compl
    ))
}
case db.personByName['Jim'] of { jim=>_ } -> {
    peer.p2c(1, repr(
        "Got a Jim ver# " ++ ( jim.version $=> 'legacy' )
    ))
}
peer.p2c(1, repr(
    'Dev Org is ' ++ dev ++ ' with workers:'
))
for (ixk, workRel) from dev.workers.range() do
    peer.p2c(1, repr(
        '  ' ++ workRel.person ++ ' in order of ' ++ ixk
    ))

# some artificial delay
for _ from console.everyMillis(200) do { break }

peer.p2c(1, repr("That's it atm."))

"""
    )

    await peer.post_command(
        r"""
peer.p2c(2, repr('Done.'))
"""
    )

    # wait a second to see some conout/conmsg before quitting the process
    await asyncio.sleep(1)

    dbc.stop()
    await dbc.join()  # reraise any error encountered


asyncio.run(db_app())
