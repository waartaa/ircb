import asyncio
import logging
from connection import Connection

logger = logging.getLogger('network')


class Network(Connection):

    def __init__(self, bouncer_username, network_name, nickname, username,
                 password, register, usermode='0', realname=''):
        self.bouncer_username = bouncer_username
        self.network_name = network_name
        self.nickname = nickname
        self.username = username
        self.password = password
        self.realname = realname
        self.usermode = usermode
        self.dispatch = register(self.bouncer_username, self.network_name,
                                 self)

    def connection_made(self, transport):
        logger.debug('Network connected: %s, %s, %s', self.bouncer_username,
                     self.network_name, self.nickname)
        self.transport = transport
        self.send(
            'USER', self.username or self.bouncer_username, self.usermode, '*',
            ':'.format(self.realname))
        if self.password:
            self.send('PASS', self.password)
        self.send('NICK', self.nickname)

    def data_received(self, data):
        logger.debug('Data received: %s', data.decode())
        self.dispatch(data)
    
