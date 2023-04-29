# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, render_template, request, redirect
from module import database
import datetime
import time

PAGE_APP = Blueprint('PAGE_APP', __name__)

@PAGE_APP.route('/', methods=['GET', 'POST'])
def generate() -> str:
    db = database.DataBase()
    info = db.queryWebsiteInfo()
    return render_template(
        'generate.html',
        title=info['title'],
        keyword=info['keyword'],
        description=info['description'],
        nowYear=datetime.datetime.now().year
    )

@PAGE_APP.route('/query', methods=['GET', 'POST'])
def query() -> str:
    db = database.DataBase()
    info = db.queryWebsiteInfo()
    return render_template(
        'query.html',
        title=info['title'],
        keyword=info['keyword'],
        description=info['description'],
        nowYear=datetime.datetime.now().year
    )

@PAGE_APP.route('/<signature>', methods=['GET', 'POST'])
@PAGE_APP.route('/<signature>/', methods=['GET', 'POST'])
def shortUrlRedirect(signature) -> str:
    db = database.DataBase()
    
    query = db.queryUrlBySignature(request.host, signature)
    if query:
        validDay = query['valid_day']
        if validDay != 0:
            validDayTimestamp = validDay * 86400000
            expireTimestmap = query['timestmap'] + validDayTimestamp
            if int(time.time()) > expireTimestmap:
                db.delete(query['id'])
                return redirect(request.host_url)
        
        db.addCount(request.host, signature)
        return redirect(query['long_url'])
    return redirect(request.host_url)