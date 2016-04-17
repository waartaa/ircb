# -*- coding: utf-8 -*-
import datetime

from hashlib import md5

import sqlalchemy as sa

from sqlalchemy_utils import ChoiceType, Choice

from ircb.models.lib import Base, get_session
from ircb.models.user import User
from ircb.config import settings

NETWORK_STATUS_TYPES = (
    ('0', 'Connecting'),
    ('1', 'Connected'),
    ('2', 'Disconnecting'),
    ('3', 'Disconnected')
)
SSL_VERIFY_CHOICES = (
    ('CERT_NONE', 'No certs required'),
    ('CERT_OPTIONAL', 'Optional cert'),
    ('CERT_REQUIRED', 'Cert required')
)
session = get_session()


def _create_access_token(user_id, network_name):
    user = session.query(User).get(user_id)
    return md5('{}{}{}{}'.format(settings.SECRET_KEY,
                                 user.username,
                                 network_name,
                                 datetime.datetime.utcnow()).encode()
               ).hexdigest()


class Network(Base):
    __tablename__ = 'networks'
    __table_args__ = (
        sa.UniqueConstraint('user_id', 'name'),
    )
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    nickname = sa.Column(sa.String(20), nullable=False)
    hostname = sa.Column(sa.String(100), nullable=False)
    port = sa.Column(sa.Integer, nullable=False)
    realname = sa.Column(sa.String(100), nullable=False, default='')
    username = sa.Column(sa.String(50), nullable=False, default='')
    password = sa.Column(sa.String(100), nullable=False, default='')
    usermode = sa.Column(sa.String(1), nullable=False, default='0')
    ssl = sa.Column(sa.Boolean(), default=False)
    ssl_verify = sa.Column(ChoiceType(SSL_VERIFY_CHOICES),
                           default=Choice(*SSL_VERIFY_CHOICES[0]))

    access_token = sa.Column(sa.String(100), nullable=False, unique=True,
                             default=lambda context: _create_access_token(
                             context.current_parameters['user_id'],
                             context.current_parameters['name']))
    user_id = sa.Column(
        sa.Integer(), sa.ForeignKey(User.id, ondelete='CASCADE'),
        nullable=False)

    # Runtime fields
    current_nickname = sa.Column(sa.String(20), nullable=True)
    status = sa.Column(ChoiceType(NETWORK_STATUS_TYPES),
                       default=Choice(*NETWORK_STATUS_TYPES[3]))

    # Remote socket info
    rhost = sa.Column(sa.String(100), nullable=True)
    rport = sa.Column(sa.Integer(), nullable=True)

    # Local socket info
    lhost = sa.Column(sa.String(100), nullable=True)
    lport = sa.Column(sa.Integer(), nullable=True)

    # timestamps
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    last_updated = sa.Column(sa.DateTime,
                             default=datetime.datetime.utcnow)

    def create_access_token(self):
        return _create_access_token(self.user.id, self.name)

    def to_dict(self, serializable=False):
        d = super().to_dict()
        ssl_verify = self.ssl_verify and self.ssl_verify if isinstance(
            self.ssl_verify, str) else self.ssl_verify.code
        status = self.status and (
            self.status if isinstance(self.status, str) else self.status.code)
        d['ssl_verify'] = ssl_verify
        d['status'] = status
        if serializable:
            d['created'] = self.created.timestamp()
            d['last_updated'] = self.last_updated.timestamp()
        return d
