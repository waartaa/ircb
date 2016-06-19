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

    def to_dict(self, serializable=False):
        d = super().to_dict()
        if serializable:
            d['timestamp'] = self.timestamp.timestamp()
            d['created'] = self.created.timestamp()
            d['last_updated'] = self.last_updated.timestamp()


class MessageLog(Base, BaseLog):
    """
    Network/Channel/PM messages
    """
    __tablename__ = 'message_logs'

    from_nickname = sa.Column(sa.String(20))
    from_user_id = sa.Column(sa.Integer, nullable=True, default=None)


class ActivityLog(Base, BaseLog):
    """
    Channel activity(join, part, quit) logs
    """
    __tablename__ = 'activity_logs'
