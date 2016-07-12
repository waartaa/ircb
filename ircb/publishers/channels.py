# -*- coding: utf-8 -*-

from ircb.storeclient import ChannelStore

from .base import BasePublisher


class ChannelPublisher(BasePublisher):

    name = 'channels'
    store = ChannelStore

    def __init__(self, user_id, network_id=None):
        self.user_id = user_id
        self.network_id = network_id
        super().__init__()

    def fetch(self):
        filter = {
            'user_id': self.user_id
        }
        if self.network_id:
            filter['network_id'] = self.network_id
        results = yield from ChannelStore.get({
            'filter': filter
        }, raw=True)
        return results

    def skip_create(self, data):
        return self.skip_update(data)

    def skip_update(self, data):
        return data['user_id'] != self.user_id or \
            (data['network_id'] != self.network_id
             if self.network_id else False)
