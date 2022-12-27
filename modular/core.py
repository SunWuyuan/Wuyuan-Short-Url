# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import make_response
import json

def getRequestParameter(request):
    parameters = {}
    if request.method == 'GET':
        parameters = request.args
    elif request.method == 'POST':
        parameters = request.form
        if not parameters:
            parameters = request.get_json()
    return dict(parameters)

def generateResponseResult(state, info):
    result = {
        'state': state,
        'info': info
    }
    result = json.dumps(result, ensure_ascii=False)
    response = make_response(result)
    response.mimetype = 'application/json; charset=utf-8'
    return response