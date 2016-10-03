# -*- coding: utf-8 -*-
import asyncio
import logging

from ircb.storeclient import MessageLogStore
from collections import deque

from .base import BasePublisher

logger = logging.getLogger('publisher')


class MessageLogPublisher(BasePublisher):
    """
    Publish latest logs in a room in realtime.

    It fetches latest chat logs for a room from the store, initially.
    Then, it keeps on listening to the store for WRITE events on
    MessageLog model and keeps the record of latest chat logs fetched
    always updated.

    This can be used to push latest chat logs in a room to a client
    in realtime.
    """
    name = 'latest_message_logs'
    store = MessageLogStore

    def __init__(self, hostname, roomname, user_id, limit=30):
        self.limit = limit
        self.hostname = hostname
        self.roomname = roomname
        self.user_id = user_id
        super().__init__()

    @property
    def id(self):
        return '{name}::{roomname}::{user_id}::{limit}'.format(
            name=self.name, roomname=self.roomname,
            user_id=self.user_id, limit=self.limit)

    def fetch(self):
        """
        Fetch initial latest chat logs for a room.
        """
        results = yield from MessageLogStore.get({
            'filter': {
                'hostname': self.hostname,
                'roomname': self.roomname,
                'user_id': self.user_id
            },
            'order_by': ('-timestamp',),
            'limit': self.limit,
            # 'fields': self.fields,
            'sort': 'timestamp'
        }, raw=True)
        logger.debug('fetched: %s', results)
        return results

    def skip_create(self, data):
        skip = False
        if self.skip_update(data):
            skip = skip or True
        if self.results and data['timestamp'] < self.index[
                self.results[-1]]['timestamp']:
            skip = skip or True
        if not self.fetched:
            skip = skip or True
        return skip

    def skip_update(self, data):
        """
        We'll skip updating our results if the insert/update event
        is not relevant to us.
        """
        return data['user_id'] != self.user_id or \
            data['roomname'] != self.roomname or \
            data['hostname'] != self.hostname
