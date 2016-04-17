# -*- coding: utf-8 -*-
import irc3
from irc3.plugins.autojoins import AutoJoins as Irc3AutoJoins


@irc3.plugin
class Autojoins(Irc3AutoJoins):

    def __init__(self, bot):
        super().__init__(bot)
        self.kicks_count = {}

    @irc3.event(irc3.rfc.KICK)
    def on_kick(self, mask, channel, target, **kwargs):
        # noop for now
        pass
