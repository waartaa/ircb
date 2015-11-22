import asyncio


class Connection(asyncio.Protocol):

    def decode(self, line):
        try:
            return line.decode()
        except UnicodeDecodeError:
            return line.decode("latin1")

    def normalize(self, line, ending='\r\n'):
        if not line.endswith(ending):
            line += ending
        return line

    def send(self, *args):
        message = self.normalize(" ".join(args))
        print('SEND', message.encode())
        self.transport.write(message.encode())
