from ircb.lib.dispatcher import dispatcher
from ircb.lib.constants.signals import (
    STORE_NETWORK_CREATE, STORE_NETWORK_CREATED,
    STORE_NETWORK_UPDATE, STORE_NETWORK_UPDATED)
from ircb.models import get_session, User, Network
import logging

session = get_session()
logger = logging.getLogger('stores')


class NetworkStore(object):

    @classmethod
    def initialize(cls):
        dispatcher.register(cls.create, STORE_NETWORK_CREATE)
        dispatcher.register(cls.update, STORE_NETWORK_UPDATE)

    @classmethod
    def create(cls, signal, data, taskid=None):
        network = cls._create(**(data or {}))
        logger.debug('NetworkStore created: {} {} {}'.format(
            signal, data, taskid))
        dispatcher.send(
            signal=STORE_NETWORK_CREATED,
            data=network,
            taskid=taskid)

    @classmethod
    def update(cls, signal, data, taskid=None):
        network = cls._update(**(data or {}))
        logger.debug('NetworkStore updated: {} {} {}'.format(
            signal, data, taskid))
        dispatcher.send(
            signal=STORE_NETWORK_UPDATED,
            data=network,
            taskid=taskid
        )

    @classmethod
    def _create(cls, user, name, nickname, hostname, port, realname, username,
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
    def _update(cls, filter, update={}):
        network = session.query(Network).filter(
            getattr(Network, filter[0]) == filter[1]).one()
        for key, value in update.items():
            setattr(network, key, value)
        session.add(network)
        session.commit()
        return network
