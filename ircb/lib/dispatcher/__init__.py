import asyncio
import aiozmq.rpc
from collections import defaultdict
import logging

from ircb.config import settings

logger = logging.getLogger('dispatcher')


class Handler(aiozmq.rpc.AttrHandler):

    def __init__(self, signal_listeners):
        self._signal_listeners = signal_listeners

    @aiozmq.rpc.method
    def send(self, signal, data, taskid=None):
        try:
            signals = [signal, '__all__']
            for s in signals:
                for callback in self._signal_listeners.get(s, []):
                    callback(signal, data, taskid)
            logger.debug('SEND: {} {} {}'.format(signal, data, taskid))
        except Exception as e:
            logger.error('SEND ERROR: {} {} {} {}'.format(
                e, signal, data, taskid), exc_info=True)


class Dispatcher(object):

    def __init__(self, role):
        self.role = role
        self._signal_listeners = defaultdict(set)
        self.handler = Handler(self._signal_listeners)
        self.subscriber = self.publisher = None
        asyncio.Task(self.setup_pubsub())

    @asyncio.coroutine
    def setup_pubsub(self):
        self.subscriber = yield from aiozmq.rpc.serve_pubsub(
            self.handler, subscribe='',
            bind=settings.SUBSCRIBER_ENDPOINTS[self.role],
            log_exceptions=True)
        self.publisher = yield from aiozmq.rpc.connect_pubsub(
            connect=self.subscriber_endpoints)

    @property
    def subscriber_endpoints(self):
        return [endpoint for role, endpoint in
                settings.SUBSCRIBER_ENDPOINTS.items()
                if role != self.role]

    def send(self, signal, data, taskid=None):
        asyncio.Task(self._send(signal, data, taskid))

    @asyncio.coroutine
    def _send(self, signal, data, taskid=None):
        logger.debug('PUBLISH from %s: %s' % (self.role, (signal, data, taskid)))
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
