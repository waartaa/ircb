# -*- coding: utf-8 -*-
import click

from ircb.lib.async import coroutinize
from ircb.storeclient import UserStore


@click.group(name='users')
def user_cli():
    """Manager users"""
    from ircb.storeclient import initialize
    initialize()


@click.command(name='create')
@click.argument('username')
@click.argument('email')
@click.argument('password', required=False, default='')
@coroutinize
def user_create(username, email, password):
    """Create a user"""
    yield from UserStore.create(dict(
        username=username,
        email=email,
        password=password
    ))


user_cli.add_command(user_create)
