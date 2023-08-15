from flask import Blueprint, request, Response, redirect
from module import core, auxiliary, database
import config
import time

API_APP = Blueprint('API_APP', __name__, url_prefix='/api')

@API_APP.route('/get_domain', methods=['GET', 'POST'])
def getDomain() -> Response:
    db = database.DataBase()
    return core.GenerateResponse().success(list(db.queryDomain().keys()))

@API_APP.route('/generate', methods=['GET', 'POST'])
def generate() -> Response:
    parameter = core.getRequestParameter(request)
    domain = parameter.get('domain')
    longUrl = parameter.get('longUrl')
    signature = parameter.get('signature')
    validDay = parameter.get('validDay', '0')

    if not domain or not longUrl:
        return core.GenerateResponse().error(110, '参数不能为空')
    elif not auxiliary.isUrl(longUrl):
        return core.GenerateResponse().error(110, 'longUrl需完整')
    elif validDay:
        if not validDay.isdigit():
            return core.GenerateResponse().error(110, 'validDay仅能为数字')
        validDay = int(validDay)
        if validDay < 0 or validDay > 365:
            return core.GenerateResponse().error(110, 'validDay仅能填0~365,0代表永久')
    
    db = database.DataBase()
    
    domains = db.queryDomain()
    if domain not in domains:
        return core.GenerateResponse().error(110, 'domain不存在')
    if config.AUTOMATIC:
        protocol = 'https'
    else:
        protocol = domains[domain]
    
    if signature:
        if not signature.isdigit() and not signature.isalpha() and not signature.isalnum():
            return core.GenerateResponse().error(110, 'signature仅能为数字和字母')
        elif len(signature) < 1 or len(signature) > 5:
            return core.GenerateResponse().error(110, 'signature长度仅能为1~5')
        elif signature.lower() == 'api':
            return core.GenerateResponse().error(110, 'signature不能为api')
        elif signature.lower() == 'index':
            return core.GenerateResponse().error(110, 'signature不能为index')
        elif signature.lower() == 'query':
            return core.GenerateResponse().error(110, 'signature不能为query')
        elif db.queryUrlBySignature(domain, signature):
            return core.GenerateResponse().error(110, 'signature已存在')
        
        id_ = db.insertUrl(core.Type.CUSTOM, domain, longUrl, validDay)
    else:
        query = db.queryUrlByLongUrl(domain, longUrl)
        if query:
            return core.GenerateResponse().success(f'{protocol}://{domain}/{query["signature"]}')
        
        id_ = db.insertUrl(core.Type.SYSTEM, domain, longUrl, validDay)
        signature = auxiliary.base62Encode(id_)
        if db.queryUrlBySignature(domain, signature):
            signature += 'a'
    db.updateUrl(id_, signature)
    return core.GenerateResponse().success(f'{protocol}://{domain}/{signature}')

@API_APP.route('/get', methods=['GET', 'POST'])
def get() -> Response:
    parameter = core.getRequestParameter(request)
    shortUrl = parameter.get('shortUrl')

    if not shortUrl:
        return core.GenerateResponse().error(110, '参数不能为空')
    elif not auxiliary.isUrl(shortUrl):
        return core.GenerateResponse().error(110, 'shortUrl需要完整')

    shortUrl = shortUrl.split('/')
    domain = shortUrl[2]
    signature = shortUrl[3]

    db = database.DataBase()

    if domain not in db.queryDomain():
        return core.GenerateResponse().error(110, 'shortUrl错误')
    query = db.queryUrlBySignature(domain, signature)
    if not query:
        return core.GenerateResponse().error(110, 'shortUrl错误')

    info = {
        'longUrl': query['long_url'],
        'validDay': query['valid_day'],
        'count': query['count'],
        'timestamp': query['timestamp']
    }
    return core.GenerateResponse().success(info)

@API_APP.route('/<signature>', methods=['GET', 'POST'])
@API_APP.route('/<signature>/', methods=['GET', 'POST'])
def shortUrlRedirect(signature) -> Response:
    db = database.DataBase()

    query = db.queryUrlBySignature(request.host, signature)
    if not query:
        return redirect(request.host_url)
    validDay = query['valid_day']
    if validDay != 0:
        validDayTimestamp = validDay * 86400000
        expireTimestamp = query['timestamp'] + validDayTimestamp
        if int(time.time()) > expireTimestamp:
            db.deleteUrl(query['id'])
            return redirect(request.host_url)

    db.addUrlCount(request.host, signature)
    return redirect(query['long_url'])