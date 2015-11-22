# -*- coding: utf-8 -*-
import logging

from irc3 import IrcBot, IrcConnection

from ircb.stores import NetworkMessageStore

logger = logging.getLogger('irc')


class IrcbIrcConnection(IrcConnection):

    def data_received(self, data):
        super().data_received(data)


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
        words = message.split()
        cmd = words[0]

        if cmd == 'PRIVMSG':
            msg = ' '.join(words[2:])
            if msg.startswith('\x01') and msg.endswith('\x01'):
                self.ctcp(words[1], msg.strip('\x01'))
            else:
                self.privmsg(words[1], ' '.join(words[2:]))
        elif cmd == 'NOTICE':
            msg = ' '.join(words[2:])
            if msg.startswith('\x01') and msg.endswith('\x01'):
                self.ctcp_reply(words[1], msg.strip('\x01'))
            else:
                self.notice(words[1], ' '.join(words[2:]))
        elif cmd == 'MODE':
            self.mode(words[1], words[2:])
        elif cmd == 'JOIN':
            self.join(words[1], words[2] if len(words) > 2 else None)
        elif cmd == 'PART':
            self.part(words[1], ' '.join(words[2:]))
        elif cmd == 'TOPIC':
            self.topic(words[1], ' '.join(words[2:]))
        elif cmd == 'AWAY':
            self.away(words[1], ' '.join(words[2:]))
        elif cmd == 'QUIT':
            self.quit(' '.join(words[1:]))
        elif cmd == 'NICK':
            self.set_nick(words[1])
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
