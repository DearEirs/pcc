import aiomysql

import db


database = db.Mysql()


async def list(uid, oid, cursor=0, page_size=10, is_friend=0):
    next_cursor = cursor + page_size
    result = {'oid': oid, 'next_cursor': next_cursor}

    if is_friend:
        sql = ('select uid, name from user where '
               'uid in (select fid from friend where uid={}) and'
               'uid in (select uid from favour where oid={})'.format(uid, oid))
    else:
        sql = 'select uid, name from user where uid in (select uid from favour limit {} {})'.format(cursor, next_cursor)

    async with database.get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql)
            like_list = await cur.fetchall()
            result['like_list'] = like_list
            return result


async def like(uid, oid):
    result = {'oid': oid, 'uid': uid}
    async with database.get_conn() as conn:
        async with conn.cursor() as cur:
            # 查询用户与对象的like关系
            await cur.execute("select uid from favour where oid={0}".format(oid))
            is_like = await cur.fetchall()
            # 如果对象没有被like过，则往favour表插入用户
            if is_like:
                result['message'] = '{} is already like {}'.format(uid, oid)
            else:
                await cur.execute("insert into favour values ('{0}', '{1}')".format(oid, uid))
                # 返回对象like列表
                await cur.execute("select uid, name from user where uid in (select uid from favour where oid={} limit 20)".format(oid))
                like_list = await cur.fetchall()
                result['like_list'] = like_list
            return result


async def count(oid):
    async with database.get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute("select oid, count(uid) from favour where oid={};".format(oid))
            oid, count = await cur.fetchone()
            return {"oid": oid, "count": count}


async def is_like(uid, oid):
    result = {'oid': oid, 'uid': uid}
    async with database.get_conn() as conn:
        async with conn.cursor() as cur:
            await cur.execute("select uid from  favour where oid={0}".format(oid))
            is_like = await cur.fetchall()
            result['is_like'] = 1 if is_like else 0
            return result
