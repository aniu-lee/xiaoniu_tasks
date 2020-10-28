from flask import Flask
from flask_celery import Celery
from flask_sqlalchemy import SQLAlchemy

from config import config

celery = Celery()

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    db.app = app

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    celery.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_bl
    app.register_blueprint(api_bl, url_prefix='/api')

    return app