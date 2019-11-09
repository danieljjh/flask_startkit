# -*- coding: UTF-8 -*-
"""
- creates a Flask app instance and registers the database object
"""
import os
import logging
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, auth_token_required, current_user, utils, roles_accepted, auth_required
from flask_cors import CORS
from flask_caching import Cache
# from flask_socketio import SocketIO, emit

from myapp.model.models import *
# from flask_pymongo import pymongo


cache = Cache(config={'CACHE_TYPE': 'simple'})
# socketio = SocketIO()


def create_app(app_name='MyFlask'):
    app = Flask(app_name)
    if "DanielJiang" in os.getcwd():
        app.config.from_object('myapp.config.BaseConfig')
    else:
        app.config.from_object('myapp.config.ProductionConfig')

    CORS(app)

    handler = logging.FileHandler(
        app.config['LOGGING_LOCATION'], encoding='UTF-8')
    handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    handler.setFormatter(formatter)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.addHandler(handler)

    cache.init_app(app)

    from .modules.api import blu_api
    app.register_blueprint(blu_api, url_prefix="/api")

    from .modules.survey import blu_survey
    app.register_blueprint(blu_survey, url_prefix="/api/survey")

    from .modules.page import blu_page
    app.register_blueprint(blu_page, url_prefix="/pages")

    # from .modules.my_socket import socket_blu
    # app.register_blueprint(socket_blu, url_prefix="/socket")

    # socketio.init_app(app)
    db.init_app(app)
    return app
