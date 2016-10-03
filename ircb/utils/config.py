# -*- coding: utf-8 -*-
import logging.config

from ircb.config import settings


def load_config(verbose=False, **kwargs):
    logging_conf = settings.LOGGING_CONF

    loglevel = 'INFO'
    if verbose:
        loglevel = 'DEBUG'

    logging_conf['level'] = loglevel
    for key, value in logging_conf['handlers'].items():
        value['level'] = loglevel

    logging.config.dictConfig(settings.LOGGING_CONF)
