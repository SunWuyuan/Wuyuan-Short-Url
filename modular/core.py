# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import make_response
import json

def getRequestParameter(request):
    data = {}
    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = request.form
        if not data:
            data = request.get_json()
    return dict(data)

class GenerateResponseResult:
    def __init__(self):
        pass

    def _json(self):
        result = json.dumps(self.result)
        response = make_response(result)
        response.mimetype = 'application/json; charset=utf-8'
        return response

    def custom(self, contentType, data):
        response = make_response(data)
        response.headers['Content-Type'] = contentType
        return response

    def success(self, data):
        result = {
            'code': 200,
            'message': '成功',
            'data': data
        }
        self.result = result
        return self._json()

    def error(self, code, message):
        result = {
            'code': code,
            'message': message
        }
        self.result = result
        return self._json()