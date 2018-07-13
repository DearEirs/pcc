import aiomysql

import db


database = db.Mysql()


async def list(uid, oid, cursor=0, page_size=10, is_friend=0):
    cursor = 0 if not cursor else cursor
    page_size = 10 if not page_size else page_size
    is_friend = 0 if not is_friend else is_friend
    next_cursor = cursor + page_size
    result = {'oid': oid, 'next_cursor': next_cursor}

    if is_friend:
        sql = ('select uid, name from user where '
               'uid in (select fid from friend where uid={0}) and '
               'uid in (select uid from favour where oid={1}) limit {2},{3}'.format(uid, oid, cursor, next_cursor))
    else:
        sql = 'select uid, name from user where uid in (select uid from favour) limit {0},{1}'.format(cursor, next_cursor)

    print(sql)
    connection = await database.get_conn()
    async with connection as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            like_list = await cur.fetchall()
            result['like_list'] = like_list
            return result


async def like(uid, oid):
    result = {'oid': oid, 'uid': uid}
    connection = await database.get_conn()
    async with connection as conn:
        async with conn.cursor() as cur:
            # 查询用户与对象的like关系
            await cur.execute("select uid from favour where oid={0}".format(oid))
            is_like = await cur.fetchall()
            # 如果对象没有被like过，则往favour表插入用户
            if is_like:
                result['message'] = '{0} is already like {1}'.format(uid, oid)
            else:
                await cur.execute("insert into favour values ('{0}', '{1}')".format(oid, uid))
                # 返回对象like列表
                await cur.execute("select uid, name from user where uid in (select uid from favour where oid={}) limit 20".format(oid))
                like_list = await cur.fetchall()
                result['like_list'] = like_list
            return result


async def count(oid):
    connection = await database.get_conn()
    async with connection as conn:
        async with conn.cursor() as cur:
            await cur.execute("select count(oid) from favour where oid={0};".format(oid))
            count = await cur.fetchone()
            count = count[0]
            return {"oid": oid, "count": count}


async def is_like(uid, oid):
    result = {'oid': oid, 'uid': uid}
    connection = await database.get_conn()
    async with connection as conn:
        async with conn.cursor() as cur:
            await cur.execute("select uid from  favour where oid={0}".format(oid))
            is_like = await cur.fetchall()
            result['is_like'] = 1 if is_like else 0
            return result
