#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@qding.me
# Pw @ 2016-07-07 16:07


from flask import Flask, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import DevConfig, ProConfig, CeleryConfig
from celery import Celery
from flask_socketio import SocketIO
import logging
from logging.handlers import TimedRotatingFileHandler


bootstrap = Bootstrap()
db = SQLAlchemy()
socketio = SocketIO()
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(module)s "
                              "%(funcName)s %(message)s",
                              datefmt="%Y-%m-%d:%H:%M:%S"
                              )

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login_page'


def create_app():
    # NOTE init application object
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    app.jinja_env.filters["column_name"] = jinja_display_relation_name
    app.jinja_env.filters["generate_ip_list"] = jinja_generate_ip_list

    # NOTE config log
    file_handle = TimedRotatingFileHandler(
        app.config.get("LOG_PATH", "logs/access.log"), "D", 1
    )
    # file_handle = logging.FileHandler(app.config.get("LOG_PATH",
    #                                                  "logs/access.log"))
    file_handle.setFormatter(formatter)
    file_handle.setLevel(app.config.get("LOG_LEVEL", logging.INFO))
    app.logger.addHandler(file_handle)

    # NOTE init app
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    # NOTE 注册蓝图
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .user_control import user_control as user_control_blueprint
    app.register_blueprint(user_control_blueprint, url_prefix="/user_control")

    from .dashboard import dashboard as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/dashboard")

    return app
