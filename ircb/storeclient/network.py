from ircb.storeclient.base import BaseStore
from ircb.lib.constants.signals import (
    STORE_NETWORK_CREATE, STORE_NETWORK_CREATED)


class NetworkStore(BaseStore):
    CREATE_SIGNAL = STORE_NETWORK_CREATE
    CREATED_SIGNAL = STORE_NETWORK_CREATED
