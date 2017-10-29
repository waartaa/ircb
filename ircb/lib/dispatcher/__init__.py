# -*- coding: utf-8 -*-
import asyncio
import aiozmq.rpc
import aioredis
import logging
import sys

from collections import defaultdict

from ircb.config import settings

logger = logging.getLogger('dispatcher')


class Handler(aiozmq.rpc.AttrHandler):

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher
        # lock for registering subscriber
        self._lock = asyncio.Lock()

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

    @asyncio.coroutine
    @aiozmq.rpc.method
    def register_sub(self, subscriber_addr, key):
        yield from self._lock.acquire()
        try:
            connections = self._dispatcher.publisher.transport.connections()
            if subscriber_addr in connections:
                self._lock.release()
                return
            self._dispatcher.publisher.transport.connect(subscriber_addr)
            try:
                logger.debug('Connecting to redis at {}:{}...'.format(
                    settings.REDIS_HOST, settings.REDIS_PORT))
                redis = yield from aioredis.create_redis(
                    (settings.REDIS_HOST, settings.REDIS_PORT),
                    timeout=5
                )
                logger.debug('Connected to redis')
            except (IOError, ConnectionRefusedError) as e:
                logger.error('Failed to connect to redis at {}:{}'.format(
                    settings.REDIS_HOST, settings.REDIS_PORT))
                logger.error('Exiting...')
                sys.exit(1)
            yield from redis.set(key, 1)
            redis.close()
        finally:
            if self._lock.locked():
                self._lock.release()


class Dispatcher(object):

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
    def setup_pubsub(self):
        try:
            logger.debug('Connecting to redis at {}:{}...'.format(
                settings.REDIS_HOST, settings.REDIS_PORT))
            redis = yield from aioredis.create_redis(
                (settings.REDIS_HOST, settings.REDIS_PORT),
                timeout=5
            )
            logger.debug('Connected to redis')
        except (IOError, ConnectionRefusedError) as e:
            logger.error('Failed to connect to redis at {}:{}'.format(
                settings.REDIS_HOST, settings.REDIS_PORT))
            logger.error('Exiting...')
            sys.exit(1)
        if self.role == 'stores':
            bind_addr = settings.SUBSCRIBER_ENDPOINTS[self.role]
        else:
            bind_addr = 'tcp://{host}:*'.format(host=settings.INTERNAL_HOST)
        self.subscriber = yield from aiozmq.rpc.serve_pubsub(
            self.handler, subscribe='',
            bind=bind_addr,
            log_exceptions=True)
        subscriber_addr = list(self.subscriber.transport.bindings())[0]
        self.publisher = yield from aiozmq.rpc.connect_pubsub()
        if self.role == 'storeclient':
            self.publisher.transport.connect(
                settings.SUBSCRIBER_ENDPOINTS['stores'])
            _key = 'SUBSCRIBER_REGISTERED_{}'.format(subscriber_addr)
            ret = 0
            yield from redis.set(_key, ret)
            while ret != b'1':
                yield from self.publisher.publish(
                    'register_sub'
                ).register_sub(
                    subscriber_addr, _key
                )
                ret = yield from redis.get(_key)
                yield from asyncio.sleep(0.01)
        self.lock.release()
        redis.close()
        if self.role == 'stores':
            logger.info('Running {role} at {addr}...'.format(
                role=self.role, addr=bind_addr))

    @property
    def subscriber_endpoints(self):
        return [endpoint for role, endpoint in
                settings.SUBSCRIBER_ENDPOINTS.items()
                if role != self.role]

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
        self.loop.run_forever()
