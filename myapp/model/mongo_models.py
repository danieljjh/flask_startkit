# -*- coding: UTF-8 -*-
"""
models.py
- Data classes for the surveyapi application

show document fields:
[k for k,v in KidBooksMg._fields.iteritems()]

"""
# from flask import Blueprint, request, current_app
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy
# from flaskext.mysql import MySQL
# from passlib.apps import custom_app_context
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
# from flask import current_app
# from sqlalchemy import *
# from flask_pymongo import PyMongo
from flask_mongoengine import MongoEngine
from bson.objectid import ObjectId
from mongoengine import *


me = MongoEngine()


class KidBooksMg(me.Document):
    meta = {'collection': 'kidbooks'}
    level_id = IntField(required=True)
    unit_id = IntField(required=True)
    book_id = IntField(required=True)
    en_name = StringField(max_length=200, required=True)
    cn_name = StringField(max_length=200, required=True)
    text_audio_url = StringField(max_length=200, )
    main_words = StringField(max_length=200)
    explain_audio_url = StringField(max_length=200)
    sentence_pattern = StringField(max_length=200)
    notes = StringField(max_length=200)


class FollowMeMg(me.Document):
    '''
        contents: 
            no
            en_sentence
            cn_sentence
    '''
    meta = {'collection': 'followme'}
    level_id = IntField(required=True)
    unit_id = IntField()
    day_no = IntField(required=True)
    contents = ListField(required=True)