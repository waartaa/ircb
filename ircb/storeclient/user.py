from ircb.storeclient.base import BaseStore
from ircb.lib.constants.signals import (
    STORE_USER_CREATE, STORE_USER_CREATED,
    STORE_USER_GET, STORE_USER_GOT)


class UserStore(BaseStore):
    CREATE_SIGNAL = STORE_USER_CREATE
    CREATED_SIGNAL = STORE_USER_CREATED
    GET_SIGNAL = STORE_USER_GET
    GOT_SIGNAL = STORE_USER_GOT
