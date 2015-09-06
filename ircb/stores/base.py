# -*- coding: utf-8 -*-
from ircb.lib.dispatcher import dispatcher
import logging

logger = logging.getLogger('stores')


class BaseStore(object):
    GET_SIGNAL = None
    GOT_SIGNAL = None
    CREATE_SIGNAL = None
    CREATED_SIGNAL = None
    UPDATE_SIGNAL = None
    UPDATED_SIGNAL = None
    DELETE_SIGNAL = None
    DELETED_SIGNAL = None

    @classmethod
    def initialize(cls):
        signal_callback_map = dict(
            GET_SIGNAL=cls.do_get,
            CREATE_SIGNAL=cls.do_create,
            UPDATE_SIGNAL=cls.do_update,
            DELETE_SIGNAL=cls.do_delete
        )
        for signal, callback in signal_callback_map.items():
            if getattr(cls, signal, None):
                dispatcher.register(callback, getattr(cls, signal))

    @classmethod
    def do_get(cls, signal, data, taskid=None):
        logger.debug(
            '{} GET: {} {} {}'.format(
                cls.__name__, signal, data, taskid)
        )
        result = cls.get(**(data or {}))
        logger.debug(
            '{} GOT: {}'.format(
                cls.__name__, result)
        )
        dispatcher.send(
            signal=cls.GOT_SIGNAL,
            data=result,
            taskid=taskid)

    @classmethod
    def do_create(cls, signal, data, taskid=None):
        logger.debug(
            '{} CREATE: {} {} {}'.format(
                cls.__name__, signal, data, taskid)
        )
        result = cls.create(**(data or {}))
        logger.debug(
            '{} CREATED: {}'.format(
                cls.__name__, result)
        )
        dispatcher.send(
            signal=cls.CREATED_SIGNAL,
            data=result,
            taskid=taskid)

    @classmethod
    def do_update(cls, signal, data, taskid=None):
        logger.debug(
            '{} UPDATE: {} {} {}'.format(
                cls.__name__, signal, data, taskid)
        )
        result = cls.update(**(data or {}))
        logger.debug(
            '{} UPDATED: {}'.format(
                cls.__name__, result)
        )
        dispatcher.send(
            signal=cls.UPDATED_SIGNAL,
            data=result,
            taskid=taskid)

    @classmethod
    def do_delete(cls, signal, data, taskid=None):
        logger.debug(
            '{} DELETE: {} {} {}'.format(
                cls.__name__, signal, data, taskid)
        )
        result = cls.delete(**(data or {}))
        logger.debug(
            '{} DELETED: {}'.format(
                cls.__name__, result)
        )
        dispatcher.send(
            signal=cls.DELETED_SIGNAL,
            data=result,
            taskid=taskid)

    @classmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError
