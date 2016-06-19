# -*- coding: utf-8 -*-
import asyncio
import datetime
import irc3
from irc3.plugins.logger import Logger as Irc3Logger
from ircb.storeclient import MessageLogStore, ActivityLogStore


class StoreHandler(object):

    def __init__(self, bot):
        self.bot = bot

    def __call__(self, event):
        if event['event'].lower() == 'privmsg':
            asyncio.Task(self.handle_message_log(event))
        elif event['event'].lower() in ('join', 'part', 'quit', 'topic'):
            asyncio.Task(self.handle_activity_log(event))

    def handle_message_log(self, event):
        yield from MessageLogStore.create(dict(
            hostname=event['host'],
            roomname=event['channel'],
            message=event['data'],
            event=event['event'],
            timestamp=datetime.datetime.utcnow().timestamp(),
            mask=str(event['mask']),
            user_id=self.bot.config.get('user_id'),
            from_nickname=event['mask'].nick
        ))

    def handle_activity_log(self, event):
        yield from ActivityLogStore.create(dict(
            hostname=event['host'],
            roomname=event['channel'],
            message=event['data'],
            event=event['event'],
            timestamp=datetime.datetime.utcnow().timestamp(),
            mask=str(event['mask']),
            user_id=self.bot.config.get('user_id')
        ))
        pass


@irc3.plugin
class Logger(Irc3Logger):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self, **kwargs):
        super().process(**kwargs)

    @irc3.event((r'''(@(?P<tags>\S+) )?(?P<event>[A-Z]+) (?P<target>#\S+)'''
                 r'''(\s:(?P<data>.*)|$)'''), iotype='out')
    def on_output(self, event, target=None, data=None, **kwargs):
        super().on_output(event, target, data, **kwargs)

    @irc3.event((r'''(@(?P<tags>\S+) )?:(?P<mask>\S+) (?P<event>[A-Z]+)'''
                 r''' (?P<target>#\S+)(\s:(?P<data>.*)|$)'''))
    def on_input(self, mask, event, target=None, data=None, **kwargs):
        super().on_input(mask, event, target, data, **kwargs)
