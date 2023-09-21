from flask import Blueprint, render_template, request, redirect, Response
from module import database
import datetime

PAGE_APP = Blueprint('PAGE_APP', __name__)

@PAGE_APP.get('/')
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

@PAGE_APP.get('/query')
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