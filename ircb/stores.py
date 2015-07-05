import os
import json
import logging
import sys

logger = logging.getLogger('stores')


class AuthStore(object):

    def __init__(self):
        try:
            f = open(os.path.join(os.path.dirname(__file__),
                                  'config/users.json'))
            s = f.read()
            self._data = json.loads(s)
            logger.debug('Loaded users data')
        except:
            logger.error('Unable to load users data')
            sys.exit(1)

    def auth(self, username, password):
        return self._data.get('{}:{}'.format(username, password))


class NetworkStore(object):

    def __init__(self):
        try:
            f = open(os.path.join(os.path.dirname(__file__),
                                  'config/networks.json'))
            s = f.read()
            self._data = json.loads(s)
            logger.debug('Loaded networks data')
        except:
            logger.error('Unable to load networks data')
            sys.exit(1)

    def get(self, key):
        return self._data.get(key)

auth_store = AuthStore()
network_store = NetworkStore()
