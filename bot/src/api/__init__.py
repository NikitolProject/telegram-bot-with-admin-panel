import asyncio

import tornado.ioloop
import tornado.web

from ajsonrpc.backend.tornado import JSONRPCTornado

__all__ = ('api', 'start_jsonrpc')

api = JSONRPCTornado()


def make_app():
    return tornado.web.Application([
        (r"/jsonrpc", api.handler),
    ])


async def start_jsonrpc() -> None:
    app = make_app()
    app.listen(8888)
    asyncio.run_coroutine_threadsafe(asyncio.Event().wait(), asyncio.get_event_loop())
