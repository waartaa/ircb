from ircb.lib.constants.signals import (
    STORE_USER_CREATE, STORE_USER_CREATED,
    STORE_USER_GET, STORE_USER_GOT)
from ircb.models import get_session, User
from ircb.stores.base import BaseStore

session = get_session()


class UserStore(BaseStore):
    CREATE_SIGNAL = STORE_USER_CREATE
    CREATED_SIGNAL = STORE_USER_CREATED
    GET_SIGNAL = STORE_USER_GET
    GOT_SIGNAL = STORE_USER_GOT

    @classmethod
    def get(cls, query):
        if isinstance(query, dict):
            qs = session.query(User)
            for key, value in query.items():
                qs = qs.filter(getattr(User, key) == value)
            return qs.all()
        elif isinstance(query, tuple):
            key, value = query
            return session.query(User).filter(
                getattr(User, key) == value).first()
        else:
            return session.query(User).get(query)

    @classmethod
    def create(cls, username, email, password):
        user = User(username=username, email=email, password=password)
        session.add(user)
        session.commit()
        return user
