# -*- coding: utf-8 -*-
import datetime
import sqlalchemy as sa

from ircb.models.lib import Base


class BaseLog(object):
    id = sa.Column(sa.Integer, primary_key=True)

    hostname = sa.Column(sa.String(100), nullable=False)
    roomname = sa.Column(sa.String(255), nullable=False)

    message = sa.Column(sa.String(2048), default='')
    event = sa.Column(sa.String(20), nullable=False)
    timestamp = sa.Column(sa.TIMESTAMP(timezone=True))
    mask = sa.Column(sa.String(100), default='')

    user_id = sa.Column(sa.Integer)

    # timestamps
    created = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    last_updated = sa.Column(sa.DateTime,
                             default=datetime.datetime.utcnow)

    def to_dict(self, serializable=True):
        d = super().to_dict()
        if serializable:
            d['timestamp'] = self.timestamp.timestamp()
        return d

    @classmethod
    def from_dict(cls, data, serialized=True):
        if serialized:
            data['timestamp'] = datetime.datetime.fromtimestamp(
                data['timestamp'])
            if 'created' in data:
                data['created'] = datetime.datetime.fromtimestamp(
                    data['created'])
            if 'last_updated' in data:
                data['last_updated'] = datetime.datetime.fromtimestamp(
                    data['last_updated'])
        return cls(**data)


class MessageLog(BaseLog, Base):
    """
    Network/Channel/PM messages
    """
    __tablename__ = 'message_logs'

    from_nickname = sa.Column(sa.String(20))
    from_user_id = sa.Column(sa.Integer, nullable=True, default=None)


class ActivityLog(BaseLog, Base):
    """
    Channel activity(join, part, quit) logs
    """
    __tablename__ = 'activity_logs'
