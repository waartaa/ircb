from ircb.lib.dispatcher import dispatcher
from ircb.lib.constants.signals import (
    STORE_NETWORK_CREATE, STORE_NETWORK_CREATED)
from ircb.models import get_session, User, Network

session = get_session()


class NetworkStore(object):

    @classmethod
    def initialize(cls):
        dispatcher.register(cls.create, STORE_NETWORK_CREATE)

    @classmethod
    def create(cls, signal, data, taskid=None):
        network = cls._create(**(data or {}))
        dispatcher.send(
            signal=STORE_NETWORK_CREATED,
            data=network,
            taskid=taskid)

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
