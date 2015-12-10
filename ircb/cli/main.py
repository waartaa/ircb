import click

from ircb.cli.user import user_cli
from ircb.cli.network import network_cli
import ircb.stores


@click.group()
def cli():
    """ircb CLI"""
    ircb.stores.initialize()


cli.add_command(user_cli)
cli.add_command(network_cli)

if __name__ == '__main__':
    cli()
