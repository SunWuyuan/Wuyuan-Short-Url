from flask import Flask, Response
from module import database, core
from view import api, page
import flask_cors
import config

app = Flask(__name__)
flask_cors.CORS(app, supports_credentials=True)
app.register_blueprint(api.API_APP)
app.register_blueprint(page.PAGE_APP)

@app.errorhandler(500)
def error500(error: Exception) -> Response:
    return core.GenerateResponse().error(500, '未知错误', httpCode=500)

def initialization() -> None:
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
    app.run(host=config.HTTP['host'], port=config.HTTP['port'], debug=True)