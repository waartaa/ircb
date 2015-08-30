from collections import defaultdict


class Dispatcher(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._signal_listeners = defaultdict(set)

    def send(self, signal, data, taskid=None):
        signals = [signal, '__all__']
        for s in signals:
            for callback in self._signal_listeners.get(s, []):
                callback(signal, data, taskid)

    def register(self, callback, signal=None):
        signal = signal or '__all__'
        if callback not in self._signal_listeners.get('__all__', []):
            callbacks = self._signal_listeners[signal]
            callbacks.add(callback)

dispatcher = Dispatcher()
