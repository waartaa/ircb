from ircb.lib.constants.signals import (
    STORE_NETWORK_CREATE, STORE_NETWORK_CREATED,
    STORE_NETWORK_UPDATE, STORE_NETWORK_UPDATED,
    STORE_NETWORK_GET, STORE_NETWORK_GOT)
from ircb.models import get_session, User, Network
from ircb.stores.base import BaseStore

session = get_session()


class NetworkStore(BaseStore):
    CREATE_SIGNAL = STORE_NETWORK_CREATE
    CREATED_SIGNAL = STORE_NETWORK_CREATED
    GET_SIGNAL = STORE_NETWORK_GET
    GOT_SIGNAL = STORE_NETWORK_GOT
    UPDATE_SIGNAL = STORE_NETWORK_UPDATE
    UPDATED_SIGNAL = STORE_NETWORK_UPDATED

    @classmethod
    def get(cls, query):
        if isinstance(query, dict):
            qs = session.query(Network)
            for key, value in query.items():
                qs = qs.filter(getattr(Network, key) == value)
            return qs.all()
        elif isinstance(query, tuple):
            key, value = query
            return session.query(Network).filter(
                getattr(Network, key) == value).first()
        else:
            return session.query(Network).get(query)

    @classmethod
    def create(cls, user, name, nickname, hostname, port, realname, username,
               password, usermode):
        user = session.query(User).filter(User.username == user).first()
        if user is None:
            raise
        network = Network(name=name, nickname=nickname, hostname=hostname,
                          port=port, realname=realname, username=username,
                          password=password, usermode=usermode,
                          user_id=user.id)
        session.add(network)
        session.commit()
        return network

    @classmethod
    def update(cls, filter, update={}):
        network = session.query(Network).filter(
            getattr(Network, filter[0]) == filter[1]).one()
        for key, value in update.items():
            setattr(network, key, value)
        session.add(network)
        session.commit()
        return network
