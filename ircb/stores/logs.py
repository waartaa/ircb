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
    def get(cls, query):
        pass

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
