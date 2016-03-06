import asyncio

from aiohttp import web

from ircb.storeclient import UserStore


class SigninView(web.View):

    @asyncio.coroutine
    def post(self):
        data = yield from self.request.post()
        user = yield from UserStore.get(
            dict(query=('auth', (data.get('username'), data.get('password'))))
        )
        if user:
            return web.Response(body=b'OK', status=200)
        else:
            return web.Response(body=b'LOGIN FAILURE', status=400)
