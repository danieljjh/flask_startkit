# -*- coding: UTF-8 -*-
"""
models.py
- Data classes for the surveyapi application
"""
# from flask import Blueprint, request, current_app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from passlib.apps import custom_app_context
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, auth_token_required
from .query_mixin import QueryMixin
from flask import current_app
from sqlalchemy import *
import sqlalchemy.types as types
import json
import jsonpickle


# from flask_pymongo import PyMongo
# from flask_mongoengine import MongoEngine


db = SQLAlchemy()
# mongo = PyMongo()
# me = MongoEngine()


def row2dict(row):
    if row is None:
        return ""
    d = {}
    for column in row.__table__.columns:
        if isinstance(getattr(row, column.name), String):
            d[column.name] = getattr(row, column.name)
        elif isinstance(getattr(row, column.name), datetime):
            d[column.name] = str(getattr(row, column.name))
        else:
            # d[column.name] = str(getattr(row, column.name))
            d[column.name] = getattr(row, column.name)
    return d


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_on = db.Column(db.DateTime, default=db.func.current_timestamp(),
                            onupdate=db.func.current_timestamp())


class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('users.id'))
    role_id = Column('role_id', Integer(), ForeignKey('roles.id'))


class User(Base, db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(32))
    active = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    wxid = db.Column(db.String(128))
    xcxid = db.Column(db.String(128))
    union_id = db.Column(db.String(128))
    nick_name = db.Column(db.String(50))
    icon_url = db.Column(db.String(128))
    roles = db.relationship(
        'Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User %r>' % self.username


class Role(Base, db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<UserRole %r>' % self.name


class WxUser(db.Model, QueryMixin):
    __tablename__ = 'wx_user'
    id = db.Column(db.Integer, primary_key=True)
    xcxId = db.Column(db.String(128), index=True)
    nickName = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))


# Surveys
class Surveys(Base, db.Model, QueryMixin):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True)
    survey_name = db.Column(db.String(30))
    survey_description = db.Column(db.String(120))
    active = db.Column(db.Boolean, default=True)


#: Survey questions
class SurveyQuestions(db.Model, QueryMixin):
    __tablename__ = 'survey_questions'
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, index=True)
    question_id = db.Column(db.Integer, index=True)
    question_name = db.Column(db.String(100))
    col_type = db.Column(db.String(30))
    value_type = db.Column(db.String(10))
    values = db.Column(JSON)


class SurveyResult(Base, db.Model, QueryMixin):
    __tablename__ = 'survey_result'
    id = db.Column(db.Integer, primary_key=True)
    wx_user_id = db.Column(db.Integer, index=True)
    survey_id = db.Column(db.Integer, index=True)
    survey_name = db.Column(db.String(30))


class SurveyResultDtl(db.Model, QueryMixin):
    __tablename__ = 'survey_result_dtl'
    id = db.Column(db.Integer, primary_key=True)
    result_id = db.Column(db.Integer, index=True)
    question_id = db.Column(db.Integer, index=True)
    label = db.Column(db.String(100))
    value_type = db.Column(db.String(10))
    value_cn = db.Column(db.String(50))


# class Friends(db.Model):
#     __tablename__ = 'friends'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(32), nullable=False, unique=True)
#     wx_id = db.Column(db.String(32), nullable=False, unique=True)
#     description = db.Column(db.String(50))


# class ChatGroups(db.Model):
#     __tablename__ = 'chat_group'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False, unique=True)
#     description = db.Column(db.String(255))


# class ChatGroupMember(db.Model):
#     __tablename__ = 'chat_grp_member'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False, unique=True)
#     description = db.Column(db.String(255))
#     chat_group_id = db.Column(db.Integer, db.ForeignKey(
#         'chat_group.id'), nullable=False)
#     chat_group = db.relationship(
#         'ChatGroups', backref=db.backref('chat_grp_member', lazy=True))
