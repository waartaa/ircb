from __future__ import absolute_import

from ircb.models import create_tables

from .network import NetworkStore


def initialize():
    create_tables()
    NetworkStore.initialize()
