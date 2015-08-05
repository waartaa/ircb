import os
import json
import logging
import sys
from collections import OrderedDict

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


class NetworkMessageStore(object):

    def __init__(self):
        self._data = OrderedDict()

    def get_key_value(self, line):
        key, value = None, None
        words = line.split(' ')
        code = words[1]
        if code in ('001', '251'):
            key, value = code, line
            value = line
            self._data[code] = line
        elif words[1] == 'JOIN':
            key = '{}-{}'.format('JOIN', words[2])
            # words[0] = words[0].split('!')[0]
            value = ' '.join(words)
        elif words[1] == 'PART':
            key = '{}-{}'.format('JOIN', words[2])
            value = None
        return key, value

    def update(self, data):
        lines = data.splitlines()
        for line in lines:
            key, value = self.get_key_value(line)
            if key:
                self._data.pop(key, None)
            if value:
                self._data[key] = value

    def get_all(self):
        data = []
        for key, value in self._data.items():
            data.append(value)
        return '\r\n'.join(data)
