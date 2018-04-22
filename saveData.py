import asyncio
from aiomysql import create_pool
import csv

host = '127.0.0.1'
port = 3306
user = 'root'
password = 'root'
db = 'pcc'

#如果表存在则删除
def delTable():
    async def req(table):
        async with create_pool(host=host, port=port,
                               user=user, password=password,
                               db=db, loop=loop) as pool:
            async with pool.get() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("DROP TABLE {}".format(table))
                    #value = await cur.fetchone()
                    #print(value)

    tables = ['object', 'friend', 'user', 'favour']
    loop = asyncio.get_event_loop()
    tasks = [req(table) for table in tables]     # 创建多个协程的列表，
    rets = loop.run_until_complete(asyncio.gather(*tasks))      # 将这些协程注册到事件循环中。



#使用预处理语句创建表
def createTable():
    Tuser = "CREATE TABLE user (uid  CHAR(20) NOT NULL, uname  CHAR(40))"

    Tfriend = "CREATE TABLE friend (uid  CHAR(20) NOT NULL, friend_id  CHAR(20))"

    Tobject = "CREATE TABLE object (oid  CHAR(20) NOT NULL)"

    Tlike = "CREATE TABLE favour (oid CHAR(20) NOT NULL, uid CHAR(20))"

    async def req(sql_table):
        async with create_pool(host=host, port=port,
                               user=user, password=password,
                               db=db, loop=loop) as pool:
            async with pool.get() as conn:
                async with conn.cursor() as cur:
                    print(sql_table)
                    await cur.execute(sql_table)

    sql_tables = [Tuser, Tfriend, Tobject, Tlike]
    loop = asyncio.get_event_loop()
    tasks = [req(sql_table) for sql_table in sql_tables]     # 创建多个协程的列表，
    rets = loop.run_until_complete(asyncio.gather(*tasks))      # 将这些协程注册到事件循环中。



# 插入数据
def insert():
    async def req(sql):
        async with create_pool(host=host, port=port,
                               user=user, password=password,
                               db=db, loop=loop) as pool:
                async with pool.get() as conn:
                    async with conn.cursor() as cur:
                        #print(sql)
                        await cur.execute(sql)

    user_list = []
    friends_list = []
    like_list = []

    # user_file = csv.reader(open(r'C:\Users\Asus\Desktop\py\py3\architecture\test\user.csv'))
    # for i, j in user_file:
    #     user_list.append("INSERT INTO user VALUES ('{}', '{}')".format(i, j))
    #
    #
    # friends_file = csv.reader(open(r'C:\Users\Asus\Desktop\py\py3\architecture\test\friends.csv'))
    # for i, j in friends_file:
    #     friends_list.append("INSERT INTO friend VALUES ('{}', '{}')".format(i, j))

    like_file = csv.reader(open(r'C:\Users\Asus\Desktop\py\py3\architecture\test\like.csv'))
    for i, *j in like_file:
        for _ in list(set(j)):
            like_list.append("INSERT INTO favour VALUES ('{}', '{}')".format(i, _))

    sql_insert = [user_list, friends_list, like_list]
    loop = asyncio.get_event_loop()
    for sql_list in sql_insert:
        print('insert data to tables')
        i = 0
        len_sql_list = len(sql_list)
        # 控制每次插入的数量
        while i < len_sql_list:
            print(i)
            j = i + 500 if i < len_sql_list else len_sql_list
            sqls = sql_list[i:j]
            i = j
            tasks = [req(sql) for sql in sqls]     # 创建多个协程的列表，
            loop.run_until_complete(asyncio.gather(*tasks))      # 将这些协程注册到事件循环中。


#delTable()
#createTable()
insert()