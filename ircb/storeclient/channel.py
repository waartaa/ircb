# -*- coding: utf-8 -*-
from ircb.storeclient.base import BaseStore
from ircb.lib.constants.signals import (STORE_CHANNEL_CREATE,
                                        STORE_CHANNEL_CREATED,
                                        STORE_CHANNEL_GET,
                                        STORE_CHANNEL_GOT,
                                        STORE_CHANNEL_UPDATE,
                                        STORE_CHANNEL_UPDATED,
                                        STORE_CHANNEL_DELETE,
                                        STORE_CHANNEL_DELETED,
                                        STORE_CHANNEL_CREATE_OR_UPDATE)


class ChannelStore(BaseStore):
    CREATE_SIGNAL = STORE_CHANNEL_CREATE
    CREATED_SIGNAL = STORE_CHANNEL_CREATED
    GET_SIGNAL = STORE_CHANNEL_GET
    GOT_SIGNAL = STORE_CHANNEL_GOT
    UPDATE_SIGNAL = STORE_CHANNEL_UPDATE
    UPDATED_SIGNAL = STORE_CHANNEL_UPDATED
    DELETE_SIGNAL = STORE_CHANNEL_DELETE
    DELETED_SIGNAL = STORE_CHANNEL_DELETED
    CREATE_OR_UPDATE_SIGNAL = STORE_CHANNEL_CREATE_OR_UPDATE
