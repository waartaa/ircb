# -*- coding: utf-8 -*-
import asyncio
import logging

import ircb.stores
from ircb.storeclient import NetworkStore

logger = logging.getLogger('identd')

"""
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '0.0.0.0'
port = 8001
s.bind((host, port))
s.listen(5)

while True:
    c, addr = s.accept()
    data = c.recv(4096)

    lport, rport = [_.strip() for _ in data.split(',')]

    result = yield from NetworkStore.get({'query':{'lport': lport,
                                                   'rport': rport}})
    print(result)
"""


class IdentdServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        print('New client connection received')
        self.transport = transport

    def data_received(self, data):
        print(data)


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
    ircb.stores.initialize()
    identd_server = IdentdServer()
    identd_server.start()

if __name__ == '__main__':
    runserver()
