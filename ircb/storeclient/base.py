import asyncio
from uuid import uuid1

from ircb.lib.dispatcher import dispatcher


class BaseStore(object):
    CREATE_SIGNAL = None
    CREATED_SIGNAL = None
    UPDATE_SIGNAL = None
    UPDATED_SIGNAL = None
    DELETE_SIGNAL = None
    DELETED_SIGNAL = None

    @classmethod
    def create(cls, data, async=False, timeout=10):
        return cls._create(data, async)

    @classmethod
    def update(cls, id, data):
        raise NotImplementedError

    @classmethod
    def delete(cls, id):
        raise NotImplementedError

    @classmethod
    def _create(cls, data, async=False):
        task_id = cls.get_task_id(data)
        fut = asyncio.Future()

        def callback(signal, data, taskid=None):
            if taskid == task_id:
                fut.set_result(data)

        dispatcher.register(callback, signal=cls.CREATED_SIGNAL)
        dispatcher.send(cls.CREATE_SIGNAL, data, taskid=task_id)

        result = yield from fut
        return result

    @classmethod
    def get_task_id(self, data):
        return str(uuid1())
