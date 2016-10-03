# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy import UniqueConstraint
from sqlalchemy_utils import ChoiceType

from ircb.config import settings
from ircb.models.lib import Base

CHANNEL_STATUS_TYPES = (
    ('0', 'Connecting'),
    ('1', 'Connected'),
    ('2', 'Disconnecting'),
    ('3', 'Disconnected')
)


class Channel(Base):
    __tablename__ = 'channels'
    __table_args__ = (
        UniqueConstraint('network_id', 'name'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False, default='')
    network_id = Column(Integer(),
                        ForeignKey('networks.id', ondelete='CASCADE'),
                        nullable=False)
    user_id = Column(Integer(),
                     ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)

    # Runtime fields
    status = Column(ChoiceType(CHANNEL_STATUS_TYPES))

    # timestamps
    created = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        d = super().to_dict()
        d['status'] = self.status if isinstance(self.status, str) \
            else self.status.code
        return d
