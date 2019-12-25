# coding = utf-8
"""
@author: zhou
@time:2019/12/12 14:55
@File: __init__.py
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_apscheduler import APScheduler
from flask_cors import CORS


db = SQLAlchemy()
scheduler = APScheduler()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    scheduler.init_app(app)
    CORS(app, )

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
