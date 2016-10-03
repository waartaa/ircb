# -*- coding: utf-8 -*-
import asyncio
import click

from ircb import bouncer
from ircb.web import app as web
from ircb import identd


@click.group(name='run')
def run_cli():
    """Implement run commands"""
    pass


@click.command(name='allinone')
@click.option('--host', '-h', default='0.0.0.0',
              help='Host for bouncer, defaults to 0.0.0.0')
@click.option('--port', '-p', default=9000,
              help='Port for bouncer, defaults to 9000')
@click.option('--enable-identd', '-i', default=False, is_flag=True,
              help='Run with identd')
@click.option('--identd-host', default='0.0.0.0',
              help='Host for identd, defaults to 0.0.0.0')
@click.option('--identd-port', default=113,
              help='Port for identd, defaults to 113')
@click.option('--web-host', default='0.0.0.0',
              help='Host for web server, defaults to 0.0.0.0')
@click.option('--web-port', default=10000,
              help='Port for web server, defaults to 10000')
def run_allinone(host, port, enable_identd, identd_host, identd_port,
                 web_host, web_port):
    """Run ircb in a single process"""
    import ircb.stores
    import ircb.stores.base
    import ircb.storeclient
    ircb.stores.initialize()
    loop = asyncio.get_event_loop()
    bouncer_server = bouncer.Bouncer(loop).create(host, port)
    if enable_identd:
        identd_server = identd.IdentdServer(loop).create(
            identd_host, identd_port)
    web_server = web.createserver(loop, web_host, web_port)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    bouncer_server.close()
    web_server.close()
    loop.run_until_complete(bouncer_server.wait_closed())
    loop.run_until_complete(web_server.wait_closed())
    if enable_identd:
        identd_server.close()
        loop.run_until_complete(identd_server.wait_closed())


@click.command(name='stores')
def run_stores():
    """Run ircb stores"""
    import ircb.stores
    import ircb.stores.base
    ircb.stores.initialize()
    ircb.stores.base.dispatcher.run_forever()


@click.command(name='bouncer')
@click.option('--host', '-h', default='0.0.0.0',
              help='Host, defaults to 0.0.0.0')
@click.option('--port', '-p', default=9000,
              help='Port, defaults to 9000')
def run_bouncer(host, port):
    """Run ircb bouncer"""
    bouncer.runserver(host, port)


@click.option('--host', '-h', default='0.0.0.0',
              help='Host, defaults to 0.0.0.0')
@click.option('--port', '-p', default=10000,
              help='Port, defaults to 10000')
@click.command(name='web')
def run_web(host, port):
    """Run ircb web server"""
    web.runserver(host, port)


@click.command(name='identd')
@click.option('--host', '-h', default='0.0.0.0',
              help='Host, defaults to 0.0.0.0')
@click.option('--port', '-p', default=113,
              help='Port, defaults to 113')
def run_identd(host, port):
    """Run identd server"""
    identd.runserver(host, port)

run_cli.add_command(run_allinone)
run_cli.add_command(run_bouncer)
run_cli.add_command(run_stores)
run_cli.add_command(run_web)
run_cli.add_command(run_identd)
