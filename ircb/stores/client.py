# -*- coding: utf-8 -*-
from ircb.models import Client, Network, get_session
from ircb.lib.constants.signals import (STORE_CLIENT_CREATE,
                                        STORE_CLIENT_CREATED,
                                        STORE_CLIENT_DELETE,
                                        STORE_CLIENT_DELETED)
from ircb.stores.base import BaseStore

session = get_session()


class ClientStore(BaseStore):
    CREATE_SIGNAL = STORE_CLIENT_CREATE
    CREATED_SIGNAL = STORE_CLIENT_CREATED
    DELETE_SIGNAL = STORE_CLIENT_DELETE
    DELETED_SIGNAL = STORE_CLIENT_DELETED

    @classmethod
    def create(cls, socket, network_id, user_id):
        network = session.query(Network).filter(
            Network.id == network_id, Network.user_id == user_id).one()
        client = Client(
            socket=socket, network_id=network_id, user_id=user_id)
        session.add(client)
        session.commit()
        return client

    @classmethod
    def delete(cls, id):
        client = session.query(Client).get(id)
        session.delete(client)
        session.commit()
