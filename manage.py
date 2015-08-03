from flask.ext.script import Command, Manager, Option

from ircb.web.app import app
from ircb.models import create_tables, get_session, User, Network

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

    def run(self, user, name, nick, host, port, realname, username, password,
            usermode):
        user = session.query(User).filter(User.username == user).first()
        if user is None:
            raise
        network = Network(name=name, nickname=nick, hostname=host, port=port,
                          realname=realname, username=username,
                          password=password, usermode=usermode,
                          user_id=user.id)
        session.add(network)
        session.commit()
        print(network.access_token)


if __name__ == '__main__':
    create_tables()
    manager.add_command('createuser', CreateUserCommand())
    manager.add_command('createnetwork', CreateNetworkCommand())
    manager.run()
