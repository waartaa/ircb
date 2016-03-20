import asyncio

from aiohttp import web
from aiohttp_auth import auth

from ircb.storeclient import UserStore
from ircb.web.decorators import auth_required


class SigninView(web.View):

    @asyncio.coroutine
    def post(self):
        data = yield from self.request.post()
        user = yield from UserStore.get(
            dict(query=('auth', (data.get('username'), data.get('password'))))
        )
        if user:
            yield from auth.remember(self.request, user.username)
            return web.Response(body=b'OK')
        raise web.HTTPForbidden()


class SignoutView(web.View):

    @auth_required
    @asyncio.coroutine
    def post(self):
        yield from auth.forget(self.request)
        return web.Response(body=b'OK')
