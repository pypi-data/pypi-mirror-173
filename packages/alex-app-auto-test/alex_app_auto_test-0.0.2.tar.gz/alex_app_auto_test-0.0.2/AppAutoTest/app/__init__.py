#!/usr/bin/env python
# coding=utf-8

from flask import Flask
# from flask_bootstrap import Bootstrap
# from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

# bootstrap = Bootstrap()
# moment = Moment()
db = SQLAlchemy()

from config import config


def create_app(config_mode):
    app = Flask(__name__,template_folder="../app/templates",static_folder="../app/static")
    app.config.from_object(config[config_mode])
    config[config_mode].init_app(app)

    # bootstrap.init_app(app)
    # moment.init_app(app)
    db.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
