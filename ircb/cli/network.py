# -*- coding: utf-8 -*-
import click

from tabulate import tabulate

from ircb.storeclient import NetworkStore
from ircb.lib.async import coroutinize

@click.group(name='networks')
def network_cli():
    """Manager networks"""
    from ircb.storeclient import initialize
    initialize()


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
@click.option('--ssl', default=False, is_flag=True)
@click.option('--ssl_verify', default="CERT_NONE",
              type=click.Choice(
                  ['CERT_NONE', 'CERT_OPTIONAL', 'CERT_REQUIRED']))
@coroutinize
def create(user, network_name, host, port, nick, realname, username, password,
           usermode,ssl,ssl_verify):
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
            usermode=usermode,
            ssl=ssl,
            ssl_verify=ssl_verify
        )
    )
    print(network.access_token)


@click.command(name='list')
@coroutinize
def ls(page=1):
    networks = yield from NetworkStore.get({'query': {}})
    headers = ['Id', 'User', 'Name', 'Nick', 'Server']
    table = [
        [network.id,
         network.user_id,
         network.name,
         network.nickname,
         '{}/{}'.format(network.hostname, network.port)]
        for network in networks]
    print(tabulate(table, headers, tablefmt='grid'))


@click.command(name='connect')
@click.argument('id')
@coroutinize
def connect(id):
    network = yield from NetworkStore.update(
        dict(
            filter=('id', id),
            update={
                'status': '0'
            })
    )

@click.command(name='disconnect')
@click.argument('id')
@coroutinize
def disconnect(id):
    network = yield from NetworkStore.update(
        dict(
            filter=('id', id),
            update={
                'status': '2'
            })
    )


network_cli.add_command(create)
network_cli.add_command(ls)
network_cli.add_command(connect)
network_cli.add_command(disconnect)
