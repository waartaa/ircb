import click

from ircb.cli.loaddata import load_data
from ircb.cli.network import network_cli
from ircb.cli.run import run_cli
from ircb.cli.user import user_cli
from ircb.utils.config import load_config


@click.group()
@click.option('--verbose', '-v', default=False, is_flag=True,
              help='Show verbose logs')
def cli(verbose):
    """ircb CLI"""
    load_config(verbose=verbose)

cli.add_command(user_cli)
cli.add_command(network_cli)
cli.add_command(run_cli)
cli.add_command(load_data)

if __name__ == '__main__':
    cli()
