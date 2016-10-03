# -*- coding: utf-8 -*-
from wtforms_alchemy import ModelForm

from ircb.models import User


class UserForm(ModelForm):

    class Meta:
        model = User
        only = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
        ]
        unique_validator = None
