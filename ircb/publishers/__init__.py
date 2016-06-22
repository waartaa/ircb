# -*- coding: utf-8 -*-
import asyncio
import logging

from ircb.storeclient import MessageLogStore
from collections import deque

logger = logging.getLogger('publisher')


class MessageLogPublisher(object):
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

    def __init__(self, hostname, roomname, user_id, limit=30):
        self.hostname = hostname
        self.roomname = roomname
        self.user_id = user_id
        self.limit = limit
        self.results = deque(maxlen=self.limit)
        self.index = {}
        self.fields = []
        self.fetched = False
        MessageLogStore.on('create', self.handle_create,
                           raw=True)
        asyncio.Task(self.fetch())

    @property
    def signature(self):
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
        logger.debug('fetched', results)
        self.normalize(results)
        self.fetched = True

    def normalize(self, results):
        for result in results:
            self.index[result['id']] = result
            self.results.append(result['id'])
        logger.debug('normalized index: %s', self.index)
        logger.debug('normalized results: %s', self.results)

    def handle_update(self, data):
        """
        Check if an update operation on a row of message_logs table
        affects our data, and update it if needed.
        """
        if self.skip(data):
            logger.debug('skipping update data', data)
            return
        if data['id'] in self.index:
            self.index[data['id']] = data

    def handle_create(self, data):
        """
        Check if an insert operation in message_logs table affects our
        results. If yes, append it to results.
        """
        if self.skip(data):
            return
        if self.results and data['timestamp'] < self.index[
                self.results[-1]]['timestamp']:
            return
        if not self.fetched:
            return

        logger.debug('skip created data', data)
        self.index[data['id']] = data
        self.results.append(data['id'])
        logger.debug('updated results: %s, %s', self.results, self.index)

    def skip(self, data):
        """
        We'll skip updating our results if the insert/update event
        is not relevant to us.
        """
        return data['user_id'] != self.user_id or \
            data['hostname'] != self.hostname or \
            data['roomname'] != self.roomname


if __name__ == '__main__':
    import sys
    from ircb.storeclient import initialize
    from ircb.utils.config import load_config
    load_config()
    initialize()
    try:
        hostname = sys.argv[1]
        roomname = sys.argv[2]
        user_id = sys.argv[3]
    except:
        print("Usage: __init__.py '<hostname>' '<roomname>' '<user_id>'")
        sys.exit(1)
    MessageLogPublisher(hostname, roomname, int(user_id))
    loop = asyncio.get_event_loop()
    loop.run_forever()
