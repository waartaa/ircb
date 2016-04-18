# -*- coding: utf-8 -*-
import asyncio
import logging

from collections import defaultdict

import ircb.stores

from ircb.config import settings
from ircb.connection import Connection
from ircb.irc import IrcbBot
from ircb.storeclient import initialize as storeclient_initialize
from ircb.storeclient import ChannelStore, ClientStore, NetworkStore, UserStore

logger = logging.getLogger('bouncer')


class BouncerServerClientProtocol(Connection):

    def __init__(self, get_bot_handle, unregister_client):
        self.network = None
        self.forward = None
        self.get_bot_handle = get_bot_handle
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
            tokens = line.split(" ", 1)
            verb = tokens[0]
            if verb == "QUIT":
                pass

            elif verb == "PASS":
                message = tokens[1]
                access_token = message.split(" ")[0]
                self.network = yield from self.get_network(access_token)
                if self.network is None:
                    logger.debug(
                        'Client authentiacation failed for token: {}'.format(
                            access_token))
                    self.unregister_client(self.network.id, self)
                    self.transport.write('Authentication failed')
                    self.transport.close()
                    return
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
            self.forward = yield from self.get_bot_handle(
                self.network, self)
            if self.forward is None:
                self.transport.write('Bot not connected')
                self.transport.close()
                asyncio.Task(ClientStore.delete({'id': self.client_id}))

    def connection_lost(self, exc):
        self.unregister_client(self.network.id, self)
        logger.debug('Client connection lost: {}'.format(self.network))
        if self.client_id:
            asyncio.Task(ClientStore.delete({'id': self.client_id}))

    def get_network(self, access_token):
        result = yield from NetworkStore.get(
            {'query': ('access_token', access_token)})
        return result

    def __str__(self):
        return '<BouncerClientConnection {}:{}>'.format(
            self.host, self.port)

    def __repr__(self):
        return self.__str__()


class Bouncer(object):

    def __init__(self):
        self.bots = {}
        self.clients = defaultdict(set)
        NetworkStore.on('create', self.on_network_create)
        NetworkStore.on('update', self.on_network_update)

    def start(self, host, port):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(
            lambda: BouncerServerClientProtocol(self.get_bot_handle,
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

    def on_network_update(self, network, modified=None):
        asyncio.Task(self._on_network_create_update(network))

    def on_network_create(self, network):
        asyncio.Task(self._on_network_create_update(network))

    @asyncio.coroutine
    def _on_network_create_update(self, network):
        if network.status == '0':
            bot = self.bots.get(network.id)
            if bot and not bot.protocol.closed:
                return
            user = yield from UserStore.get({'query': network.user_id})
            logger.debug(
                'Creating new bot: {}-{}'.format(
                    user.username, network.name)
            )
            connected_channels = yield from ChannelStore.get({
                'query': dict(
                    network_id=network.id,
                    status='1'
                )
            })
            config = dict(
                id=network.id,
                name=network.name,
                userinfo=network.username,
                password=network.password,
                nick=network.nickname,
                realname=network.realname,
                host=network.hostname,
                port=network.port,
                ssl=network.ssl,
                ssl_verify=network.ssl_verify,
                lock=asyncio.Lock(),
                autojoins=[channel.name for channel in connected_channels]
            )
            # Acquire lock for connecting to IRC server, so that
            # other clients connecting to the same bot can wait on this
            # lock before trying to send messages to the bot
            yield from config['lock'].acquire()
            if bot and bot.protocol.closed:
                bot.reload_config(**config)
            else:
                bot = IrcbBot(**config)
            bot.run_in_loop()
            self.register_bot(network.id, bot)
        elif network.status == '2':
            bot = self.bots.get(network.id)
            if bot:
                bot.quit()
                bot.protocol.close()

    def on_network_delete(self, network):
        pass

    @asyncio.coroutine
    def get_bot_handle(self, network, client):
        try:
            key = network.id
            bot = self.bots.get(key)
            self.register_client(key, client)
            connected_channels = yield from ChannelStore.get({
                'query': dict(
                    network_id=key,
                    status='1'
                )
            })
            if bot is None:
                yield from NetworkStore.update(
                    dict(
                        filter=('id', network.id),
                        update={
                            'status': '0'
                        })
                )
                return
            logger.debug('Reusing existing bot: {}'.format(bot))
            # Wait for bot.config.lock to be release when connection is
            # made to remote IRC server
            if bot.config.lock:
                yield from bot.config.lock
                bot.config.lock = None
            joining_messages_list = [
                ':* 001 {nick} :You are now connected to {network}'.format(
                    nick=bot.nick, network=network.name),
                ':* 251 {nick} : '.format(nick=bot.nick)
            ]
            for channel in connected_channels:
                joining_messages_list.append(
                    ':{nick}!* JOIN {channel}'.format(
                        nick=bot.nick,
                        channel=channel.name)
                )
                bot.raw('NAMES %s' % channel.name)

            client.send(*['\r\n'.join(joining_messages_list)])

            def forward(line):
                bot = self.bots.get(key)
                if bot:
                    logger.debug(
                        'Forwarding {}\t {}'.format(bot, line))
                    bot.raw(line)

            return forward
        except Exception as e:
            logger.error('get_bot_handle error: {}'.format(e),
                         exc_info=True)

    def register_bot(self, network_id, bot):
        logger.debug('Registering new bot: {}'.format(network_id))
        key = network_id
        existing_bot = self.bots.get(key)
        if existing_bot:
            existing_bot.protocol.transport.close()
            del self.bots[key]
        bot.clients = self.clients[key]
        self.bots[key] = bot
        logger.debug('Bots: %s', self.bots)

    def register_client(self, network_id, client):
        key = network_id
        clients = self.clients[key]
        clients.add(client)
        logger.debug('Registered new client: %s, %s', key, clients)

    def unregister_client(self, network_id, client):
        key = network_id
        clients = self.clients[key]
        logger.debug('Unregistering client: {}'.format(client))
        try:
            clients.remove(client)
        except KeyError:
            pass


def runserver(host='0.0.0.0', port=9000, mode='allinone'):
    if mode == 'allinone':
        ircb.stores.initialize()
    storeclient_initialize()
    bouncer = Bouncer()
    bouncer.start(host, port)

if __name__ == '__main__':
    runserver()
