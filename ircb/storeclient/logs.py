# -*- coding: utf-8 -*-
from ircb.models import MessageLog, ActivityLog
from ircb.storeclient.base import BaseStore
from ircb.lib.constants.signals import (STORE_MESSAGELOG_CREATE,
                                        STORE_MESSAGELOG_CREATED,
                                        STORE_MESSAGELOG_GET,
                                        STORE_MESSAGELOG_GOT,
                                        STORE_ACTIVITYLOG_CREATE,
                                        STORE_ACTIVITYLOG_CREATED,
                                        STORE_ACTIVITYLOG_GET,
                                        STORE_ACTIVITYLOG_GOT)


class MessageLogStore(BaseStore):
    CREATE_SIGNAL = STORE_MESSAGELOG_CREATE
    CREATED_SIGNAL = STORE_MESSAGELOG_CREATED
    GET_SIGNAL = STORE_MESSAGELOG_GET
    GOT_SIGNAL = STORE_MESSAGELOG_GOT

    model = MessageLog


class ActivityLogStore(BaseStore):
    CREATE_SIGNAL = STORE_ACTIVITYLOG_CREATE
    CREATED_SIGNAL = STORE_ACTIVITYLOG_CREATED
    GET_SIGNAL = STORE_ACTIVITYLOG_GET
    GOT_SIGNAL = STORE_ACTIVITYLOG_GOT

    model = ActivityLog
