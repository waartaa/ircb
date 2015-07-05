import asyncio
import logging
from stores import network_store, auth_store
from network import Network
from connection import Connection

logger = logging.getLogger('bouncer')


class BouncerServerClientProtocol(Connection):

    def __init__(self, get_network_handle):
        self.network = None
        self.username = None
        self.password = None
        self.forward = None
        self.get_network_handle = get_network_handle

    def connection_made(self, transport):
        logger.debug('New client connection received')
        self.transport = transport

    def authenticate(self, username, password):
        return auth_store.auth(username, password)

    def data_received(self, data):
        data = self.decode(data)
        logger.debug('Received client data: %s', data)
        for line in data.rstrip().splitlines():
            verb, message = line.split(" ", 1)
            if verb == "QUIT":
                pass
            elif verb == "USER":
                self.username = message.split(" ")[0]
            elif verb == "PASS":
                self.password = message.split(" ")[0]
            else:
                if self.forward:
                    self.forward(self.encode(line))
            if self.username and self.password and self.forward is None:
                if self.authenticate(self.username, self.password) is None:
                    logger.debug(
                        'Client authentication failed: %s, %s', self.username,
                        self.password)
                    self.transport.write('Authentication failed')
                    self.transport.close()
                self.forward = self.get_network_handle(
                    self.username, self.password, self)

    def connection_lost(self, exc):
        logger.debug('Client connection lost: %s, %s',
                     self.username, self.network)


class Bouncer(object):

    def __init__(self):
        self.networks = {}
        self.clients = {}

    def start(self, host='127.0.0.1', port=9000):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(
            lambda: BouncerServerClientProtocol(self.get_network_handle),
            host, port)
        logger.info('Listening on {}:{}'.format(host, port))
        bouncer_server = loop.run_until_complete(coro)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        bouncer_server.close()
        loop.run_until_complete(bouncer_server.wait_closed())
        loop.close()

    def get_network_handle(self, username, password, client):
        network_data = network_store.get('{}:{}'.format(username, password))
        if network_data is None:
            return
        key = '{}:{}'.format(username, network_data['name'])
        network = self.networks.get(key)
        if network is None:
            logger.debug(
                'New network connection: %s, %s, %s', username,
                network_data['name'], network_data
            )
            loop = asyncio.get_event_loop()
            coro = loop.create_connection(
                lambda: Network(
                    username, network_data['name'], network_data['nickname'],
                    network_data['username'], network_data['password'],
                    register=self.register_network),
                network_data['hostname'], network_data['port'])
            asyncio.async(coro)
        else:
            logger.debug('Reusing network connection: %s, %s, %s',
                         username, network_data['name'], network_data)
            network.send('USER', username, network_data['usermode'], '*',
                         ':{}'.format(network_data['realname']))
            if network_data.get('password'):
                network.send('PASS', network_data['password'])

        def forward(line):
            network = self.networks.get(key)
            logger.debug('Forwarding {}->{}\n %s'.format(username, network),
                         line.decode())
            network.send(*[line])

        self.register_client(username, password, client)
        return forward

    def register_network(self, username, network_name, network):
        logger.debug('Registering new network: %s, %s', 
                     username, network_name)
        key = '{}:{}'.format(username, network_name)
        _network = self.networks.get(key)
        if _network:
            _network.transport.close()
            del self.networks[key]
        self.networks[key] = network
        logger.debug('Networks: %s', self.networks)

        def dispatch(data):
            clients = self.clients.get(key) or []
            logger.debug('Dispatch to clients: %s, %s\n%s',
                         key, clients, data.decode())
            for client in clients:
                client.transport.write(data)
        return dispatch

    def register_client(self, username, password, client):
        network_data = network_store.get(
            '{}:{}'.format(username, password))
        if network_data is None:
            return
        key = '{}:{}'.format(username, network_data['name'])
        clients = self.clients.get(key)
        if clients is None:
            clients = set()
            self.clients[key] = clients
        clients.add(client)
        logger.debug('Registered new client: %s, %s', key, clients)

if __name__ == '__main__':
    import logging
    from config.logging import load_config
    load_config()
    bouncer = Bouncer()
    bouncer.start()
