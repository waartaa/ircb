import asyncio
import logging
from ircb.storeclient import ChannelStore

logger = logging.getLogger(__name__)


class IRCCommandHandler(object):

    def __init__(self, network_id, nickname):
        self.network_id = network_id
        self.nickname = nickname

    @asyncio.coroutine
    def handle(self, *args):
        cmd = args[0].split()[0]
        handler = getattr(self, 'handle_{}'.format(cmd.lower()), None)
        if handler:
            yield from handler(*args)

    def handle_join(self, *args):
        words = " ".join(args).split()
        channel_name = words[1]
        channel_password = words[2] if len(words) >= 3 else None
        channel = yield from ChannelStore.create_or_update(
            dict(
                channel=channel_name,
                network_id=self.network_id,
                password=channel_password,
                status='0'
            )
        )

    def handle_part(self, *args):
        words = " ".join(args).split()
        channel_name = words[1]
        channel = yield from ChannelStore.create_or_update(
            dict(
                channel=channel_name,
                network_id=self.network_id,
                status='2'
            )
        )


class IRCReplyHandler(object):

    def __init__(self, network_id, nickname):
        self.network_id = network_id
        self.nickname = nickname

    @asyncio.coroutine
    def handle(self, msg):
        lines = msg.splitlines()
        for line in lines:
            if 'JOIN' in line:
                yield from self.handle_join(line)
            elif 'PART' in line:
                yield from self.handle_part(line)

    @asyncio.coroutine
    def handle_join(self, msg):
        words = msg.split()
        nick = words[0].split('!')[0]
        if nick != ':' + self.nickname:
            return
        channel_name = words[2]
        channel = yield from ChannelStore.create_or_update(
            dict(
                channel=channel_name,
                network_id=self.network_id,
                status='1'
            )
        )

    @asyncio.coroutine
    def handle_part(self, msg):
        words = msg.split()
        nick = words[0].split('!')[0]
        if nick != ':' + self.nickname:
            return
        channel_name = words[2]
        channel = yield from ChannelStore.create_or_update(
            dict(
                channel=channel_name,
                network_id=self.network_id,
                status='3'
            )
        )
