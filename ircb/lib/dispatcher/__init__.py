# -*- coding: utf-8 -*-
import asyncio
import aiozmq.rpc
import aioredis
import logging

from collections import defaultdict

from ircb.config import settings
from ircb.lib.redis import redis

logger = logging.getLogger('dispatcher')


class Handler(aiozmq.rpc.AttrHandler):

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    @aiozmq.rpc.method
    def send(self, signal, data, taskid=None):
        try:
            signals = [signal, '__all__']
            for s in signals:
                for callback in self._dispatcher._signal_listeners.get(s, []):
                    callback(signal, data, taskid)
            logger.debug('SEND: {} {} {}'.format(signal, data, taskid))
        except Exception as e:
            logger.error('SEND ERROR: {} {} {} {}'.format(
                e, signal, data, taskid), exc_info=True)


class Dispatcher(object):
    STORE_KEY = settings.REDIS_KEYS['STORE']
    STORE_CLIENTS_KEY = settings.REDIS_KEYS['STORE_CLIENTS']

    def __init__(self, role, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.role = role
        self._signal_listeners = defaultdict(set)
        self.handler = Handler(self)
        self.subscriber = self.publisher = None
        self.lock = asyncio.Lock()
        self.queue = asyncio.Queue(loop=self.loop)
        asyncio.Task(self.lock.acquire())
        asyncio.Task(self.setup_pubsub())

    @asyncio.coroutine
    def process_queue(self):
        while True:
            while self.lock.locked():
                yield from asyncio.sleep(0.01)
                continue
            try:
                (signal, data, taskid) = self.queue.get_nowait()
                yield from self._send(signal, data, taskid)
            except asyncio.QueueEmpty:
                break

    @asyncio.coroutine
    def watch_store(self, key, ch):
        """
        Watch store key in redis for change.

        Args:
            key (str): Name of redis key for store
            ch: aioredis channel obj
        """
        while (yield from ch.wait_message()):
            msg = yield from ch.get()
            endpoint = yield from redis.get(key)
            self.publisher.transport.connect(endpoint.decode())
            if self.publisher.transport.connections():
                if self.lock.locked():
                    self.lock.release()

    @asyncio.coroutine
    def watch_storeclients(self, key, ch):
        """
        Watch store_clients key in redis for change.

        Args:
            key (str): Name of redis key for store clients
            ch (obj): aioredis channel obj
        """
        while (yield from ch.wait_message()):
            msg = yield from ch.get()
            endpoints = yield from redis.smembers(key)
            for endpoint in endpoints:
                self.publisher.transport.connect(endpoint.decode())
            if self.publisher.transport.connections():
                if self.lock.locked():
                    self.lock.release()

    @asyncio.coroutine
    def setup_pubsub(self):
        # Initialize redis connection
        yield from redis.init()

        bind_addr = 'tcp://{host}:*'.format(host=settings.INTERNAL_HOST)
        self.subscriber = yield from aiozmq.rpc.serve_pubsub(
            self.handler, subscribe='',
            bind=bind_addr,
            log_exceptions=True)
        subscriber_addr = list(self.subscriber.transport.bindings())[0]
        self.publisher = yield from aiozmq.rpc.connect_pubsub()

        if self.role == 'stores':
            # Register current store endpoint
            yield from redis.set(settings.REDIS_KEYS['STORE'],
                                 subscriber_addr)

            # Set watcher for store clients to handle new store clients
            yield from redis.watch(self.STORE_CLIENTS_KEY, self.watch_storeclients)

            # Setup initial connections to available store clients
            store_client_endpoints = yield from redis.smembers(
                self.STORE_CLIENTS_KEY)
            for endpoint in store_client_endpoints:
                self.publisher.transport.connect(endpoint.decode())
        else:
            # Register current store client endpoint to pool
            yield from redis.sadd(settings.REDIS_KEYS['STORE_CLIENTS'],
                                  subscriber_addr)

            # Enable watcher to track store endpoints
            yield from redis.watch(self.STORE_KEY, self.watch_store)

            # Setup initial connection to store
            store_endpoint = yield from redis.get(
                settings.REDIS_KEYS['STORE'])
            self.publisher.transport.connect(store_endpoint.decode())
        if self.publisher.transport.connections():
            self.lock.release()

    def send(self, signal, data, taskid=None):
        asyncio.Task(self.enqueue((signal, data, taskid)))

    @asyncio.coroutine
    def enqueue(self, data):
        empty = self.queue.empty()
        yield from self.queue.put(data)
        if empty:
            asyncio.Task(self.process_queue())

    @asyncio.coroutine
    def _send(self, signal, data, taskid=None):
        logger.debug('PUBLISH from %s: %s' %
                     (self.role, (signal, data, taskid)))
        yield from self.publisher.publish(signal).send(signal, data, taskid)

    def register(self, callback, signal=None):
        try:
            signal = signal or '__all__'
            if callback not in self._signal_listeners.get('__all__', []):
                callbacks = self._signal_listeners[signal]
                callbacks.add(callback)
            logger.debug('REGISTER: {} {}'.format(callback, signal))
        except Exception as e:
            logger.error('REGISTER ERROR: {} {} {}'.format(
                e, callback, signal), exc_info=True)

    def run_forever(self):
        logger.info('Running stores...')
        self.loop.run_forever()
