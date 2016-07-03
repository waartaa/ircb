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
        self.results_count = 0
        self.index = {}
        self.fields = []
        self.fetched = False
        self.callbacks = {
            'update': set(),
            'create': set()
        }
        MessageLogStore.on('create', self.handle_create,
                           raw=True)
        asyncio.Task(self.fetch())

    def on(self, event, callback):
        """
        Register callbacks for an event.
        """
        callbacks = self.callbacks.get(event)
        if callbacks:
            callbacks.add(callback)

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
            self.results_count += 1
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

        for callback in self.callbacks.get('update') or set():
            callback(data)

    def handle_create(self, data):
        """
        Check if an insert operation in message_logs table affects our
        results. If yes, append it to results.
        """
        skip = False
        if self.skip(data):
            skip = skip or True
        if self.results and data['timestamp'] < self.index[
                self.results[-1]]['timestamp']:
            skip = skip or True
        if not self.fetched:
            skip = skip or True
        if skip:
            logger.debug('skip created data', data)
            return

        if self.results_count == self.limit:
            logger.debug('Removing id: %s from index', self.results[0])
            self.index.pop(self.results[0], None)
        else:
            self.results_count += 1

        self.index[data['id']] = data
        self.results.append(data['id'])
        logger.debug('updated results: %s, %s', self.results, self.index)
        for callback in self.callbacks.get('create') or set():
            callback(data)

    def skip(self, data):
        """
        We'll skip updating our results if the insert/update event
        is not relevant to us.
        """
        return data['user_id'] != self.user_id or \
            data['roomname'] != self.roomname or \
            data['hostname'] != self.hostname


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
