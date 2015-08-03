from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from ircb.config import settings

Base = declarative_base()


def create_tables(db_uri=settings.DB_URI):
    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)


def get_session(db_uri=settings.DB_URI):
    engine = create_engine(db_uri)
    scopedsession = scoped_session(sessionmaker(bind=engine))
    return scopedsession
