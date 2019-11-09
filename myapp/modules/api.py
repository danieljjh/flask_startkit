# -*- coding: UTF-8 -*-
"""
api.py
- provides the API endpoints for wx
  REST requests and responses

"""

from flask import Blueprint, jsonify, request, current_app, abort, g
from flask import redirect, url_for
from myapp.model.models import *
# from flask_httpauth import HTTPBasicAuth
# from passlib.apps import custom_app_context
# import hashlib
import requests
import datetime as dt
import time
# import os
# import os.path
import random
# import urllib
# from .views import *
# try:
#     import xml.etree.cElementTree as ET
# except ImportError:
#     import xml.etree.ElementTree as ET
# from .mycache import cache

app = current_app
blu_api = Blueprint('api', __name__)
#   在 app/__init__.py  文件里有 以下内容：
#    from .modules.api import blu_api
#    app.register_blueprint(blu_api, url_prefix="/api")
#   所以， api.py 的 网址 都是 以  /api 开始的
#   /my_get  的完整网址是  127.0.0.1:5000/api/my_get
###


@blu_api.route('/my_get', methods=['GET'])
# ： 这个是 网址， methods: 指定这个网址可以接受 哪种 request
# route 是 外部调用的 地址 ， 而 def 的名称是 用于内部 function 调用的
def my_api_get():
    """
     my first api
     method: GET
     input:
            http://localhost:5000/api/my_get?name=yale&age=14
     output:
        json
    """
    name = request.args.get('name')
    age = request.args.get('age')
    print('age:', age, 'type of age', type(age), sep=' ')
    #: API 收到的 GET 方式的 请求，用 request.args.get('name') 方式获取， 'name' 是参数名称
    #: GET 方式传递的参数，都是字符
    res = dict(name=name, age=age)
    # 用 jsonify 把 dict 转为 json
    return jsonify(res)


@blu_api.route('/my_post', methods=['POST'])
def my_api_post():
    """
     my first api
     method: POST
     input:
            http://localhost:5000/api/my_post

            {
                "name": "Yale",
                "age": 14,
                "education": {
                    "school": "sx",
                    "class": "m1"
                }
            }
     output:
        json
    """
    data = request.get_json()
    name = data['name']
    age = data['age']
    education = data['education']
    school = data['education']['school']
    # print('data:', data, 'type of data:', type(data), sep=' ')
    # print('age:', age, 'type of age', type(age), sep=' ')
    #: API 收到的 POST 方式的 请求，用 request.get_json() 方式获取， 得到的是 dict，再用 key 获取 json 的 value
    # ：POST 方式传递的参数，可以是字符，数值，日期，或者json
    res = dict(name=name, age=age, school=school)
    return jsonify(res)


@blu_api.route('/help', methods=['GET'])
def helps():
    """Print available route and functions."""
    func_list = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            options = {}
            methods = [m for m in rule.methods]
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)
            func_list.append(dict(
                route=rule.rule, route_docs=app.view_functions[rule.endpoint].__doc__, route_methods=methods, route_args=options))
            # func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    func_list = sorted(func_list, key=lambda k: k['route'])
    return jsonify(func_list)
