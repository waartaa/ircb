# -*- coding: utf-8 -*-
import asyncio
import irc3

from ircb.storeclient import ChannelStore


@irc3.plugin
class IrcbPlugin(object):

    def __init__(self, bot):
        self.bot = bot

    @irc3.event(irc3.rfc.JOIN)
    def on_join(self, mask, channel, **kw):
        def callback():
            yield from ChannelStore.create_or_update(
                dict(
                    channel=channel,
                    network_id=self.bot.config.id,
                    status='1'
                )
            )
        asyncio.Task(callback())

    @irc3.event(irc3.rfc.PART)
    def on_part(self, mask, channel, **kw):
        def callback():
            yield from ChannelStore.create_or_update(
                dict(
                    channel=channel,
                    network_id=self.bot.config.id,
                    status='3'
                )
            )
        asyncio.Task(callback())
