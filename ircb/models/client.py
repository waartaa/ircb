# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy import UniqueConstraint

from ircb.models.lib import Base


class Client(Base):
    __tablename__ = 'clients'
    __table_args__ = (
        UniqueConstraint('socket', 'network_id'),
    )

    id = Column(Integer, primary_key=True)
    socket = Column(String(100), nullable=False)
    network_id = Column(
        Integer(), ForeignKey('networks.id', ondelete='CASCADE'),
        nullable=False)
    user_id = Column(
        Integer(), ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False)

    # created
    created = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
