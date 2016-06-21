# -*- coding: utf-8 -*-

from storeclient import MessageLogStore
from collections import deque


class MessageLogPublisher(object):
    name = 'latest_message_logs'

    def __init__(self, roomname, user_id, limit=30):
        self.roomname = roomname
        self.user_id = user_id
        self.limit = limit
        self.logs = deque(maxlen=self.limit)
        self.index = {}
        MessageLogStore.on_update(self.handle_update)
        MessageLogStore.on_delete(self.handle_delete)
        MessageLogStore.on_create(self.handle_create)

    @property
    def signature(self):
        return '{name}::{roomname}::{user_id}::{limit}'.format(
            name=self.name, roomname=self.roomname,
            user_id=self.user_id, limit=self.limit)

    def fetch(self):
        results = MessageLogStore.get({
            'filter': {},
            'order_by': '',
            'limit': self.n
        })
        self.normalize(results)

    def normalize(self, results):
        for result in results:
            self.index[result.id] = result
            self.logs.append(result.id)

    def handle_update(self):
        pass

    def handle_create(self):
        pass

    def handle_delete(self):
        pass
