#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sanic import Sanic
from sanic import response
import view


func_dict = {
    'list': view.list,
    'like': view.like,
    'count': view.count,
    'is_like': view.is_like
}


app = Sanic()


@app.route("/pcc", methods=['GET'])
async def dispatch(request):
    action = request.args.get('action')
    if not action:
        result = {
            "error_code": "101",
            "error_message": "未能提供正确的参数, 请检查参数后重新发起请求"
        }
        return response.json(result)

    oid = request.args.get('oid')
    if action == 'like' or action == 'is_like':
        uid = request.args.get('uid')
        action = func_dict[action]
        result = await action(uid, oid)

    elif action == 'count':
        action = func_dict[action]
        result = await action(oid)

    elif action == 'list':
        uid = request.args.get('uid')
        cursor = request.args.get('cursor')
        page_size = request.args.get('page_size')
        is_friend = request.args.get('is_friend')

        action = func_dict[action]
        result = await action(uid, oid, cursor, page_size, is_friend)

    return response.json(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
