# -*- coding: utf-8 -*-
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from ircb.config import settings


class _Base(object):

    def to_dict(self, serializable=True):
        d = {}
        for col in self.__table__.columns:
            d[col.name] = getattr(self, col.name)
        if serializable:
            if getattr(self, 'created'):
                d['created'] = self.created.timestamp()
            if getattr(self, 'last_updated'):
                d['last_updated'] = self.last_updated.timestamp()
        return d

    @classmethod
    def from_dict(cls, data, serialized=True):
        if serialized:
            if 'created' in data:
                data['created'] = datetime.datetime.fromtimestamp(
                    data['created'])
            if 'last_updated' in data:
                data['last_updated'] = datetime.datetime.fromtimestamp(
                    data['last_updated'])
        return cls(**data)

Base = declarative_base(cls=_Base)


def create_tables(db_uri=settings.DB_URI):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)


def get_session(db_uri=settings.DB_URI):
    engine = create_engine(db_uri)
    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession
