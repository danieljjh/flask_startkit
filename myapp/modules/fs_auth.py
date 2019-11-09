"""
view for flask-security auth

"""
from flask import render_template, json, jsonify, request, abort, g
from flask import Blueprint, jsonify, request, current_app
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, current_user, utils, roles_accepted, auth_required
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)

from myapp.model.models import *
# app = create_app()
# from flask_httpauth import HTTPBasicAuth
# from passlib.apps import custom_app_context
# from flask import current_app

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')
# app = current_app


@auth_bp.route("/list_user/", methods=['GET', 'POST'])
def un_auth():
    users = User.query.all()
    return jsonify({'data': [row2dict(x) for x in users]})


@auth_bp.route("/user_login/", methods=['POST'])
def login_jwt():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {'access_token': create_access_token(username)}
    return jsonify(ret), 200


@auth_bp.route("/get_user/", methods=['POST'])
@login_required
# @auth_token_required
def current_user_info():
    roles = current_user.roles
    r = [row2dict(x) for x in roles]
    # return jsonify({'user': current_user.username, 'token': current_user.get_auth_token()})
    return jsonify({'user': current_user.username, 'roles': r})


@auth_bp.route("/token_login/", methods=['GET', 'POST'])
# @roles_required('admin')
# @auth_token_required
@jwt_required
def token_login():
    '''
    '''
    current_user = get_jwt_identity()
    u = current_user
    # tk = current_user.get_auth_token()
    # roles = [row2dict(x)['name'] for x in current_user.roles]
    return jsonify({'user': u, 'roles': 'roles'})


@auth_bp.route("/fsrole/")
# @roles_accepted('op')
def flask_security_login2():
    u = row2dict(current_user)
    tk = current_user.get_auth_token()
    return jsonify({'user': u, 'token': tk})


@auth_bp.route('/users/create/', methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    user_role = request.json.get('user_role')
    r = user_datastore.create_user(username=username, password=password)
    db.session.commit()
    return jsonify({'status': 'success', 'user': row2dict(r)})


@auth_bp.route('/logout/', methods=['POST'])
def logout():
    utils.logout_user()
    return jsonify({'status': 'success'})
