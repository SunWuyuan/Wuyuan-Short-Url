from flask import Blueprint, request, Response
from module import core, auxiliary, model, database_type
import config

API_APP = Blueprint('API_APP', __name__, url_prefix='/api')

@API_APP.get('/get_domain')
def getDomain() -> Response:
    data = [item.domain for item in model.Domain.query.all()]
    return core.GenerateResponse().success(data)

@API_APP.post('/generate')
def generate() -> Response:
    parameter = request.get_json()
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

    domain_ = model.Domain.query.filter_by(domain=domain).first()
    if not domain_:
        return core.GenerateResponse().error(110, 'domain不存在')
    if config.AUTOMATIC:
        protocol = 'https'
    else:
        protocol = model.Domain.query.filter_by(id=domain_.id).first().protocol
        if database_type.Domain(protocol) == database_type.Domain.HTTP:
            protocol = 'http'
        else:
            protocol = 'https'
    
    if signature:
        #if not signature.isdigit() and not signature.isalpha() and not signature.isalnum():
        #    return core.GenerateResponse().error(110, 'signature仅能为数字和字母')
        if len(signature) < 1 or len(signature) > 10:
            return core.GenerateResponse().error(110, '特征码长度仅能为1~10')
        elif signature.lower() == 'api':
            return core.GenerateResponse().error(110, '特征码不能为api')
        elif signature.lower() == 'index':
            return core.GenerateResponse().error(110, '特征码不能为index')
        elif signature.lower() == 'query':
            return core.GenerateResponse().error(110, '特征码不能为query')
        elif model.Url.query.filter_by(domain_id=domain_.id, signature=signature).first():
            return core.GenerateResponse().error(110, '特征码已存在')

        url = model.Url(type_=database_type.Url.CUSTOM, domain_id=domain_.id, long_url=longUrl, valid_day=validDay, signature=signature)
        model.DB.session.add(url)
        model.DB.session.commit()
    else:
        url = model.Url.query.filter_by(domain_id=domain_.id, long_url=longUrl).first()
        if url:
            return core.GenerateResponse().success(f'{protocol}://{domain}/{url.signature}')
        
        url = model.Url(type_=database_type.Url.CUSTOM, domain_id=domain_.id, long_url=longUrl, valid_day=validDay)
        model.DB.session.add(url)
        model.DB.session.commit()

        id_ = model.Url.query.filter_by(domain_id=domain_.id, long_url=longUrl).first().id
        signature = auxiliary.base62Encode(id_)
        if model.Url.query.filter_by(domain_id=domain_.id, signature=signature).first():
            signature += 'a'
        url = model.Url.query.filter_by(id=id_).first()
        url.signature = signature
        model.DB.session.commit()
    return core.GenerateResponse().success(f'{protocol}://{domain}/{signature}')

@API_APP.get('/get')
def get() -> Response:
    parameter = request.args
    domain = parameter.get('domain')
    signature = parameter.get('signature')
    if not domain or not signature:
        return core.GenerateResponse().error(110, '参数不能为空')

    domain_ = model.Domain.query.filter_by(domain=domain).first()
    if not domain_:
        return core.GenerateResponse().error(110, 'shortUrl错误')
    url = model.Url.query.filter_by(domain_id=domain_.id, signature=signature).first()
    if not url:
        return core.GenerateResponse().error(110, 'shortUrl错误')

    info = {
        'longUrl': url.long_url,
        'validDay': url.valid_day,
        'count': url.count,
        'creationTimestamp': url.creation_timestamp
    }
    return core.GenerateResponse().success(info)
