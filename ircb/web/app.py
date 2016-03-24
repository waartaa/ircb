import asyncio
import logging
import logging.config

from aiohttp import web
from aiohttp_auth import auth
from aiohttp_session import get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from ircb.config import settings
from ircb.web.user import SigninView, SignoutView
from ircb.web.network import NetworkListView, NetworkView

logging.config.dictConfig(settings.LOGGING_CONF)


@asyncio.coroutine
def index(request):
    return web.Response(body=b"Hello, ircb!")


@asyncio.coroutine
def init(loop):
    from ircb.storeclient import initialize
    initialize()
    policy = auth.SessionTktAuthentication(
        settings.WEB_SALT, 60, include_ip=True)
    middlewares = [
        session_middleware(EncryptedCookieStorage(settings.WEB_SALT)),
        auth.auth_middleware(policy)
    ]

    app = web.Application(middlewares=middlewares)
    app.router.add_route('GET', '/', index)

    app.router.add_route('*', '/api/signin', SigninView, name='signin')
    app.router.add_route('*', '/api/signout', SignoutView, name='signout')
    app.router.add_route('*', '/api/networks', NetworkListView,
                         name='networks')
    app.router.add_route('*', '/api/network/{id}', NetworkView,
                         name='network')
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
