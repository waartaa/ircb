import asyncio
import aioredis


class Redis():
    """
    Wrapper around aioredis library to talk to redis. It provides some
    higher level utility methods to interact with redis as a cache or
    as a data structure code.
    """
    SUPPORTED_METHODS = set([
        'set',
        'get',
        'sadd',
        'smembers',
        'delete'
    ])

    def __init__(self, host='127.0.0.1', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self._initialized = False

    async def init(self, reset=False):
        """
        Initialize redis connections

        Args:
            reset (bool): Whether to reset redis connection
        """
        if not self._initialized or reset:
            # redis connection to reade/write
            self.conn = await aioredis.create_redis(
                (self.host, self.port), db=self.db)
            # redis connection to subscribe
            self.sub = await aioredis.create_redis(
                (self.host, self.port), db=self.db)
            self._initialized = True

    async def subscribe(self, pattern, handler):
        """
        Subscribe for a pattern from Redis

        Args:
            pattern (str): Pattern to subscribe to
            handler (func): Handler to handle published message

        Returns:
            Task object running the handler function
        """
        res = await self.sub.subscribe(pattern)
        ch = res[0]
        return asyncio.ensure_future(handler(pattern, ch))

    async def watch(self, key, handler):
        """
        Watch a redis key for change events.

        Args:
            key (str): Name of key
            handler (func): Handler function to handle key change

        Returns:
            A task object running the handler
        """
        res = await self.sub.subscribe('__keyspace@0__:{}'.format(key))
        ch = res[0]
        return asyncio.ensure_future(handler(key, ch))

    def __getattr__(self, key):
        """
        Interface select redis operations from redis connection
        object to this instance.
        """
        val = None
        if key not in self.SUPPORTED_METHODS:
            raise AttributeError(
                'RedisError: Key: "{}" not supported'.format(key))
        if key in ('subscribe',):
            val = getattr(self.sub, key)
        else:
            val = getattr(self.conn, key)
        if val:
            setattr(self, key, val)
            return val

    def close(self):
        """Close redis connections"""
        self.conn.close()
        self.sub.close()


redis = Redis()


def main():
    loop = asyncio.get_event_loop()

    async def reader(key, ch):
        while (await ch.wait_message()):
            msg = await ch.get()
            print("Got Message:", msg)
            val = await redis.smembers(key)
            print(val)

    async def go():
        await redis.init()
        tsk = await redis.watch('mykey', reader)
        await redis.sadd('mykey', 1, 2, 3, 7)
        print(await redis.smembers('mykey'))
        await redis.delete('mykey')
        await tsk
        redis.close()

    loop.run_until_complete(go())

if __name__ == '__main__':
    main()
