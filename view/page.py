# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Blueprint, render_template
from modular import database
import datetime

PAGE_APP = Blueprint('PAGE_APP', __name__)

@PAGE_APP.route('/', methods=['GET', 'POST'])
def generate():
    db = database.DataBase()
    info = db.queryWebsiteInfo()
    return render_template(
        'generate.html',
        title=info.get('title'),
        keyword=info.get('keyword'),
        description=info.get('description'),
        nowYear=datetime.datetime.now().year
    )

@PAGE_APP.route('/query', methods=['GET', 'POST'])
def query():
    db = database.DataBase()
    info = db.queryWebsiteInfo()
    return render_template(
        'query.html',
        title= info.get('title'),
        keyword=info.get('keyword'),
        description=info.get('description'),
        nowYear=datetime.datetime.now().year
    )

@PAGE_APP.route('/doc', methods=['GET', 'POST'])
def doc():
    db = database.DataBase()
    info = db.queryWebsiteInfo()
    return render_template(
        'doc.html',
        title= info.get('title'),
        keyword=info.get('keyword'),
        description=info.get('description'),
        nowYear=datetime.datetime.now().year
    )