# -*- coding: utf-8 -*-
import click
import yaml

from ircb.lib.async import coroutinize
from ircb.storeclient import UserStore
from ircb.storeclient import NetworkStore


@click.group(name='users')
def loaddata_cli():
    "Loads YAML file with config"
    pass


def validate_yaml(f): 
    "Validates YAML file"
    return True


@click.command(name='loaddata')
@click.argument('f')
@coroutinize
def load_data(f):
    with open(f, 'r') as f:
        config = yaml.load(f)

        if validate_yaml(config): 

            for user in config.keys():
                user_data = config[user]
                yield from UserStore.create(
                    dict(
                        username=user,
                        email=user_data['email'],
                        password=user_data['password']
                    )
                )
                networks = user_data['networks']
                for net in networks.keys():
                    net_data = networks[net]
                    network = yield from NetworkStore.create(
                        dict(
                            user=user,
                            name=net,
                            nickname=net_data["nick"],
                            hostname=net_data["host"],
                            port=net_data["port"],
                            realname=net_data["realname"],
                            username=net_data["username"],
                            password=net_data["password"],
                            usermode=net_data["usermode"],
                        )
                    )
