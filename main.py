from flask import Flask, Response
from module import core, model
from view import api, page
import flask_cors
import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{config.DATABASE["username"]}:{config.DATABASE["password"]}@{config.DATABASE["host"]}:{config.DATABASE["port"]}/{config.DATABASE["name"]}?ssl_ca=./isrgrootx1.pem&ssl_verify_cert=true&ssl_verify_identity=true'
flask_cors.CORS(app, supports_credentials=True)
app.register_blueprint(api.API_APP)
app.register_blueprint(page.PAGE_APP)
model.DB.init_app(app)

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

    with app.app_context():
        model.DB.create_all()
        if not model.Core.query.filter_by(name='title').first():
            model.DB.session.add(model.Core('title', '悟元短链接'))
        if not model.Core.query.filter_by(name='keyword').first():
            model.DB.session.add(model.Core('keyword', '悟元短链接'))
        if not model.Core.query.filter_by(name='description').first():
            model.DB.session.add(model.Core('description', '缩短链接.'))
        model.DB.session.commit()

initialization()
if __name__ == '__main__':
    app.run(host=config.HTTP['host'], port=config.HTTP['port'], debug=True)
