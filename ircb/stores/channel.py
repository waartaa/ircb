# -*- coding: utf-8 -*-
from ircb.models import get_session, Network, Channel
from ircb.lib.constants.signals import (STORE_CHANNEL_CREATE,
                                        STORE_CHANNEL_CREATED,
                                        STORE_CHANNEL_GET,
                                        STORE_CHANNEL_GOT,
                                        STORE_CHANNEL_UPDATE,
                                        STORE_CHANNEL_UPDATED,
                                        STORE_CHANNEL_DELETE,
                                        STORE_CHANNEL_DELETED)
from ircb.stores.base import BaseStore

session = get_session()


class ChannelStore(BaseStore):
    CREATE_SIGNAL = STORE_CHANNEL_CREATE
    CREATED_SIGNAL = STORE_CHANNEL_CREATED
    GET_SIGNAL = STORE_CHANNEL_GET
    GOT_SIGNAL = STORE_CHANNEL_GOT
    UPDATE_SIGNAL = STORE_CHANNEL_UPDATE
    UPDATED_SIGNAL = STORE_CHANNEL_UPDATED
    DELETE_SIGNAL = STORE_CHANNEL_DELETE
    DELETED_SIGNAL = STORE_CHANNEL_DELETED

    @classmethod
    def get(cls, id):
        return session.query(Channel).get(id)

    @classmethod
    def create(cls, channel, network_id, password="", status=0):
        network = session.query(Network).get(network_id)
        channel = Channel(name=channel, network_id=network_id,
                          password=password, status=status,
                          user_id=network.user_id)
        session.add(channel)
        session.commit()

    @classmethod
    def update(cls, filter, update={}):
        channel = session.query(Channel).filter(
            getattr(Channel, filter[0]) == filter[1]).one()
        for key, value in update.items():
            setattr(channel, key, value)
        session.add(channel)
        session.commit()
        return channel

    @classmethod
    def delete(cls, id):
        channel = session.query(Channel).get(id)
        session.delete(channel)
        session.commit()
