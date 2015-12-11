# -*- coding: utf-8 -*-
import click

from ircb.bouncer import runserver


@click.command(name='runserver')
@click.option('--host', '-h', default='0.0.0.0',
              help='Host, defaults to 0.0.0.0')
@click.option('--port', '-p', default=9000,
              help='Port, defaults to 9000')
def runserver_cli(host, port):
    """Run ircb server"""
    runserver(host, port)
