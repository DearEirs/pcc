import asyncio
from aiomysql import create_pool
import aiomysql
import db


host = '192.168.1.130'
port = 3306
user = 'root'
password = 'root'
db = 'pcc'
loop = asyncio.get_event_loop()


async def list(uid, oid, cursor=0, page_size=10, is_friend=None):
    next_cursor = cursor + page_size
    select_social = "select user.uid, user.username from friend, favour \
        where favour.uid=friend.friend_id and favour.oid={oid}"
    select_others = "select user.uid, user.username from user, \
        favour where favour.oid={oid} limit {cursor}, {next_cursor}"

    friends = await db.mysql.excute(select_social)
    like_list = list(friends)

    if not is_friend:
        select_others.format(oid=oid, cursor=cursor, next_cursor=next_cursor)
        others = await db.mysql.excute(select_others)
        like_list = like_list.extend(others)

    return {"oid": oid, "like_list": like_list, "next_cursor": next_cursor}


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


async def count(oid):
    async with create_pool(host=host, port=port,
                           user=user, password=password,
                           db=db) as pool:
        async with pool.get() as conn:
            async with conn.cursor() as cur:
                await cur.execute("select oid, count(uid) from favour where oid=%s group by oid;", oid)
                value = await cur.fetchone()
                return {"oid": value[0],
                        "count": value[1]
                        }


async def is_like(uid, oid):
    async with create_pool(host=host, port=port,
                           user=user, password=password,
                           db=db) as pool:
        async with pool.get() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''SELECT uid, oid
                                  FROM  favour
                                  WHERE uid=%s AND oid=%s;''',(uid, oid))
                res = await cur.fetchone()
                if res:
                    return {'status':'yes'}
                else:
                    return {'status':'no'}


async def error():
    pass
