from collections import OrderedDict


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
