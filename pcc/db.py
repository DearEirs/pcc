import aiomysql
from settings import MYSQL_CONFIG as m


class Mysql:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,
                 host=m['host'],
                 user=m['user'],
                 password=m['password'],
                 port=m['port'],
                 db=m['db']):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db

    async def create_pool(self):
        self.pool = await aiomysql.create_pool(host=self.host,
                                               port=self.port,
                                               user=self.user,
                                               password=self.password,
                                               db=self.db)
        return self.pool

    async def execute(self, sql):
        if not hasattr(self, "pool"):
            await self.create_pool()
        async with self.pool.get() as conn:
            async with conn.cursor() as cur:
                result = await cur.execute(sql)
                return result
