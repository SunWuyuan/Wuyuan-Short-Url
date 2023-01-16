# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, redirect, request
from modular import core, auxiliary, database
import config
import time

API_APP = Blueprint('API_APP', __name__)

@API_APP.route('/api/generate', methods=['GET', 'POST'])
def generate():
    parameter = core.getRequestParameter(request)
    domain = parameter.get('domain')
    longUrl = parameter.get('longUrl')
    signature = parameter.get('signature')
    validDay = parameter.get('validDay') or 0

    if not domain or not longUrl or (validDay and (type(validDay) == str and not validDay.isdigit())):
        return core.GenerateResponseResult().error(110, '参数错误')
    elif not auxiliary.isUrl(longUrl):
        return core.GenerateResponseResult().error(110, '长网址需完整')
    elif validDay:
        validDay = int(validDay)
        if validDay < 0 or validDay > 365:
            return core.GenerateResponseResult().error(110, '仅能填0~365,0代表永久')
    
    db = database.DataBase()

    domains = db.queryDomain()

    if domain not in domains:
        return core.GenerateResponseResult().error(110, '域名错误')
    
    if config.AUTOMATIC:
        protocol = 'https'
    else:
        protocol = domains.get(domain)

    if signature:
        if not signature.isdigit() and not signature.isalpha() and not signature.isalnum():
            return core.GenerateResponseResult().error(110, '特征码仅能为数字和字母')
        elif len(signature) < 1 or len(signature) > 5:
            return core.GenerateResponseResult().error(110, '特征码长度仅能为1~5')
        elif signature.lower() == 'api':
            return core.GenerateResponseResult().error(110, '特征码不能为api')
        elif signature.lower() == 'index':
            return core.GenerateResponseResult().error(110, '特征码不能为index')
        elif signature.lower() == 'query':
            return core.GenerateResponseResult().error(110, '特征码不能为query')
        elif signature.lower() == 'doc':
            return core.GenerateResponseResult().error(110, '特征码不能为doc')
        elif db.queryUrlBySignature(domain, signature):
            return core.GenerateResponseResult().error(110, '特征码已存在')
        
        id_ = db.insert('custom', domain, longUrl, validDay)
        db.update(id_, signature)

        return core.GenerateResponseResult().success(f'{protocol}://{domain}/{signature}')
    else:
        query = db.queryUrlByLongUrl(domain, longUrl)
        if query:
            return core.GenerateResponseResult().success(f'{protocol}://{domain}/{query.get("signature")}')
        
        id_ = db.insert('system', domain, longUrl, validDay)
        signature = auxiliary.base62Encode(id_)
        if db.queryUrlBySignature(domain, signature):
            signature += 'a'
        db.update(id_, signature)

        return core.GenerateResponseResult().success(f'{protocol}://{domain}/{signature}')

@API_APP.route('/api/get_domain', methods=['GET', 'POST'])
def getDomain():
    db = database.DataBase()
    return core.GenerateResponseResult().success(list(db.queryDomain().keys()))

@API_APP.route('/api/get', methods=['GET', 'POST'])
def get():
    parameter = core.getRequestParameter(request)
    shortUrl = parameter.get('shortUrl')

    if not shortUrl:
        return core.GenerateResponseResult().error(110, '参数错误')
    elif not auxiliary.isUrl(shortUrl):
        return core.GenerateResponseResult().error(110, '短网址需要完整')

    shortUrl = shortUrl.split('/')
    domain = shortUrl[2]
    signature = shortUrl[3]

    db = database.DataBase()

    if domain not in db.queryDomain():
        return core.GenerateResponseResult().error(110, '短网址错误')
    query = db.queryUrlBySignature(domain, signature)
    if not query:
        return core.GenerateResponseResult().error(110, '短网址错误')
    
    info = {
        'longUrl': query.get('long_url'),
        'validDay': query.get('valid_day'),
        'count': query.get('count'),
        'timestmap': query.get('timestmap')
    }
    return core.GenerateResponseResult().success(info)

@API_APP.route('/<signature>', methods=['GET', 'POST'])
@API_APP.route('/<signature>/', methods=['GET', 'POST'])
def shortUrlRedirect(signature):
    db = database.DataBase()
    
    query = db.queryUrlBySignature(request.host, signature)
    if query:
        validDay = query.get('valid_day')
        if validDay:
            validDayTimestamp = validDay * 86400000
            expireTimestmap = query.get('timestmap') + validDayTimestamp
            if int(time.time()) > expireTimestmap:
                db.delete(query.get('id'))
                return redirect(request.host_url)
        
        db.addCount(request.host, signature)
        return redirect(query.get('long_url'))
    return redirect(request.host_url)