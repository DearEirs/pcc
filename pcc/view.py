import asyncio
from aiomysql import create_pool

host = '192.168.1.130'
port = 3306
user = 'root'
password = 'root'
db = 'pcc'
loop = asyncio.get_event_loop()

async def list():
    pass


async def like(uid, oid):

    async with create_pool(host=host, port=port,
                           user=user, password=password,
                           db=db) as pool:
        async with pool.get() as conn:
            async with conn.cursor() as cur:
                uids = []   # 列表:存放所有的uid
                like_list = []  # 列表：存放oid所有的like用户
                # 查询like oid的所有uid
                await cur.execute("select uid from favour where oid = {}".format(oid))
                uids_ret = await cur.fetchall()
                for _ in uids_ret:
                    uids.append(_[0])   # 将查询的结果存到列表里

                # 如果对象没有被like过，则往favour表插入用户
                if uid not in uids:
                    await cur.execute("insert into favour values ('{}', '{}')".format(oid, uid))
                    uids.append(uid)

                    # 查询每个uid的uname
                    for each_uid in uids:
                        await cur.execute("select uname from user where uid = {}".format(each_uid))
                        uname = await cur.fetchone()
                        like_list.append({each_uid: uname[0]})

                    return {'oid': oid, 'uid': uid, 'like_list': like_list}

                else:   # 第二次 like 返回错误码
                    print('error')
                    error()











async def count():
    pass


async def is_like():
    pass


async def error():
    pass