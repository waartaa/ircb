import click

from ircb.cli.user import user_cli
from ircb.cli.network import network_cli
from ircb.cli.run import run_cli


@click.group()
def cli():
    """ircb CLI"""
    from ircb.storeclient import initialize
    initialize()


cli.add_command(user_cli)
cli.add_command(network_cli)
cli.add_command(run_cli)

if __name__ == '__main__':
    cli()
