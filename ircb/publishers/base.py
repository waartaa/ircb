# -*- coding: utf-8 -*-

import asyncio
import logging

logger = logging.getLogger('publisher')


class BasePublisher(object):

    store = None
    name = None

    def __init__(self, *args, **kwargs):
        self.fetched = False
        self.callbacks = {
            'update': set(),
            'create': set(),
            'fetch': set()
        }

    @property
    def id(self):
        raise NotImplementedError

    def run(self):
        self.store.on('create', self.handle_create, raw=True)
        self.store.on('update', self.handle_update, raw=True)
        self.store.on('delete', self.handle_delete, raw=True)
        asyncio.Task(self._fetch())

    def on(self, event, callback):
        """
        Register callbacks for an event.
        """
        callbacks = self.callbacks.get(event)
        if callbacks is not None:
            callbacks.add(callback)

    @asyncio.coroutine
    def _fetch(self):
        results = yield from self.fetch()
        self.handle_fetch(results)

    def fetch(self):
        return []

    def handle_fetch(self, results):
        self.normalize(results)
        for callback in self.callbacks.get('fetch') or set():
            callback(results)
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
        if self.skip_update(data):
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
        if self.skip_create(data):
            logger.debug('skipping create data: {}'.format(data))
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

    def handle_delete(self, data):
        pass

    def skip_create(self, data):
        return False

    def skip_update(self, data):
        return False
