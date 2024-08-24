from flask import Flask

def create_app():
    app = Flask(__name__)

    with app.app_context():
        from . import routes  # 引入 routes 模块

    return app
