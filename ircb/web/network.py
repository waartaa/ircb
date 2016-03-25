import asyncio
import json

from aiohttp import web
from aiohttp_auth.auth import get_auth
from ircb.web.decorators import auth_required
from ircb.web.lib import View
from ircb.storeclient import UserStore, NetworkStore
from ircb.forms import NetworkForm


class NetworkListView(View):
    store = NetworkStore

    @auth_required
    @asyncio.coroutine
    def get(self):
        username = yield from get_auth(self.request)
        user = yield from UserStore.get(
            dict(query=('username', username)))
        networks = yield from NetworkStore.get(
            dict(query={'user_id': user.id})) or []
        return web.Response(body=self.serialize(networks).encode(),
                            content_type='application/json')

    @auth_required
    @asyncio.coroutine
    def post(self):
        username = yield from get_auth(self.request)
        data = yield from self.request.post()
        form = NetworkForm(**data)
        form.validate()
        if form.errors:
            return web.Response(
                body=json.dumps(form.errors).encode(),
                status=400,
                content_type='application/json')
        cleaned_data = form.data
        cleaned_data['user'] = username
        network = yield from NetworkStore.create(**cleaned_data)
        return web.Response(body=self.serialize(network).encode(),
                            content_type='application/json')


class NetworkView(View):
    store = NetworkStore
    w_fields = ['name', 'nickname', 'hostname', 'port', 'realname',
                'username', 'password', 'usermode', 'ssl',
                'ssl_verify']
    post_reqd_fields = ['user', 'name', 'host', 'port', 'nick']

    @auth_required
    @asyncio.coroutine
    def get(self):
        username = yield from get_auth(self.request)
        user = yield from UserStore.get(
            dict(query=('username', username)))
        network_id = self.request.match_info['id']
        networks = yield from NetworkStore.get(
            dict(query={'user_id': user.id, 'id': int(network_id)}))
        network = (networks and networks[0]) or None
        if network is None:
            raise web.HTTPNotFound()
        return web.Response(body=self.serialize(network).encode(),
                            content_type='application/json')
