# -*- coding: utf-8 -*-
import click

from ircb.storeclient import NetworkStore
from ircb.lib.async import coroutinize

@click.group(name='networks')
def network_cli():
    """Manager networks"""
    pass


@click.command(name='create')
@click.argument('user')
@click.argument('network_name')
@click.argument('host')
@click.argument('port')
@click.argument('nick')
@click.option('--realname', default='')
@click.option('--username', default='')
@click.option('--password', default='')
@click.option('--usermode', default='0')
@coroutinize
def create(user, network_name, host, port, nick, realname, username, password,
           usermode):
    """Create a network for a user"""
    network = yield from NetworkStore.create(
        dict(
            user=user,
            name=network_name,
            nickname=nick,
            hostname=host,
            port=port,
            realname=realname,
            username=username,
            password=password,
            usermode=usermode
        )
    )
    print(network.access_token)


network_cli.add_command(create)
