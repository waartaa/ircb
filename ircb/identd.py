#!/usr/bin/env python

from ircb.storeclient import NetworkStore

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = '0.0.0.0'
port = 8001
s.bind((host, port))
s.listen(5)

while True:
    c, addr = s.accept()
    data = c.recv(4096)

    lport, rport = [_.strip() for _ in data.split(',')]

    result = yield from NetworkStore.get({'query':{'lport': lport,
                                                   'rport': rport}})
    print(result)
