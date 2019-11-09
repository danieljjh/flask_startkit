# -*- coding: UTF-8 -*-

"""
tools.py
- model tools
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
# from passlib.apps import custom_app_context
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
# from flask import current_app
from sqlalchemy import *
from myapp.model.models import *

# db = SQLAlchemy()

#: show model and model columns


def show_model_list():
    '''
        show model class
    '''
    res = [cls for cls in db.Model._decl_class_registry.values(
    ) if isinstance(cls, type) and issubclass(cls, db.Model)]
    return res


def show_model_dtl(model_class):
    """
        show columns
    """
    return [m.key for m in model_class.__table__.columns]


def all_model_columns():
    '''
        列出 models 里的 Class 的table 的 columns
    '''
    classes = show_model_list()
    res = []
    for x in classes:
        class_info = dict(name=x.__tablename__, columns=[
                          m.key for m in x.__table__.columns])
        res.append(class_info)
    return res
