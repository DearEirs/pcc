#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sanic import Sanic
from sanic import response

import actions


func_dict = {
    'list': actions.list,
    'like': actions.like,
    'count': actions.count,
    'is_like': actions.is_like
}


app = Sanic()


@app.route("/pcc", methods=['GET'])
async def dispatch(request):
    '''根据提交的参数分发请求'''
    action = request.args.get('action')
    if not action:
        result = {
            "error_code": "101",
            "error_message": "未能提供正确的参数, 请检查参数后重新发起请求"
        }
        return response.json(result)
    
    oid = request.args.get('oid')
    if action == 'list':
        uid = request.args.get('uid')
        cursor =  request.args.get('cursor')
        page_size = request.args.get('page_size')
        is_friend = request.args.get('is_friend')

        action = func_dict[action]
        result = await action(uid, oid, cursor, page_size, is_friend)
        
    elif action == 'like' or action == 'is_like':
        uid = request.args.get('uid')
        action = func_dict[action]
        result = await action(uid, oid)
        
    elif action == 'count':
        action = func_dict[action]
        result = await action(oid)

    return response.json(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
