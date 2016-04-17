# -*- coding: utf-8 -*-
import click

from ircb.bouncer import runserver
from ircb.config import settings


@click.group(name='run')
def run_cli():
    """Implement run commands"""
    pass


@click.command(name='server')
@click.option('--host', '-h', default='0.0.0.0',
              help='Host, defaults to 0.0.0.0')
@click.option('--port', '-p', default=9000,
              help='Port, defaults to 9000')
@click.option('--mode', '-m', default='allinone',
              type=click.Choice(
                  ['allinone', 'bouncer']))
def run_server(host, port, mode):
    """Run ircb server"""
    runserver(host, port, mode)


@click.command(name='stores')
def run_stores():
    import ircb.stores
    import ircb.stores.base
    ircb.stores.initialize()
    ircb.stores.base.dispatcher.run_forever()


run_cli.add_command(run_server)
run_cli.add_command(run_stores)
