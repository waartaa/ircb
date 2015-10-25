import asyncio
import logging
import logging.config
from network import Network
from connection import Connection
import ircb.stores
from ircb.models import get_session, Network as NetworkModel, User
from ircb.config import settings
from ircb.storeclient import NetworkStore, ClientStore


logger = logging.getLogger('bouncer')


class BouncerServerClientProtocol(Connection):

    def __init__(self, get_network_handle, unregister_client):
        self.network = None
        self.forward = None
        self.get_network_handle = get_network_handle
        self.unregister_client = unregister_client
        self.host, self.port = None, None
        self.client_id = None

    def connection_made(self, transport):
        logger.debug('New client connection received')
        self.transport = transport
        self.host, self.port = self.transport.get_extra_info(
            'socket').getpeername()

    def data_received(self, data):
        asyncio.Task(self.handle_data_received(data))

    @asyncio.coroutine
    def handle_data_received(self, data):
        data = self.decode(data)
        logger.debug('Received client data: %s', data)
        for line in data.rstrip().splitlines():
            verb, message = line.split(" ", 1)
            if verb == "QUIT":
                pass
            elif verb == "PASS":
                access_token = message.split(" ")[0]
                self.network = self.get_network(access_token)
                if self.network is None:
                    logger.debug(
                        'Client authentiacation failed for token: {}'.format(
                            access_token))
                    self.unregister_client(self.network.id, self)
                    self.transport.write('Authentication failed')
                    self.transport.close()
                else:
                    client = yield from ClientStore.create({
                        'socket': '{}:{}'.format(self.host, self.port),
                        'network_id': self.network.id,
                        'user_id': self.network.user_id
                    })
                    self.client_id = client.id
            elif self.forward:
                self.forward(line)

            if self.forward is None:
                self.forward = yield from self.get_network_handle(
                    self.network, self)

    def connection_lost(self, exc):
        self.unregister_client(self.network.id, self)
        logger.debug('Client connection lost: {}'.format(self.network))
        if self.client_id:
            asyncio.Task(ClientStore.delete({'id': self.client_id}))

    def get_network(self, access_token):
        return session.query(NetworkModel).filter(
            NetworkModel.access_token == access_token).first()

    def __str__(self):
        return '<BouncerClientConnection {}:{}>'.format(
            self.host, self.port)

    def __repr__(self):
        return self.__str__()


class Bouncer(object):

    def __init__(self, session):
        self.networks = {}
        self.clients = {}
        self.session = session

    def start(self, host='127.0.0.1', port=9000):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(
            lambda: BouncerServerClientProtocol(self.get_network_handle,
                                                self.unregister_client),
            host, port)
        logger.info('Listening on {}:{}'.format(host, port))
        bouncer_server = loop.run_until_complete(coro)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        bouncer_server.close()
        loop.run_until_complete(bouncer_server.wait_closed())

    def get_network_handle(self, network, client):
        try:
            key = network.id
            network_conn = self.networks.get(key)
            if network_conn is None:
                user = session.query(User).get(network.user_id)
                logger.debug(
                    'New network connection: {}-{}'.format(
                        user.username, network.name)
                )
                loop = asyncio.get_event_loop()
                yield from NetworkStore.update(
                    dict(
                        filter=('id', network.id),
                        update={
                            'status': '0'
                        })
                )
                coro = loop.create_connection(
                    lambda: Network(
                        user.username, network.id, network.name,
                        network.nickname, network.username, network.password,
                        register=self.register_network,
                        usermode=network.usermode,
                        realname=network.realname
                    ),
                    network.hostname, network.port)
                asyncio.async(coro)
            else:
                logger.debug('Reusing network connection: {}'.format(
                    network_conn))
                joining_messages = network_conn.get_joining_messages()
                client.send(*[joining_messages])

                # FIXME
                for line in joining_messages.splitlines():
                    if 'JOIN' in line:
                        words = line.split(' ')
                        network_conn.send('NAMES', words[2])

            def forward(line):
                network_conn = self.networks.get(key)
                if network_conn:
                    logger.debug(
                        'Forwarding {}\t {}'.format(network_conn, line))
                    network_conn.send(*[line])

            self.register_client(key, client)
            return forward
        except Exception as e:
            logger.error('get_network_handle error: {}'.format(e),
                         exc_info=True)

    def register_network(self, network_id, network):
        logger.debug('Registering new network: {}'.format(network_id))
        key = network_id
        network_conn = self.networks.get(key)
        if network_conn:
            network_conn.transport.close()
            del self.networks[key]
        self.networks[key] = network
        logger.debug('Networks: %s', self.networks)

        def dispatch(data):
            clients = self.clients.get(key) or []
            logger.debug('Dispatch to clients: %s, %s\t%s',
                         key, clients, data.decode())
            for client in clients:
                client.transport.write(data)
        return dispatch

    def register_client(self, network_id, client):
        key = network_id
        clients = self.clients.get(key)
        if clients is None:
            clients = set()
            self.clients[key] = clients
        clients.add(client)
        logger.debug('Registered new client: %s, %s', key, clients)

    def unregister_client(self, network_id, client):
        key = network_id
        clients = self.clients.get(key)
        logger.debug('Unregistering client: {}'.format(client))
        try:
            clients.remove(client)
        except KeyError:
            pass

if __name__ == '__main__':
    logging.config.dictConfig(settings.LOGGING_CONF)
    session = get_session()
    ircb.stores.initialize()
    bouncer = Bouncer(session)
    bouncer.start()

