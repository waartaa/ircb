# -*- coding: utf-8 -*-
import logging.config

from ircb.config import settings

def load_config():
    logging.config.dictConfig(settings.LOGGING_CONF)
