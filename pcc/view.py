import db
from log import Log

db_mysql = db.Mysql()


async def like(uid, oid):
    '''
    对一个对象（一条feed、文章、或者url）进行 like 操作，禁止 like 两次，第二次 like 返回错误码
    :param uid:用户ID
    :param oid:对象ID
    :return:
    '''
    connnetct = await db_mysql.conn()
    async with connnetct as conn:
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
                    if uname:
                        like_list.append({each_uid: uname[0]})

                    else:
                        like_list.append({each_uid: None})
                return {'oid': oid, 'uid': uid, 'like_list': like_list[:20]}

            else:   # 第二次 like 返回错误码
                content = 'object already been liked.'
                Log().recordLog(content)
                result = await error(oid, uid, content)
                return result

async def is_like(uid, oid):
    '''
    返回参数指定的对象有没有被当前用户 like 过
    :param uid:用户ID
    :param oid:对象ID
    :return:
    '''
    connnetct = await db_mysql.conn()
    async with connnetct as conn:
        async with conn.cursor() as cur:
            await cur.execute('''SELECT uid, oid
                              FROM  favour
                              WHERE uid=%s AND oid=%s;''',(uid, oid))
            status = await cur.fetchone()
            if status:
                return {'oid': oid, 'uid': uid, 'is_like': '1'}
            else:
                return {'oid': oid, 'uid': uid, 'is_like': '0'}

async def count(oid):
    '''
    一个对象的 like 计数
    :param oid:
    :return:
    '''
    connnetct = await db_mysql.conn()
    async with connnetct as conn:
        async with conn.cursor() as cur:
            await cur.execute("select oid, count(uid) from favour where oid={} group by oid;".format(oid))
            value = await cur.fetchone()
            if value:
                return {"oid": value[0],
                        "count": value[1]
                        }
            else:
                content = 'the oid is not exist'
                Log().recordLog(content)
                result = await error(oid, None, content)
                return result

async def list(uid, oid, cursor=0, page_size=10, is_friend=0):
    '''
    :param uid:
    :param oid:
    :param cursor:起始位置,取上次返回结果的next_cursor
    :param page_size:返回的列表长度
    :param is_friend:是否仅返回只是好友的uid列表
    :return:
    '''
    connnetct = await db_mysql.conn()
    async with connnetct as conn:
        async with conn.cursor() as cur:
            cursor = 0 if not cursor else cursor
            page_size = 10 if not page_size else page_size
            is_friend = 0 if not is_friend else is_friend
            next_cursor = int(cursor) + int(page_size)
            result = {'oid': oid, 'next_cursor': next_cursor}
            if is_friend == '1':
                uid_sql = ('select uid from favour where oid={0} and '
                       'uid in (select friend_id from friend where uid={1})'.format(oid, uid))
                await cur.execute(uid_sql)
                rets = await cur.fetchall()
                uids = ''
                for _ in rets:
                    uids += _[0] + ','
                sql = ('select uid, uname from user where uid in ({}) limit {},{}'.format(uids[:-1], cursor, next_cursor))
            else:
                sql = 'select uid, uname from user where uid in (select uid from favour) limit {0},{1}'.format(cursor, next_cursor)
            print(sql)
            await cur.execute(sql)
            like_list = await cur.fetchall()
            result['like_list'] = like_list
            return result

async def error(oid, uid, content):
    return {"error_code": 501,
        "error_message": content,
        "oid": oid,
        "uid": uid
        }