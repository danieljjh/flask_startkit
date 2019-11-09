# -*- coding: utf-8 -*-
"""
config.py
- settings for the flask application object
"""
import logging


class BaseConfig(object):
    ENV = 'develop'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://jjh:jjhjjh100@localhost/quiz?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # used for encryption and session management
    SECRET_KEY = 'mysecretkey'
    # 安全配置
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = False
    LOGGING_LOCATION = 'log/app.log'
    LOGGING_FORMAT = '%(asctime)s  - in Module %(module)s: - Func %(funcName)s  - Line: %(lineno)s - %(message)s'
    LOGGING_LEVEL = logging.DEBUG
    # SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    # SECURITY_TRACKABLE = True
    SECURITY_PASSWORD_SALT = 'wubing'
    SECURITY_USER_IDENTITY_ATTRIBUTES = ['username']
    SECURITY_LOGIN_URL = '/api/login'
    SECURITY_TOKEN_MAX_AGE = 'None'  # never expired
    SECURITY_TOKEN_AUTHENTICATION_KEY = 'auth_token'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    # SECURITY_UNAUTHORIZED_VIEW = '/api/fs_auth/unauth/'
    # jwt flask-jwt-extended
    JWT_SECRET_KEY = 'myJwt'
    MONGO_URI = "mongodb://localhost:27017/ttxMongo"  # for PyMongo
    MONGODB_SETTINGS = {'db': 'ttxMongo'}  # for mongoengine


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''

    LOGGING_LEVEL = logging.ERROR
    # MONGODB_SETTINGS = {'db': 'ttxMongo'}  # for mongoengine


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''


class TestingConfig(BaseConfig):
    TESTING = True
