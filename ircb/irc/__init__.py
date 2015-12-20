# -*- coding: utf-8 -*-
import asyncio
import logging
import re

import irc3

from ircb.storeclient import NetworkStore
from ircb.storeclient import ChannelStore

logger = logging.getLogger('irc')


class IrcbIrcConnection(irc3.IrcConnection):

    def connection_made(self, transport):
        super().connection_made(transport)
        asyncio.Task(self.handle_connection_made(transport))

    def data_received(self, data):
        super().data_received(data)

    def connection_lost(self, exc):
        asyncio.Task(self.handle_connection_lost())
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

    @asyncio.coroutine
    def handle_connection_lost(self):
        logger.debug('Network disconnected: %s, %s, %s',
                     self.factory.config.userinfo,
                     self.factory.config.name, self.factory.config.nick)
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


class IrcbBot(irc3.IrcBot):

    defaults = dict(
        irc3.IrcBot.defaults,
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
        includes=['ircb.irc.plugins.ircb', 'ircb.irc.plugins.autojoins'],
        connection=IrcbIrcConnection
    )
    cmd_regex = re.compile(
        r'(?P<cmd>[A-Z]+)(?:\s+(?P<args>[^\:]+))?(?:\:(?P<msg>.*))?')

    def __init__(self, *args, **kwargs):
        self.clients = None
        super().__init__(*args, **kwargs)

    def run_in_loop(self):
        """Run bot in an already running event loop"""
        self.create_connection()
        self.add_signal_handlers()

    def connection_made(self, f):
        super().connection_made(f)
        # Release lock acquired during creating a new bot instance
        self.config.lock.release()

    def join(self, target, password=None):
        """join a channel"""
        if not password:
            password = self.config.passwords.get(
                target.strip(self.server_config['CHANTYPES']))
        if password:
            target += ' ' + password
        self.send_line('JOIN %s' % target)
        asyncio.Task(self.join_handler(target, password))

    @asyncio.coroutine
    def join_handler(self, target, password):
        yield from ChannelStore.create_or_update(
            dict(
                channel=target,
                network_id=self.config.id,
                password=password,
                status='0'
            )
        )

    def part(self, target, reason=None):
        super().part(target, reason)
        asyncio.Task(self.part_handler(target))

    @asyncio.coroutine
    def part_handler(self, target):
        yield from ChannelStore.create_or_update(
            dict(
                channel=target,
                network_id=self.config.id,
                status='2'
            )
        )

    def raw(self, message):
        """Handle raw message"""
        logger.debug('Received raw msg: %s' % message)
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
