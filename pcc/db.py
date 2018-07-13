import aiomysql
import settings


config = settings.MYSQL_CONFIG


class Mysql:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,
                 host=config['host'],
                 user=config['user'],
                 password=config['password'],
                 port=config['port'],
                 db=config['db']):
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

    async def get_conn(self):
        if not hasattr(self, "pool"):
            await self.create_pool()
        return self.pool.get()
