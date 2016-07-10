# -*- coding: utf-8 -*-
from ircb.publishers.logs import MessageLogPublisher

if __name__ == '__main__':
    import asyncio
    import sys
    from ircb.storeclient import initialize
    from ircb.utils.config import load_config
    load_config()
    initialize()
    try:
        hostname = sys.argv[1]
        roomname = sys.argv[2]
        user_id = sys.argv[3]
    except:
        print("Usage: __init__.py '<hostname>' '<roomname>' '<user_id>'")
        sys.exit(1)
    publisher = MessageLogPublisher(hostname, roomname, int(user_id))
    publisher.run()
    loop = asyncio.get_event_loop()
    loop.run_forever()
