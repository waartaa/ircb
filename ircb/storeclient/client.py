from ircb.models import Client
from ircb.storeclient.base import BaseStore
from ircb.lib.constants.signals import (STORE_CLIENT_CREATE,
                                        STORE_CLIENT_CREATED,
                                        STORE_CLIENT_DELETE,
                                        STORE_CLIENT_DELETED)


class ClientStore(BaseStore):
    CREATE_SIGNAL = STORE_CLIENT_CREATE
    CREATED_SIGNAL = STORE_CLIENT_CREATED
    DELETE_SIGNAL = STORE_CLIENT_DELETE
    DELETED_SIGNAL = STORE_CLIENT_DELETED

    model = Client
