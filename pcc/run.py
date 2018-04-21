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
async def test(request):
    action = request.args.get('action')
    uid = request.args.get('uid')
    oid = request.args.get('oid')

    if not all((action, oid)):
        result = {
            "error_code": "501",
            "error_message": "Incorrect parameter!"
        }
        return response.json(result)

    action = func_dict[action]
    result = await action(oid)
    return response.json(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
