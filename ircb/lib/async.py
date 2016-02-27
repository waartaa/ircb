import asyncio


def coroutinize(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        coro = asyncio.coroutine(func)
        loop.run_until_complete(coro(*args, **kwargs))
        from ircb.storeclient.base import dispatcher
        loop.run_until_complete(dispatcher.stop())
        loop.close()
    return wrapper
