# -*- coding: utf-8 -*-
import logging

from ircb.lib.dispatcher import Dispatcher
from ircb.models.lib import Base

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
    CREATE_OR_UPDATE = None
    CREATE_OR_UPDATE_ERROR = None

    @classmethod
    def initialize(cls):
        signal_callback_map = dict(
            GET_SIGNAL=cls.do_get,
            CREATE_SIGNAL=cls.do_create,
            UPDATE_SIGNAL=cls.do_update,
            DELETE_SIGNAL=cls.do_delete,
            CREATE_OR_UPDATE=cls.do_create_or_update
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
            data=cls.serialize(result),
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
            data=cls.serialize(result),
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
            data=cls.serialize(result),
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
            data=cls.serialize(result),
            taskid=taskid)

    @classmethod
    def do_create_or_update(cls, signal, data, taskid=None):
        logger.debug(
            '{} CREATE_OR_UPDATE: {} {} {}'.format(
                cls.__name__, signal, data, taskid)
        )
        result, action = cls.create_or_update(**(data or {}))
        if action == 'create':
            action_verb = 'CREATED'
            resp_signal = cls.CREATED_SIGNAL
        elif action == 'update':
            action_verb = 'UPDATED'
            resp_signal = cls.UPDATED_SIGNAL
        else:
            action_verb = 'CREATE_OR_UPDATE_FAILED'
            resp_signal = cls.CREATE_OR_UPDATE_ERROR
        logger.debug(
            '{} {}: {}'.format(
                cls.__name__, action_verb, result)
        )
        dispatcher.send(
            signal=resp_signal,
            data=cls.serialize(result),
            taskid=taskid)

    @classmethod
    def serialize(cls, data):
        if isinstance(data, Base):
            return cls.serialize_row(data)
        elif isinstance(data, list):
            return cls.serialize_rows(data)

    @classmethod
    def serialize_rows(cls, rows):
        return [cls.serialize_row(row) for row in rows]

    @classmethod
    def serialize_row(cls, row):
        return row.to_dict()

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

    @classmethod
    def create_or_update(self, *args, **kwargs):
        raise NotImplementedError


def init():
    global dispatcher
    dispatcher = Dispatcher(role='stores')

dispatcher = None
