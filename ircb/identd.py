# -*- coding: utf-8 -*-
import asyncio
import logging

from ircb.storeclient import NetworkStore, UserStore
from ircb.storeclient import initialize as sc_initialize
from ircb.connection import Connection
from ircb.config import settings

logger = logging.getLogger('identd')


class IdentdServerProtocol(Connection):
    def connection_made(self, transport):
        logger.debug('New client connection received')
        self.transport = transport

    def data_received(self, data):
        asyncio.Task(self.handle_received_data(self.decode(data)))

    @asyncio.coroutine
    def handle_received_data(self, data):
        logger.debug('RECV: {}'.format(data))
        lport, rport = [_.strip() for _ in data.split(',')]

        networks = yield from NetworkStore.get({
            'query': {'lport': lport, 'rport': rport}
        })
        network = networks[0]
        user = yield from UserStore.get({
            'query': network.user_id
        })
        rpl_msg = '{lport}, {rport} : USERID : UNIX : {username}'.format(
            lport=lport, rport=rport, username=user.username)
        logger.debug('RPL: {}'.format(rpl_msg))
        self.send(rpl_mgs)


class IdentdServer(object):

    def __init__(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

    def create(self, host, port):
        coro = self.loop.create_server(IdentdServerProtocol,
                                       host,
                                       port)
        logger.info('Listening on {}:{}'.format(host, port))
        return self.loop.run_until_complete(coro)

    def start(self, host, port):
        server = self.create(host, port)
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        server.close()
        self.loop.run_until_complete(server.wait_closed())


def runserver(host='0.0.0.0', port=113):
    logging.config.dictConfig(settings.LOGGING_CONF)
    sc_initialize()
    identd_server = IdentdServer()
    identd_server.start(host, port)

if __name__ == '__main__':
    runserver()
