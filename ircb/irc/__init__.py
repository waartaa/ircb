# -*- coding: utf-8 -*-
import asyncio
import logging
import re

from irc3 import IrcBot, IrcConnection

from ircb.stores import NetworkMessageStore
from ircb.storeclient import NetworkStore

logger = logging.getLogger('irc')


class IrcbIrcConnection(IrcConnection):

    def connection_made(self, transport):
        super().connection_made(transport)
        asyncio.Task(self.handle_connection_made(transport))

    def data_received(self, data):
        super().data_received(data)

    def connection_lost(self, exc):
        yield from NetworkStore.update(
            dict(
                filter=('id', self.factory.config.id),
                update={
                    'status': '3',
                    'lhost': None,
                    'lport': None,
                    'rhost': None,
                    'rport': None
                }
            )
        )
        super().connection_lost(exc)

    @asyncio.coroutine
    def handle_connection_made(self, transport):
        logger.debug('Network connected: %s, %s, %s',
                     self.factory.config.userinfo,
                     self.factory.config.name, self.factory.config.nick)
        socket = transport.get_extra_info('socket')
        lhost, lport = socket.getsockname()
        rhost, rport = socket.getpeername()
        yield from NetworkStore.update(
            dict(
                filter=('id', self.factory.config.id),
                update={
                    'status': '1',
                    'lhost': lhost,
                    'lport': lport,
                    'rhost': rhost,
                    'rport': rport
                }
            )
        )


class IrcbBot(IrcBot):

    defaults = dict(
        IrcBot.defaults,
        nick=None,
        realname='',
        userinfo=None,
        host='localhost',
        port=6667,
        url='https://github.com/waartaa/ircb',
        passwords={},
        ctcp=dict(
            version='ircb - https://github.com/waartaa/ircb',
            userinfo='{userinfo}',
            time='{now:%c}'
        ),
        connection=IrcbIrcConnection
    )
    cmd_regex = re.compile(
        r'(?P<cmd>[A-Z]+)(?:\s+(?P<args>[^\:]+))?(?:\:(?P<msg>.*))?')

    def __init__(self, *args, **kwargs):
        self.clients = None
        self.message_store = NetworkMessageStore()
        super().__init__(*args, **kwargs)

    def run_in_loop(self):
        """Run bot in an already running event loop"""
        self.create_connection()
        self.add_signal_handlers()

    def join(self, target, password=None):
        """join a channel"""
        if not password:
            password = self.config.passwords.get(
                target.strip(self.server_config['CHANTYPES']))
        if password:
            target += ' ' + password
        self.send_line('JOIN %s' % target)

    def raw(self, message):
        """Handle raw message"""
        m = self.cmd_regex.match(message)
        cmd = args = msg = None
        if m:
            cmd, args, msg = m.groups()
            args = args.strip() if args else args

        if cmd == 'PRIVMSG':
            if msg.startswith('\x01') and msg.endswith('\x01'):
                self.ctcp(args, msg.strip('\x01'))
            else:
                self.privmsg(args, msg)
        elif cmd == 'NOTICE':
            if msg.startswith('\x01') and msg.endswith('\x01'):
                self.ctcp_reply(args, msg.strip('\x01'))
            else:
                self.notice(args, msg)
        elif cmd == 'MODE':
            _ = args.split()
            self.mode(_[0], *_[1:])
        elif cmd == 'JOIN':
            _ = args.split()
            self.join(_[0], _[1] if len(_) > 1 else None)
        elif cmd == 'PART':
            self.part(args, msg)
        elif cmd == 'TOPIC':
            self.topic(args, msg)
        elif cmd == 'AWAY':
            self.away(args, msg)
        elif cmd == 'QUIT':
            self.quit(msg)
        elif cmd == 'NICK':
            self.set_nick(args)
        else:
            self.send_line(message)

    def dispatch(self, data, iotype='in', client=None):
        if iotype == 'in':
            self.dispatch_to_clients(data)
        super().dispatch(data, iotype, client)

    def dispatch_to_clients(self, data):
        for client in self.clients:
            client.send(data)

    def get_joining_messages(self):
        logger.debug('Joining messages: %s', self.message_store.get_all())
        return self.message_store.get_all()
