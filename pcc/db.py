import aiomysql
from settings import MYSQL_CONFIG as conf


class Mysql:
    def __init__(self,
                 host=conf['host'],
                 user=conf['username'],
                 password=conf['password'],
                 port=conf['port'],
                 db=conf['db']):
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

    async def conn(self):
        if not hasattr(self, "pool"):
            await self.create_pool()
        return self.pool.get()
