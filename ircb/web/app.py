import asyncio
import logging
import logging.config

from aiohttp import web

from ircb.config import settings
from ircb.web.user import SigninView

logging.config.dictConfig(settings.LOGGING_CONF)


@asyncio.coroutine
def index(request):
    return web.Response(body=b"Hello, ircb!")


app = web.Application()
app.router.add_route('GET', '/', index)

app.router.add_route('*', '/api/signin', SigninView, name='signin')


@asyncio.coroutine
def init(loop):
    from ircb.storeclient import initialize
    initialize()
    srv = yield from loop.create_server(
        app.make_handler(), '0.0.0.0', 10001)
    return srv

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
