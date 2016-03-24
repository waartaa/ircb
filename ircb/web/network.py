import asyncio

from aiohttp import web
from aiohttp_auth.auth import get_auth
from ircb.web.decorators import auth_required
from ircb.web.lib import View
from ircb.storeclient import UserStore, NetworkStore


class NetworkListView(View):
    store = NetworkStore
    datetime_fields = ['created', 'last_updated']

    @auth_required
    @asyncio.coroutine
    def get(self):
        username = yield from get_auth(self.request)
        user = yield from UserStore.get(
            dict(query=('username', username)))
        networks = yield from NetworkStore.get(
            dict(query={'user_id': user.id}))
        return web.Response(body=self.serialize(networks).encode(),
                            content_type='application/json')

