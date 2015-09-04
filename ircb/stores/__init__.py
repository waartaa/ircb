from __future__ import absolute_import

from ircb.models import create_tables

from .network import NetworkStore
from .network_message_store import NetworkMessageStore


def initialize():
    create_tables()
    NetworkStore.initialize()

__all__ = [
    'NetworkStore',
    'NetworkMessageStore'
]
