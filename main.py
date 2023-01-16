# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Flask
import flask_cors
import config
from modular import database, core
from view.api import API_APP
from view.page import PAGE_APP

app = Flask(__name__)
flask_cors.CORS(app, resources=r'/*')
app.register_blueprint(API_APP)
app.register_blueprint(PAGE_APP)

@app.errorhandler(500)
def errorhandler500(error):
    return core.GenerateResponseResult().error(500, '未知错误')

def initialization():
    print('''
 _   _ ____   ___    ____  _                _     _   _      _ 
| | | |___ \ / _ \  / ___|| |__   ___  _ __| |_  | | | |_ __| |
| |_| | __) | | | | \___ \| '_ \ / _ \| '__| __| | | | | '__| |
|  _  |/ __/| |_| |  ___) | | | | (_) | |  | |_  | |_| | |  | |
|_| |_|_____|\___/  |____/|_| |_|\___/|_|   \__|  \___/|_|  |_|
    ''')

    db = database.DataBase()
    if not db.existenceTable('core'):
        db.createCoreTable()
    if not db.existenceTable('domain'):
        db.createDomainTable()
    if not db.existenceTable('url'):
        db.createUrlTable()

initialization()
if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=True, processes=True)