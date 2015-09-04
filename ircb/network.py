import asyncio
import logging
from connection import Connection
from ircb.stores import NetworkMessageStore
from ircb.storeclient import NetworkStore

logger = logging.getLogger('network')


class Network(Connection):

    def __init__(self, bouncer_username, network_id, network_name, nickname,
                 username, password, register, usermode='0', realname=''):
        self.bouncer_username = bouncer_username
        self.id = network_id
        self.name = network_name
        self.nickname = nickname
        self.username = username or self.bouncer_username
        self.password = password
        self.realname = realname or ' '
        self.usermode = usermode
        self.dispatch = register(self.id, self)
        self.message_store = NetworkMessageStore()

    def connection_made(self, transport):
        asyncio.Task(self.handle_connection_made(transport))

    @asyncio.coroutine
    def handle_connection_made(self, transport):
        logger.debug('Network connected: %s, %s, %s', self.bouncer_username,
                     self.name, self.nickname)
        self.transport = transport
        if self.password:
            self.send('PASS', self.password)
        self.send('NICK', self.nickname)
        self.send(
            'USER', self.username, '*', '*',
            ':{}'.format(self.realname))
        yield from NetworkStore.update(
            dict(
                filter=('id', self.id),
                update={
                    'status': '1'
                }
            )
        )

    def connection_lost(self, exc):
        logger.debug('Network disconnected: %s, %s, %s', self.bouncer_username,
                     self.name, self.nickname)
        yield from NetworkStore.update(
            dict(
                filter=('id', self.id),
                update={
                    'status': '3'
                }
            )
        )

    def data_received(self, data):
        logger.debug('Data received: %s', data.decode())
        self.dispatch(data)
        self.message_store.update(self.decode(data))

    def get_joining_messages(self):
        logger.debug('Joining messages: %s', self.message_store.get_all())
        return self.message_store.get_all()

    def send(self, *args):
        super().send(*args)

    def __str__(self):
        return '<NetworkConnection: {user}-{network_name}>'.format(
            user=self.bouncer_username, network_name=self.name)

    def __repr__(self):
        return self.__str__()

