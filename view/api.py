# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, request
from modular import core, auxiliary, database
import config

API_APP = Blueprint('API_APP', __name__, url_prefix='/api')

@API_APP.route('/generate', methods=['GET', 'POST'])
def generate():
    parameter = core.getRequestParameter(request)
    domain = parameter.get('domain')
    longUrl = parameter.get('longUrl')
    signature = parameter.get('signature')
    validDay = parameter.get('validDay') or 0

    if not domain or not longUrl or (validDay and (type(validDay) == str and not validDay.isdigit())):
        return core.GenerateResponse().error(110, '参数不能为空')
    elif not auxiliary.isUrl(longUrl):
        return core.GenerateResponse().error(110, '长网址需完整')
    elif validDay:
        validDay = int(validDay)
        if validDay < 0 or validDay > 365:
            return core.GenerateResponse().error(110, '仅能填0~365,0代表永久')
    
    db = database.DataBase()

    domains = db.queryDomain()
    if domain not in domains:
        return core.GenerateResponse().error(110, '域名错误')
    if config.AUTOMATIC:
        protocol = 'https'
    else:
        protocol = domains.get(domain)

    if signature:
        if not signature.isdigit() and not signature.isalpha() and not signature.isalnum():
            return core.GenerateResponse().error(110, '特征码仅能为数字和字母')
        elif len(signature) < 1 or len(signature) > 5:
            return core.GenerateResponse().error(110, '特征码长度仅能为1~5')
        elif signature.lower() == 'api':
            return core.GenerateResponse().error(110, '特征码不能为api')
        elif signature.lower() == 'index':
            return core.GenerateResponse().error(110, '特征码不能为index')
        elif signature.lower() == 'query':
            return core.GenerateResponse().error(110, '特征码不能为query')
        elif signature.lower() == 'doc':
            return core.GenerateResponse().error(110, '特征码不能为doc')
        elif db.queryUrlBySignature(domain, signature):
            return core.GenerateResponse().error(110, '特征码已存在')
        
        id_ = db.insert('custom', domain, longUrl, validDay)
    else:
        query = db.queryUrlByLongUrl(domain, longUrl)
        if query:
            return core.GenerateResponse().success(f'{protocol}://{domain}/{query.get("signature")}')
        
        id_ = db.insert('system', domain, longUrl, validDay)
        signature = auxiliary.base62Encode(id_)
        if db.queryUrlBySignature(domain, signature):
            signature += 'a'
    db.update(id_, signature)
    return core.GenerateResponse().success(f'{protocol}://{domain}/{signature}')

@API_APP.route('/get_domain', methods=['GET', 'POST'])
def getDomain():
    db = database.DataBase()
    return core.GenerateResponse().success(list(db.queryDomain().keys()))

@API_APP.route('/get', methods=['GET', 'POST'])
def get():
    parameter = core.getRequestParameter(request)
    shortUrl = parameter.get('shortUrl')

    if not shortUrl:
        return core.GenerateResponse().error(110, '参数错误')
    elif not auxiliary.isUrl(shortUrl):
        return core.GenerateResponse().error(110, '短网址需要完整')

    shortUrl = shortUrl.split('/')
    domain = shortUrl[2]
    signature = shortUrl[3]

    db = database.DataBase()

    if domain not in db.queryDomain():
        return core.GenerateResponse().error(110, '短网址错误')
    query = db.queryUrlBySignature(domain, signature)
    if not query:
        return core.GenerateResponse().error(110, '短网址错误')
    
    info = {
        'longUrl': query.get('long_url'),
        'validDay': query.get('valid_day'),
        'count': query.get('count'),
        'timestmap': query.get('timestmap')
    }
    return core.GenerateResponse().success(info)