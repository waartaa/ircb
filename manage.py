import asyncio
from flask.ext.script import Command, Manager, Option

from ircb.web.app import app
from ircb.models import get_session, User
from ircb.storeclient import NetworkStore
from ircb.lib.async import coroutinize
import ircb.stores
import ircb.bouncer

manager = Manager(app)
session = get_session()


class CreateUserCommand(Command):
    option_list = (
        Option('--username', '-u', dest='username'),
        Option('--email', '-e', dest='email'),
        Option('--password', dest='password')
    )

    def run(self, username, email, password):
        user = User(username=username, email=email, password=password)
        session.add(user)
        session.commit()


class CreateNetworkCommand(Command):
    option_list = (
        Option('--user', '-u', dest='user'),
        Option('--name', '-n', dest='name'),
        Option('--nick', dest='nick'),
        Option('--host', dest='host'),
        Option('--port', dest='port'),
        Option('--realname', dest='realname', default=''),
        Option('--username', dest='username', default=''),
        Option('--password', dest='password', default=''),
        Option('--usermode', '-m', dest='usermode', default='0'),
    )

    @coroutinize
    def run(self, user, name, nick, host, port, realname, username, password,
            usermode):
        network = yield from NetworkStore.create(
            dict(
                user=user,
                name=name,
                nickname=nick,
                hostname=host,
                port=port,
                realname=realname,
                username=username,
                password=password,
                usermode=usermode
            )
        )
        print(network.access_token)


@manager.command
def runserver(host='0.0.0.0', port=9000):
    ircb.bouncer.runserver(host, port)


if __name__ == '__main__':
    ircb.stores.initialize()
    manager.add_command('createuser', CreateUserCommand())
    manager.add_command('createnetwork', CreateNetworkCommand())
    manager.run()
