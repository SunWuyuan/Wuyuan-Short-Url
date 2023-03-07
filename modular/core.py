# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import request, make_response, Response
import json

def getRequestParameter(request: request) -> dict:
    data = {}
    if request.method == 'GET':
        data = request.args
    elif request.method == 'POST':
        data = request.form
        if not data:
            data = request.get_json()
    return dict(data)

class GenerateResponse:
    def __init__(self) -> None:
        self.response = {}

    def _json(self) -> Response:
        responseJSON = json.dumps(self.response, ensure_ascii=False)
        response_ = make_response(responseJSON)
        response_.mimetype = 'application/json; charset=utf-8'
        return response_

    def error(self, code: int, message: str) -> Response:
        self.response = {
            'code': code,
            'message': message
        }
        return self._json()

    def success(self, data) -> Response:
        self.response = {
            'code': 200,
            'message': 'success',
            'data': data
        }
        return self._json()