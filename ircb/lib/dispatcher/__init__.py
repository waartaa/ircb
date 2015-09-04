from collections import defaultdict
import logging

logger = logging.getLogger('dispatcher')


class Dispatcher(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._signal_listeners = defaultdict(set)

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

dispatcher = Dispatcher()
