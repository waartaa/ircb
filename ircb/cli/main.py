import click

from ircb.cli.user import user_cli
from ircb.cli.network import network_cli
from ircb.cli.run import run_cli
from ircb.cli.loaddata import load_data


@click.group()
def cli():
    """ircb CLI"""
    pass


cli.add_command(user_cli)
cli.add_command(network_cli)
cli.add_command(run_cli)
cli.add_command(load_data)

if __name__ == '__main__':
    cli()
