# -*- coding: utf-8 -*-
import asyncio
import json

from aiohttp import web, MultiDict
from aiohttp_auth.auth import get_auth

from ircb.web.decorators import auth_required
from ircb.web.lib import View
from ircb.storeclient import UserStore, NetworkStore
from ircb.forms import NetworkForm


class NetworkViewMixin(object):

    @asyncio.coroutine
    def _create_or_update(self, data, username, network=None):
        if network:
            network_data = network.to_dict()
            network_data.update(data)
            form = NetworkForm(formdata=MultiDict(network_data))
        else:
            form = NetworkForm(formdata=MultiDict(data))
        form.validate()
        if form.errors:
            return web.Response(
                body=json.dumps(form.errors).encode(),
                status=400,
                content_type='application/json')
        cleaned_data = form.data
        cleaned_data['user'] = username
        if network:
            network = yield from NetworkStore.update(
                dict(
                    filter=('id', network.id),
                    update=cleaned_data
                )
            )
        else:
            network = yield from NetworkStore.create(**cleaned_data)
        return web.Response(body=self.serialize(network).encode(),
                            content_type='application/json')


class NetworkListView(View, NetworkViewMixin):
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
        resp = yield from self._create_or_update(data, username)
        return resp


class NetworkView(View, NetworkViewMixin):
    store = NetworkStore

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

    @auth_required
    @asyncio.coroutine
    def put(self):
        network_id = self.request.match_info['id']
        username = yield from get_auth(self.request)
        data = yield from self.request.post()
        user = yield from UserStore.get(
            dict(query=('username', username)))
        networks = yield from NetworkStore.get(
            dict(query={'user_id': user.id, 'id': network_id})
        )
        if not networks:
            raise web.HTTPNotFound()
        resp = yield from self._create_or_update(data, username, networks[0])
        return resp


class NetworkConnectionView(View):
    store = NetworkStore

    @auth_required
    @asyncio.coroutine
    def put(self):
        network_id = self.request.match_info['id']
        action = self.request.match_info['action']
        if action not in ('connect', 'disconnect'):
            raise web.HTTPNotFound()
        username = yield from get_auth(self.request)
        user = yield from UserStore.get(
            dict(query=('username', username)))
        networks = yield from NetworkStore.get(
            dict(query={'user_id': user.id, 'id': network_id})
        )
        if not networks:
            raise web.HTTPNotFound()
        network = networks[0]
        network = yield from NetworkStore.update(
            dict(filter=('id', network.id),
                 update={'status': '0' if action == 'connect' else '2'})
        )
        return web.Response(body=self.serialize(network).encode(),
                            content_type='application/json')
