# -*- coding: utf-8 -*-
"""
page.py
- provides the API endpoints for operations
  REST requests and responses
"""
import os
import uuid

from flask import Flask, Blueprint, jsonify, request, current_app, url_for
from flask import render_template
# from flask_security import auth_token_required
# from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, current_user
from werkzeug import secure_filename
from myapp.model.models import db, row2dict
from myapp.common.tools import *

app = Flask(__name__)
blu_page = Blueprint('page_bp', __name__, template_folder='../templates')
# html 文件都放在 template_folder 指定的文件夹下


@blu_page.route('/home', methods=['GET', 'POST'])
def home_page():
    name = "yale"
    # app.logger.info(res)
    # 后台程序里的 参数 name  可以传递到 html
    # 在 详 见 home.html 里如何使用
    return render_template('home.html', name=name,  new_name='jyq')


@blu_page.route('/hello/<user_name>', methods=['GET'])
def hello_yale(user_name):
    # 这是一种传统的 页面跳转并传递参数的方式
    # 从 pages/home 页面 跳转到 pages/hello 页面， 并传递  user_name 参数
    # <user_name>  是参数
    return render_template('hello.html', user_name=user_name)


@blu_page.route('/a_form', methods=['GET', 'POST'])
def show_forms():
    """

    """
    param = "Hello, Yale"
    if request.method == 'POST':
        data = request.form['your_name']
        # print(data)
        return jsonify(data)
    return render_template('simple_form.html', param=param)


# @blu_page.route('/upload_content/', methods=['GET', 'POST'])
# def upload_content():
#     '''
#       upload learning content xls file
#     '''
#     if request.method == 'POST':
#         # print request.form()
#         f = request.files['file']
#         table_name = request.form.get("filetype")

#         df = pd.read_excel(f, sheet_name=0)
#         res = save_xls_to_db(table_name, df)
#         return jsonify(dict(content=table_name, result=res))
#     return render_template('upload_xls.html')
