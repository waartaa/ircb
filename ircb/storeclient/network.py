# -*- coding: utf-8 -*-
from ircb.models import Network
from ircb.storeclient.base import BaseStore
from ircb.lib.constants.signals import (STORE_NETWORK_CREATE,
                                        STORE_NETWORK_CREATED,
                                        STORE_NETWORK_GET,
                                        STORE_NETWORK_GOT,
                                        STORE_NETWORK_UPDATE,
                                        STORE_NETWORK_UPDATED)


class NetworkStore(BaseStore):
    CREATE_SIGNAL = STORE_NETWORK_CREATE
    CREATED_SIGNAL = STORE_NETWORK_CREATED
    GET_SIGNAL = STORE_NETWORK_GET
    GOT_SIGNAL = STORE_NETWORK_GOT
    UPDATE_SIGNAL = STORE_NETWORK_UPDATE
    UPDATED_SIGNAL = STORE_NETWORK_UPDATED

    model = Network
