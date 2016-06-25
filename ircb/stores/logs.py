# -*- coding: utf-8 -*-
import datetime
from ircb.lib.constants.signals import (STORE_MESSAGELOG_CREATE,
                                        STORE_MESSAGELOG_CREATED,
                                        STORE_MESSAGELOG_GET,
                                        STORE_MESSAGELOG_GOT,
                                        STORE_ACTIVITYLOG_CREATE,
                                        STORE_ACTIVITYLOG_CREATED,
                                        STORE_ACTIVITYLOG_GET,
                                        STORE_ACTIVITYLOG_GOT)
from ircb.models import get_session, MessageLog, ActivityLog
from ircb.stores.base import BaseStore

session = get_session()


class MessageLogStore(BaseStore):
    GET_SIGNAL = STORE_MESSAGELOG_GET
    GOT_SIGNAL = STORE_MESSAGELOG_GOT
    CREATE_SIGNAL = STORE_MESSAGELOG_CREATE
    CREATED_SIGNAL = STORE_MESSAGELOG_CREATED

    @classmethod
    def create(cls, hostname, roomname, message, event, timestamp,
               mask, user_id, from_nickname, from_user_id=None):
        log = MessageLog(
            hostname=hostname, roomname=roomname, message=message,
            event=event, timestamp=datetime.datetime.fromtimestamp(timestamp),
            mask=mask, user_id=user_id, from_nickname=from_nickname,
            from_user_id=from_user_id)
        session.add(log)
        session.commit()
        return log

    @classmethod
    def get(cls, filter=None, order_by=None, limit=30, sort='timestamp'):
        qs = session.query(MessageLog.id)
        if filter:
            for key, value in filter.items():
                qs = qs.filter(getattr(MessageLog, key) == value)

        if order_by:
            for item in order_by:
                if item.startswith('-'):
                    qs = qs.order_by(getattr(MessageLog, item[1:]).desc())
                else:
                    qs = qs.order_by(getattr(MessageLog, item))

        qs = qs.limit(limit)
        return session.query(MessageLog).\
            filter(MessageLog.id.in_(qs.subquery())).\
            order_by(MessageLog.timestamp).all()


class ActivityLogStore(BaseStore):
    CREATE_SIGNAL = STORE_ACTIVITYLOG_CREATE
    CREATED_SIGNAL = STORE_ACTIVITYLOG_CREATED
    GET_SIGNAL = STORE_ACTIVITYLOG_GET
    GOT_SIGNAL = STORE_ACTIVITYLOG_GOT

    @classmethod
    def get(cls):
        pass

    @classmethod
    def create(cls, hostname, roomname, message, event, timestamp,
               mask, user_id):
        log = ActivityLog(
            hostname=hostname, roomname=roomname, message=message,
            event=event, timestamp=datetime.datetime.fromtimestamp(timestamp),
            mask=mask, user_id=user_id)
        session.add(log)
        session.commit()
        return log
