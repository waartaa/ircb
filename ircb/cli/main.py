import click

from ircb.cli.user import user_cli
from ircb.cli.network import network_cli
from ircb.cli.runserver import runserver_cli
import ircb.stores


@click.group()
def cli():
    """ircb CLI"""
    ircb.stores.initialize()


cli.add_command(user_cli)
cli.add_command(network_cli)
cli.add_command(runserver_cli)

if __name__ == '__main__':
    cli()
