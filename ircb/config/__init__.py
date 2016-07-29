# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from . import default_settings


class Settings(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._data = {}
        for attr in dir(default_settings):
            if attr.startswith('__'):
                continue
            self._data[attr] = getattr(default_settings, attr, None)
        settings_path = os.getenv('IRCB_SETTINGS')
        if settings_path and os.path.isfile(settings_path):
            with open(settings_path) as f:
                code = compile(f.read(), settings_path, 'exec')
                exec(code, self._data)
            # FIXME: Do not remove __builtins__
            # self._data.pop('__builtins__', None)

    def __getitem__(self, key):
        return self._data.get(key)

    def __getattr__(self, key):
        return self._data.get(key)

settings = Settings()

__all__ = ['settings']
