import datetime
from flask_user import UserMixin
from sqlalchemy import (Column, String, Unicode, Boolean, ForeignKey, Integer,
                        DateTime)
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import PasswordType
from ircb.models.lib import Base


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    username = Column(Unicode(30), nullable=False, unique=True)
    email = Column(Unicode(255), nullable=False, unique=True)
    confirmed_at = Column(DateTime())
    password = Column(
        PasswordType(schemes=['pbkdf2_sha512', 'md5_crypt']),
        nullable=False, server_default='')
    reset_password_token = Column(String(100), nullable=False, default='')

    # User information
    active = Column('is_active', Boolean(), nullable=False, server_default='0')
    first_name = Column(Unicode(50), nullable=True, server_default=u'')
    last_name = Column(Unicode(50), nullable=True, server_default=u'')

    # Relationships
    roles = relationship('Role', secondary='users_roles',
                         backref=backref('users', lazy='dynamic'))

    # Timestamps
    created = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        d = super().to_dict()
        d.pop('password')
        d['is_active'] = self.is_active()
        return d

    def authenticate(self, password):
        if self.password == password:
            return True
        return False


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False, server_default=u'',
                  unique=True)  # for @roles_accepted()
    label = Column(Unicode(255), server_default=u'')  # for display purposes


class UsersRoles(Base):
    __tablename__ = 'users_roles'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('roles.id', ondelete='CASCADE'))
