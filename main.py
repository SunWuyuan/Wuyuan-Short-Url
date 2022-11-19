# -*- coding: utf-8 -*-
# Author: XiaoXinYo

from flask import Flask
import flask_cors
from modular import database, core
from view.api import API_APP
from view.page import PAGE_APP

app = Flask(__name__)
flask_cors.CORS(app, resources=r'/*')
app.register_blueprint(API_APP)
app.register_blueprint(PAGE_APP)

@app.errorhandler(404)
def errorhandler404(error):
    return core.generateResponseResult('未找到文件', 404)

@app.errorhandler(500)
def errorhandler500(error):
    return core.generateResponseResult('未知错误', 500)

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
    if not db.existenceTable('url'):
        db.createUrlTable()

initialization()
'''
if __name__ == '__main__':
    initialization()
    app.run(host='0.0.0.0', port=5000, debug=True, processes=True)
'''