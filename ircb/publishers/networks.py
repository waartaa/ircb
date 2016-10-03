# -*- coding: utf-8 -*-

from ircb.storeclient import NetworkStore

from .base import BasePublisher


class NetworkPublisher(BasePublisher):

    name = 'networks'
    store = NetworkStore

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    @property
    def id(self):
        return '{name}::{user_id}'.format(
            name=self.name, user_id=self.user_id)

    def fetch(self):
        results = yield from NetworkStore.get({
            'query': {
                'user_id': self.user_id
            }
        }, raw=True)
        return results

    def skip_create(self, data):
        return self.skip_update(data)

    def skip_update(self, data):
        return data['user_id'] != self.user_id
