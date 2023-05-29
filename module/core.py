# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from typing import Any
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
        self.code = 0
        self.message = ''
        self.data = None

    def generate(self) -> Response:
        responseJSON = json.dumps({
            'code': self.code,
            'message': self.message,
            'data': self.data
        }, ensure_ascii=False)
        response_ = make_response(responseJSON)
        response_.mimetype = 'application/json; charset=utf-8'
        return response_

    def error(self, code: int, message: str) -> Response:
        self.code = code
        self.message = message
        return self.generate()

    def success(self, data: Any) -> Response:
        self.code = 200
        self.message = 'success'
        self.data = data
        return self.generate()