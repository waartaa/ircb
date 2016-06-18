# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ircb.models import create_tables

from .network import NetworkStore
from .client import ClientStore
from .channel import ChannelStore
from .user import UserStore
from .logs import MessageLogStore, ActivityLogStore
from .base import init


def initialize():
    init()
    create_tables()
    NetworkStore.initialize()
    ClientStore.initialize()
    ChannelStore.initialize()
    UserStore.initialize()
    MessageLogStore.initialize()
    ActivityLogStore.initialize()

__all__ = [
    'ClientStore',
    'NetworkStore',
    'ChannelStore',
    'UserStore',
    'MessageLogStore',
    'ActivityLogStore'
]
